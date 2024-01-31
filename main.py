from pyHoneygain import HoneyGain
from os import environ
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import time
import uvicorn

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
    print(f'Adding proxy {PROXY_IP}:{PROXY_PORT}')
    if 'PROXY_USERNAME' in environ and 'PROXY_PASSWORD' in environ:
        print(f'With credentials username:{PROXY_USERNAME} password:{"*" * len(PROXY_PASSWORD)}')
        try:
            successed = honeygain_user.set_proxy(f'{PROXY_IP}:{PROXY_PORT}:{PROXY_USERNAME}:{PROXY_PASSWORD}')
        except:
            successed = False
    else:
        try:
            successed = honeygain_user.set_proxy(f'{PROXY_IP}:{PROXY_PORT}')
        except:
            successed = False
    print(f'Adding proxy was{"" if successed else " not"} succesfull')


def error_placeholder():
    return {}

def getHoneyGainData():
    try:
        return {
            "me": honeygain_user.me,
            "devices": honeygain_user.devices,
            "stats": honeygain_user.stats,
            "stats_today": honeygain_user.stats_today,
            "stats_today_jt": honeygain_user.stats_today_jt,
            "notifications": honeygain_user.notifications,
            "payouts": honeygain_user.payouts,
            "balances": honeygain_user.balances
        }
    except:
        print("There was an error while getting data from HoneyGain")
        return {
            "me": error_placeholder,
            "devices": error_placeholder,
            "stats": error_placeholder,
            "stats_today": error_placeholder,
            "stats_today_jt": error_placeholder,
            "notifications": error_placeholder,
            "payouts": error_placeholder,
            "balances": error_placeholder
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


app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello": "World"}


@app.get("/infos/{item_id}")
async def read_info(item_id: str):
    data = getHoneyGainData()
    if item_id in data:
        return data[item_id]()
    else:
        return {
            "error": f'Item {item_id} not exist.'
        }

@app.get('/help')
def read_help():
    return {
        "infos": [key for key in getHoneyGainData().keys()],
        "functions": [key for key in runHoneyGainFunctions().keys()],
    }

@app.get("/functions/{item_id}")
async def read_function(item_id: str):
    functions = runHoneyGainFunctions()
    if item_id in functions:
        return functions[item_id]()
    else:
        return {
            "error": f'Function {item_id} not exist.'
        }
