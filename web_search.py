import requests

def google_search(google_api_key, cse_id, query, num_results=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': google_api_key,
        'cx': cse_id,
        'q': query,
        'num': num_results
    }
    response = requests.get(url, params=params).json()
    return [item['snippet'] for item in response.get('items', [])]