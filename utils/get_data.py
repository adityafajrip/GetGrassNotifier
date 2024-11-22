import requests
from config import HEADERS

def get_earning_data(authorization_token):
    url = "https://api.getgrass.io/epochEarnings?input=%7B%22limit%22:1,%22isLatestOnly%22:true%7D"
    headers = HEADERS.copy()
    headers["authorization"] = authorization_token
    
    try:
        censored_token = authorization_token[:5] + "*****" + authorization_token[-5:]
        print(f"Get Earning data with: {censored_token}")
        
        response = requests.get(url, headers=headers)
        
        print(f"Response Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response Content-Type: JSON")
        else:
            print(f"Error: Status Code {response.status_code}")
        
        response.raise_for_status()  #Checking Status Code

        if 'application/json' in response.headers.get('Content-Type', ''):
            data = response.json()
        else:
            print("Response tidak dalam format JSON.")
            return None, None, None, None, None, None
        
        if 'result' in data and 'data' in data['result'] and len(data['result']['data']['data']) > 0:
            total_earning = data['result']['data']['data'][0]['totalPoints']
            today_earning = data['result']['data']['data'][0]['rewardPoints']
            epoch_name = data['result']['data']['data'][0].get('epochName', 'N/A')
            total_uptime = data['result']['data']['data'][0].get('totalUptime', 0)
            start_date = data['result']['data']['data'][0].get('startDate', 'N/A')
            end_date = data['result']['data']['data'][0].get('endDate', 'N/A')

            return total_earning, today_earning, start_date, end_date, epoch_name, total_uptime
        else:
            print("No valid data found in response")
            return None, None, None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data/Token Invalid: {e}")
        return None, None, None, None, None, None


def get_total_ips(authorization_token):
    url = "https://api.getgrass.io/activeDevices"
    headers = HEADERS.copy()
    headers["authorization"] = authorization_token
    
    #Logs
    censored_token = authorization_token[:5] + "*****" + authorization_token[-5:]
    print(f"Get Total IPs with: {censored_token}")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() #Checking Status Code
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Response Content-Type: JSON")
        else:
            print(f"Error: Received non-200 status code")

        try:
            data = response.json()
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            return []
        
        if 'result' in data and 'data' in data['result']:
            ips_data = data['result']['data']
            return ips_data
        else:
            print("Invalid data structure in response")
            return []
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
