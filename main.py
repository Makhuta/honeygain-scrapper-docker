from pyHoneygain import HoneyGain
from os import environ
from fastapi import FastAPI, Path
import time
from updater import Updater
from threading import Thread
import uvicorn
from typing import Dict, Any


UPDATE_DELAY = 10
UPDATE_TIMEOUT = 300


if 'HG_USERNAME' not in environ:
    raise ValueError("'HG_USERNAME' is not defined.")

    
if 'HG_PASSWORD' not in environ:
    raise ValueError("'HG_PASSWORD' is not defined.")

USERNAME = environ['HG_USERNAME']
PASSWORD = environ['HG_PASSWORD']
API_VERSION = environ.get('API_VERSION', '/v1')

honeygain_user = HoneyGain(API_VERSION=API_VERSION)
logged_in = False

while(not logged_in):
    print("Trying to log-in as: %s..." % USERNAME)
    try:
        honeygain_user.login(USERNAME, PASSWORD)
        logged_in = True
    except:
        print("There was error while logging in.")
        print("Trying again in an hour...")
        t = time.localtime()
        print("Next try will be at %02d:%02d:%02d" % ((t.tm_hour + 1) % 24, t.tm_min, t.tm_sec))
        time.sleep(3600)

print("Succesfully logged in")

if 'PROXY_IP' in environ and 'PROXY_PORT' in environ:
    print(f'Adding proxy {environ['PROXY_IP']}:{environ['PROXY_PORT']}')
    if 'PROXY_USERNAME' in environ and 'PROXY_PASSWORD' in environ:
        print(f'With credentials username:{environ['PROXY_USERNAME']} password:{"*" * len(environ['PROXY_PASSWORD'])}')
        try:
            successed = honeygain_user.set_proxy(f'{environ['PROXY_IP']}:{environ['PROXY_PORT']}:{environ['PROXY_USERNAME']}:{environ['PROXY_PASSWORD']}')
        except:
            successed = False
    else:
        try:
            successed = honeygain_user.set_proxy(f'{PROXY_IP}:{PROXY_PORT}')
        except:
            successed = False
    print(f'Adding proxy was{"" if successed else " not"} succesfull')

myUpdater = Updater(honeygain_user)

def getHoneyGainData():
    global myUpdater
    return {
        "me": myUpdater.get_me,
        "devices": myUpdater.get_devices,
        "stats": myUpdater.get_stats,
        "stats_today": myUpdater.get_stats_today,
        "stats_today_jt": myUpdater.get_stats_today_jt,
        "notifications": myUpdater.get_notifications,
        "payouts": myUpdater.get_payouts,
        "balances": myUpdater.get_balances
    }

def openPot():
    try:
        data = honeygain_user.open_honeypot()
        if not data["success"]:
            data["credits"] = 0
        return data
    except:
        return {
            "success": False,
            "credits": 0,
        }

def runHoneyGainFunctions():
    return {
        "open_honeypot": openPot
    }

def updating():
    global myUpdater
    while True:
        myUpdater.update_me()
        time.sleep(UPDATE_DELAY)
        myUpdater.update_devices()
        time.sleep(UPDATE_DELAY)
        myUpdater.update_stats()
        time.sleep(UPDATE_DELAY)
        myUpdater.update_stats_today()
        time.sleep(UPDATE_DELAY)
        myUpdater.update_stats_today_jt()
        time.sleep(UPDATE_DELAY)
        myUpdater.update_notifications()
        time.sleep(UPDATE_DELAY)
        myUpdater.update_payouts()
        time.sleep(UPDATE_DELAY)
        myUpdater.update_balances()
        time.sleep(UPDATE_TIMEOUT)

app = FastAPI(title="HoneyGain scrapper")

@app.get('/')
def read_root() -> Dict[str, Any]:
    return {"Hello": "World"}

@app.get("/infos/{item_id}")
async def read_info(item_id: str) -> Any:
    data = getHoneyGainData()
    if item_id in data:
        return data[item_id]()
    else:
        return {
            "error": f'Item {item_id} not exist.'
        }

@app.get("/functions/{item_id}")
async def read_function(item_id: str) -> Dict[str, Any]:
    functions = runHoneyGainFunctions()
    if item_id in functions:
        return functions[item_id]()
    else:
        return {
            "error": f'Function {item_id} not exist.'
        }

if __name__ == '__main__':
    updater_thread = Thread(target=updating, daemon=True)
    updater_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8080)