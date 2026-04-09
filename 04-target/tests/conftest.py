import pytest
import pandas as pd

@pytest.fixture
def sample_raw_dataframe():
    \"\"\"
    A pytest fixture that returns a mocked DataFrame for testing transforms without needing
    a live database connection.
    \"\"\"
    return pd.DataFrame({
        'id': [1, 2, 3],
        'value': ['A', 'B', 'C']
    })
