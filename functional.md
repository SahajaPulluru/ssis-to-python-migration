# UPDATED FUNCTIONAL DIAGRAMS & SEQUENCE MATRIX

This document contains the latest structural diagrams for the M.Tech final dissertation report, incorporating the **PyTesseract OCR Image Ingestion Subsystem** and the **FAISS RAG Bilingual Pseudo-HyDE Glossary Engine**.

---

## 1. Functional Block Diagram

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
    A["Raw Document Ingestion<br/>(PDF / DOCX / TXT / PNG / JPG / BMP)"] -->|Ingest & Detect Format| B["Ingestion Parser Node"]
    
    subgraph B ["Ingestion Subsystem"]
        B1["Format Router"]
        B2["Layout-Aware Text Extractor<br/>(pdfplumber / python-docx)"]
        B3["PyTesseract OCR Subsystem<br/>(Scanned Images & PDF Image Fallbacks)"]
        B4["Language Detector<br/>(langdetect / Override Check)"]
        
        B1 --> B2
        B1 --> B3
        B2 & B3 --> B4
    end
    
    class A Ingestion;
    class B,B1,B2,B3,B4 Ingestion;

    %% Preprocessing Node
    B4 -->|Original Text| C["PII Masker Subsystem<br/>(Spacy NER & Regex Patterns)"]
    C -->|Masked PII Text + Map| D["DNT Masker Subsystem<br/>(dnt.json Brand/ID Filters)"]
    class C,D Preprocess;

    %% Risk engine
    D -->|Fully Masked Text| E["Risk Classification Engine<br/>(3 Pillars: Sensitivity, Impact, Criticality)"]
    class E RiskEngine;

    %% Tiered Routing & RAG
    E -->|Tier: Low| F["Low-Risk Translation Adapter<br/>(NLLB-200-distilled-600M)"]
    E -->|Tier: Medium| G["Medium-Risk Translation Adapter<br/>(mBART-50 Many-to-Many)"]
    E -->|Tier: High| H["High-Risk Translation Adapter<br/>(Local TranslateGemma via Ollama)"]
    class F,G,H TransRoute;

    %% RAG Component
    H <-->|Semantic Context Query| RAG["FAISS RAG Glossary Engine"]
    subgraph RAG ["FAISS RAG Glossary Engine"]
        R1["Bilingual Pseudo-HyDE Generator<br/>(Fast Word-Level Trans Translation)"]
        R2["Bilingual Embedding Merger<br/>(Source Text + Hypothetical Target)"]
        R3["FAISS FlatIP Index<br/>(Inner Product Cosine Similarity Search)"]
        R1 --> R2 --> R3
    end
    class RAG,R1,R2,R3 TransRoute;

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

---

## 2. Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Analyst as User / Analyst
    participant Web as Dashboard (FastAPI)
    participant Orch as Orchestrator (orchestrator.py)
    participant Ingest as Ingestion Parser (ingestion.py)
    participant Pre as Preprocessor (preprocessing.py)
    participant Risk as Risk Engine (risk_engine.py)
    participant RAG as FAISS RAG Glossary (rag_glossary.py)
    participant Trans as Translation Router (translation.py)
    participant Val as Validation Engine (validation.py)
    participant Post as Post-Processor (post_processing.py)

    Analyst->>Web: Uploads Document (PDF/DOCX/PNG/JPG, Target="en")
    Web->>Orch: run_translation_pipeline(file_path, source, target)
    
    %% Ingestion with OCR
    Orch->>Ingest: ingest_document(file_path, target_lang)
    alt Upload is standard Digital PDF/DOCX
        Ingest->>Ingest: Extract digital text & format tables
    else Upload is Scanned Image or Non-Text PDF
        Ingest->>Ingest: Trigger PyTesseract OCR extraction
    end
    Ingest->>Ingest: Detect source language (langdetect)
    Ingest-->>Orch: Return TranslationState (raw_text, detected_lang)

    Orch->>Pre: Mask PII & DNT keywords
    Pre-->>Orch: Return masked text & token map
    Orch->>Risk: classify_document_risk(masked_text)
    Risk-->>Orch: Return Risk Metrics (Sensitivity, Impact, Criticality, Tier)
    
    alt Tier is High
        Orch->>RAG: retrieve_glossary_hints(text, target_lang)
        RAG->>RAG: Run Pseudo-HyDE (bilingual lookup)
        RAG->>RAG: Embed combined bilingual query
        RAG->>RAG: FAISS inner-product vector search
        RAG-->>Orch: Return top-k Glossary hints
        Orch->>Trans: execute_translation(masked_text, tier, glossary_hints)
        Trans->>Trans: Call local Ollama TranslateGemma (translategemma:4b)
    else Tier is Medium
        Orch->>Trans: execute_translation(masked_text, tier)
        Trans->>Trans: Call local mBART-50 (Many-to-Many)
    else Tier is Low
        Orch->>Trans: execute_translation(masked_text, tier)
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
