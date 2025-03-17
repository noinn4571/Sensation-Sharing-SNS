import requests, json, datetime

OURA_TOKEN = "HNEMOKAN3CO3BZ3BLNAKLUK67QRAQYZM"

dt_now = datetime.datetime.now(datetime.timezone.utc)
dt_12h_ago = dt_now - datetime.timedelta(hours=12)

url = 'https://api.ouraring.com/v2/usercollection/heartrate'
params = {
    'start_datetime': dt_12h_ago.isoformat(),
    'end_datetime': dt_now.isoformat()
}
headers = {'Authorization': f'Bearer {OURA_TOKEN}'}

response = requests.get(url, headers=headers, params=params)
data = response.json()

hrs = data.get('data', [])

if hrs:
    latest = hrs[-1]
    latest_data = {
        'bpm': latest['bpm'],
        'timestamp': latest['timestamp']
    }
else:
    latest_data = {}

with open('static/data.json', mode='w', encoding='utf-8') as f:
    json.dump(latest_data, f, ensure_ascii=False)
