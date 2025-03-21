
import requests, json, datetime

class get_oura_data:
    
    @staticmethod
    def get_lastbpm():

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


        # 読み込んだ心拍数と時間をJSONファイルに保存
        with open('static/data.json', mode='w', encoding='utf-8') as f:
            json.dump(latest_data, f, ensure_ascii=False)
            
        # 保存したJSONファイルをdataとして使える形にして保存
        with open('static/data.json', mode='r', encoding='utf-8') as f:
            bpm_data = json.load(f)
        
        latest_bpm = bpm_data.get('bpm')
        latest_timestamp = bpm_data.get('timestamp')
        
        return latest_bpm, latest_timestamp
      


