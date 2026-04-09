from transform.transform_generic import transform_data

def test_transform_data_adds_audit_flag(sample_raw_dataframe):
    \"\"\"
    Test that our generic transform function correctly adds the _etl_processed_flag column
    to the incoming raw data.
    \"\"\"
    
    # Execute the transformation against our mocked fixture
    transformed_df = transform_data(sample_raw_dataframe)
    
    # Assert the new column exists
    assert '_etl_processed_flag' in transformed_df.columns
    
    # Assert the newly generated column logic was applied properly
    assert all(transformed_df['_etl_processed_flag'] == True)
    
    # Assert we did not lose any original rows
    assert len(transformed_df) == len(sample_raw_dataframe)
