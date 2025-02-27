import requests
import hashlib
import time
from datetime import datetime

class FFTTApi:
    BASE_URL = "https://fftt.dafunker.com"
    
    @staticmethod
    def get_player(license_number: str) -> dict:
        # Paramètres requis
        tm = datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]  # Format: YYYYMMDDHHMMSSmmm
        
        # Headers constants
        headers = {
            'User-Agent': 'UnityPlayer/2021.3.34f1 (UnityWebRequest/1.0, libcurl/8.4.0-DEV)',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'SERIE': 'DSVGOUJKTZDCPTI',
            'ID': '<3',
            'TM': tm,
            'TMC': hashlib.sha1(tm.encode()).hexdigest(),
            'HASH': '9599691a9fe1ebd53cb23d8a23064283',
            'PREMIUM': '0',
            'SECRET': '23cd5e0a3e364b158046fec5c6371249',
            'VERSION': '171',
            'OS': 'android',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Unity-Version': '2021.3.34f1',
            'Connection': 'keep-alive'
        }
        
        try:
            response = requests.get(
                f"{FFTTApi.BASE_URL}/v1/joueur/{license_number}",
                headers=headers, verify=False
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
