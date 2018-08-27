import pandas as pd

def get_latency_dataframe():
    df_columns = ['full_unit_id', 'experiment', 'probe', 'region', 'depth', 
    'unit_id', 'latency_psth', 'latency_sdf', 'response_type']
    latency_dataframe = pd.DataFrame(columns=df_columns)
    return latency_dataframe