# 2. FUNCTIONAL BLOCK DIAGRAM/DESCRIPTION OF TRANSLATION FRAMEWORK

The translation and analysis framework is orchestrated as a state-based sequential processing graph. All data transitions, token mappings, risk metrics, and evaluation scores are preserved within a unified `TranslationState` checkpoint context which is serialized to a local JSON database metastore. The functional block diagram of the framework and its data paths is shown below in Figure 2.

### Figure 2: FUNCTIONAL BLOCK DIAGRAM of translation pipeline graph

```mermaid
flowchart TD
    %% Styling
    classDef Ingestion fill:#1E293B,stroke:#3B82F6,stroke-width:2px,color:#F8FAFC;
    classDef Preprocess fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#F8FAFC;
    classDef RiskEngine fill:#311042,stroke:#d946ef,stroke-width:2px,color:#F8FAFC;
    classDef TransRoute fill:#022c22,stroke:#10b981,stroke-width:2px,color:#F8FAFC;
    classDef Validation fill:#450a0a,stroke:#f43f5e,stroke-width:2px,color:#F8FAFC;
    classDef Exporter fill:#1c1917,stroke:#a8a29e,stroke-width:2px,color:#F8FAFC;
    classDef UI fill:#172554,stroke:#3b82f6,stroke-width:2px,color:#F8FAFC;

    %% Ingestion Node
    A["Raw Document Ingestion<br/>(PDF / DOCX / TXT)"] -->|Ingest & Detect Language| B["Language Detector<br/>(langdetect / Manual Select)"]
    class A,B Ingestion;

    %% Preprocessing Node
    B -->|Original Text| C["PII Masker Subsystem<br/>(Spacy NER & Regex Patterns)"]
    C -->|Masked PII Text + Map| D["DNT Masker Subsystem<br/>(dnt.json Brand/ID Filters)"]
    class C,D Preprocess;

    %% Risk engine
    D -->|Fully Masked Text| E["Risk Classification Engine<br/>(3 Pillars: Sensitivity, Impact, Criticality)"]
    class E RiskEngine;

    %% Tiered Routing
    E -->|Tier: Low| F["Low-Risk Translation Adapter<br/>(NLLB-200-distilled-600M)"]
    E -->|Tier: Medium| G["Medium-Risk Translation Adapter<br/>(mBART-50 Many-to-Many)"]
    E -->|Tier: High| H["High-Risk Translation Adapter<br/>(Local TranslateGemma via Ollama)"]
    class F,G,H TransRoute;

    %% Validation Node
    F -->|Translated English Text| I["Multi-Agent Validation Suite"]
    G -->|Translated English Text| I
    H -->|Translated English Text| I
    
    subgraph I ["Validation & Audit Suite"]
        I1["Numerical & Currency Verifier<br/>(Deterministic Digit Checker)"]
        I2["Compliance Safety Guardrails<br/>(Money Laundering / Fraud Parser)"]
        I3["LLM Critic Agent<br/>(Semantic terminology checks)"]
        I4["Back-Translation Simulator<br/>(Drift similarity threshold >= 0.82)"]
    end
    class I,I1,I2,I3,I4 Validation;

    %% Auditor Decisions
    I -->|"Audit Passed (Low/Medium)"| J["Post-Processing Node<br/>(Unmask PII & DNT Tokens)"]
    I -->|"Audit Failed OR High-Risk Halt"| K["FastAPI Analyst Dashboard<br/>(Manual Review & Split-Pane Editor)"]
    class J Exporter;
    class K UI;

    %% Review gate and export
    K -->|Analyst Corrects & Approves| J
    J -->|Restored Clean Translation| L["NER Concept Extractor<br/>(Extract monetary, concepts, orgs)"]
    L -->|Linked Entity Metadata| M["JSON-LD Schema Exporter<br/>(Export Schema.org compliant Graph)"]
    class L,M Exporter;
```

### Figure 3: SEQUENCE DIAGRAM of framework execution code flow

