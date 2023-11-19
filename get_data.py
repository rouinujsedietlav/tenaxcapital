import requests
import json
import pandas as pd

def create_dataframe_from_bls_response(response):
    """
    Convert BLS API response into a pandas DataFrame and transform year-period to datetime.

    Parameters:
    response (dict): The response from the BLS API.

    Returns:
    DataFrame: A pandas DataFrame containing the data.
    """
    data = []

    for series in response['Results']['series']:
        series_id = series['seriesID']

        for entry in series['data']:
            #print(entry)
            # Extract year and period
            year = entry['year']
            period = entry['period']

            # Convert period to a month format (e.g., 'M01' to '01')
            month = period.replace('M', '')

            # Combine year and month to create a date string
            date_str = f'{year}-{month}'

            # Append the data to the list
            data.append({
                'seriesID': series_id,
                'date': pd.to_datetime(date_str, format='%Y-%m'),  # Convert to datetime
                'value': entry['value']
            })

    df = pd.DataFrame(data)

    return df

def fetch_bls_data(api_key, series_ids, start_year, end_year):
    """
    Fetch multiple series data from the BLS API.

    Parameters:
    api_key (str): Your BLS API key.
    series_ids (list of str): List of series IDs to fetch.
    start_year (int): Start year for the data.
    end_year (int): End year for the data.

    Returns:
    dict: The response data from the BLS API.
    """

    # BLS API endpoint for multiple series
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    # Construct the request payload
    data = json.dumps({
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": api_key
    })

    headers = {'Content-type': 'application/json'}

    # Make the API request
    response = requests.post(url, data=data, headers=headers)

    # Check for a successful response
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

        
def generate_tenax_data():
    # Example usage
    api_key = 'ce2af52907a84a39a1d55b7c1ab5b7ae'
    series_ids = ['CUSR0000SA0', 'CUSR0000SA0L1E','CUSR0000SAF1','CUSR0000SA0E','CUSR0000SAA','CUSR0000SAE','CUSR0000SAG','CUSR0000SAM','CUSR0000SAR','CUSR0000SAT']

    start_year = 2004
    end_year = 2023
    try:
        bls_data = fetch_bls_data(api_key, series_ids, start_year, end_year)
    except Exception as e:
        print(f"An error occurred: {e}")


    # Use the function with your BLS response
    df = create_dataframe_from_bls_response(bls_data).pivot(index='date',values='value', columns='seriesID')
    df = df[['CUSR0000SA0', 'CUSR0000SA0L1E','CUSR0000SAF1','CUSR0000SA0E','CUSR0000SAA','CUSR0000SAE','CUSR0000SAG','CUSR0000SAM','CUSR0000SAR','CUSR0000SAT']]

    df.columns=['All items', 'All items less food and energy', 'Food','Energy','Apparel','Education and communication', 'Other goods and services','Medical care','Recreation','Transportation']

    df.to_csv('db.csv')
    
generate_tenax_data()
