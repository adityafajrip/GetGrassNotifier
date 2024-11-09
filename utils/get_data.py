import requests
from config import HEADERS, IPDATA_KEY


def get_earning_data(authorization_token):
    url = "https://api.getgrass.io/epochEarnings?input=%7B%22limit%22:1,%22isLatestOnly%22:true%7D"
    headers = HEADERS.copy()
    headers["authorization"] = authorization_token
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  #status code

        data = response.json()
        
        if 'result' in data and 'data' in data['result'] and len(data['result']['data']['data']) > 0:
            total_earning = data['result']['data']['data'][0]['totalPoints']
            today_earning = data['result']['data']['data'][0]['rewardPoints']
            epoch_name = data['result']['data']['data'][0].get('epochName', 'N/A')
            total_uptime = data['result']['data']['data'][0].get('totalUptime', 0)
            start_date = data['result']['data']['data'][0].get('startDate', 'N/A')
            end_date = data['result']['data']['data'][0].get('endDate', 'N/A')
            
            return total_earning, today_earning, start_date, end_date, epoch_name, total_uptime
        else:
            return None, None, None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data/Token Invalid: {e}")
        return None, None, None, None, None, None


def get_total_ips(authorization_token):
    url = "https://api.getgrass.io/activeDevices"
    headers = HEADERS.copy()
    headers["authorization"] = authorization_token
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if 'result' in data and 'data' in data['result']:
            ips_data = data['result']['data']
            return ips_data
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def get_country_flag(ip_address):
    try:
        url = f"https://api.ipdata.co/{ip_address}?api-key={IPDATA_KEY}&fields=flag,emoji_flag"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        flag_url = data.get('flag', None)
        emoji_flag = data.get('emoji_flag', None)
        
        if emoji_flag:
            return emoji_flag
        else:
            return None 
      
    except requests.exceptions.RequestException as e:
        print(f"Error fetching flag for IP {ip_address}: {e}")
        return None