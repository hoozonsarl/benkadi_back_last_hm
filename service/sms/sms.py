import requests
import dotenv
import os
from datetime import datetime, timedelta
import json
dotenv.load_dotenv()

def send_sms_to_donneur(telephone: str, message: str):

    user = os.getenv("USER_SMS", "totiokamdem6@hoozonsarl.com")
    password = os.getenv("PASSWORD_SMS", "nexahHoozon123")
    result = False
    headers = {
         "Accept": "application/json",
         "Content-Type": "application/json",
    }

    data = {
        "user": user,
        "password": password,
        "senderid":"FGT_FERT",
        "sms": message,
        "mobiles": telephone,
        "scheduletime": str(datetime.now())
    }

    response = requests.post(url="https://smsvas.com/bulk/public/index.php/api/v1/sendsms", headers=headers, data=json.dumps(data))
   
    if response.ok:

        if response.json()["responsecode"] == 1:
            result = True
        else:
            result = False
    return result