```mermaid
sequenceDiagram
    autonumber
    actor Analyst as User / Analyst
    participant Web as Dashboard (FastAPI)
    participant Orch as Orchestrator (orchestrator.py)
    participant Pre as Preprocessor (preprocessing.py)
    participant Risk as Risk Engine (risk_engine.py)
    participant Trans as Translation Router (translation.py)
    participant Val as Validation Engine (validation.py)
    participant Post as Post-Processor (post_processing.py)

    Analyst->>Web: Uploads Document (Source Lang, Target="en")
    Web->>Orch: run_translation_pipeline(file_path, source, target)
    Orch->>Orch: Ingest document (extract text & detect language)
    Orch->>Pre: Mask PII & DNT keywords
    Pre-->>Orch: Return masked text & token map
    Orch->>Risk: classify_document_risk(masked_text)
    Risk-->>Orch: Return Risk Metrics (Sensitivity, Impact, Criticality, Tier)
    Orch->>Trans: execute_translation(masked_text, tier, glossary_hints)
    
    alt Tier is High
        Trans->>Trans: Call local Ollama TranslateGemma (translategemma:4b)
    else Tier is Medium
        Trans->>Trans: Call local mBART-50 (Many-to-Many)
    else Tier is Low
        Trans->>Trans: Call local NLLB-200 (600M)
    end

    Trans-->>Orch: Return translated text
    Orch->>Val: Audit translation (numbers match, safety scan, semantic drift)
    Val-->>Orch: Return validation scores and guardrail triggers

    alt Tier is High OR Validation fails
        Orch->>Orch: Save state context, pause at 'human_review' node
        Orch-->>Web: Return paused state
        Web-->>Analyst: Serve document edit form (Awaiting Analyst review)
        Analyst->>Web: Edit & approve translation draft
        Web->>Orch: resume_pipeline(doc_id)
    end

    Orch->>Post: Unmask PII/DNT and run Named Entity Recognition (NER)
    Post-->>Orch: Return clean English output & entities
    Orch->>Post: generate_json_ld(state)
    Post-->>Orch: Return JSON-LD schema
    Orch->>Orch: Save state context as 'complete'
    Orch-->>Web: Return final completed state
    Web-->>Analyst: Display "✓ APPROVED & EXPORTED TO GRAPH" and JSON-LD
```

---

### 1. SUB-SYSTEM NODE DESCRIPTIONS

#### a) File Ingestion Subsystem
This entrypoint node handles file parsing and language routing. It extracts raw unicode streams from uploaded documents while keeping structural layouts (tables, newlines, and list layouts) intact. Once the text is extracted, it calls the **Language Detection module** to determine the document's native script, routing the ISO code to the classification engine.

#### b) Preprocessing Masking Subsystem
The masking subsystem isolates critical customer identities and corporate markers prior to translation:
* **PII Masking:** Scans the text using a SpaCy NER pipeline and regular expression extractors to locate customer names, credit card numbers, email accounts, and SSNs, replacing them with formatted token tags (e.g., `__PII_EMAIL_0__`).
* **DNT (Do Not Translate) Masking:** Matches tokens against `dnt.json` definitions to catch and replace SWIFT codes, brand IDs, and IBAN formats. Both token mapping directories are saved in the database metastore to allow full reconstruction.

#### c) Risk Classification Subsystem
Evaluates the document against Sensitivity, Business Impact, and Criticality. It scans for regulatory concepts and high-value transactions (monetary figures exceeding $\$100,000$). Documents containing financial compliance triggers are immediately categorized as High-Risk to route them to the specialized TranslateGemma translation model and enforce dashboard review.

#### d) Translation Routing Subsystem
Directs document translation into English based on the assigned risk score:
* **NLLB-200-distilled-600M:** Executed for Low-Risk files, ensuring swift local translation.
* **mBART-50:** Executed for Medium-Risk files, leveraging its Seq2Seq architecture for structural contract terminology.
* **Ollama TranslateGemma (`translategemma:4b`):** Deployed for High-Risk files, delivering context-aware local translations while preserving all PII/DNT tags.

#### e) Validation & Auditing Subsystem
Performs a series of verification checks on the output translation:
* **Numerical Verifier:** Matches all numerals and currencies between source and translation.
* **Back-Translation Check:** Translates the text back to the source language using TranslateGemma and measures word-level Jaccard similarity. If the score falls below `0.82`, it triggers a dashboard review halt.
* **Safety Guardrails:** Scans translation for compliance violations (fraud, bribery, tax evasion) to alert the analyst.

#### f) Post-Processing & Exporter Subsystem
Once approved (either automatically for low/medium-risk documents or manually by the analyst), the system unmasks all tokens using the map directory, restoring the document's original names and codes. It then extracts financial Named Entities (NER) and exports the data into a standard **JSON-LD Schema** structure, allowing the translated document and its compliance metadata to be indexed into an enterprise **Knowledge Graph**.
