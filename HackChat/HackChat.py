#!/usr/bin/python3
#coding: utf-8
import os
#
#   LOOK BY THIS DIRECTION
#   SLAVE <-------- LISTENER
#==================================================
#State|   
#?     PORT      |      USAGE
#OK    4333            PLAIN-TEXT MESSAGES(BY /dev/tty)
#      4334            FILE INCOMMING TCP(SLAVE <-- LISTENER)
#      4335            FILE OUTGOING TCP(SLAVE --> LISTENER)
#      4336            MASTER COMMAND
#      4337            SLAVE ASK(CAN TURN INTO SLAVE COMMAND IF NEED)
#      4338            KEEPALIVE LINK A
#      4339            KEEPALIVE LINK B
#      4340            CHAOS CHANNEL(SEND) (from /dev/urandom)
#      4341            CHAOS CHANNEL(RECEIVE) (from /dev/urandom)
#      4342            MULTI-DIRECT MONITORING DATA(JSON)
#      4343            NOTIFICATION EXCHANGE
#OK    4344            MASTER/SLAVE WEB API CHANNEL
#==================================================

def exit_hackchat():
    os.system("systemctl stop hackchat.api-com-1.service")
    exit(0)
#==================================================

import argparse
import time
import keyboard
parser = argparse.ArgumentParser()
parser.add_argument("role", type=str,
                    help="slave/victim or master/listener")
parser.add_argument("-u", action="store_true",help="Enable temporary user")
args = parser.parse_args()
if args.role == "stop":
    print("stop all in sure mode...")
    exit_hackchat()

import json, requests
from multiprocessing import Process
from copy import deepcopy

from termcolor import colored

with open("/etc/hackchat/core/config_connect.json","rb") as f:
    slave=json.loads(f.read())[0]["slave"]
    f.close()
#==================================================
with open("/etc/hackchat/core/config_connect.json","rb") as f:
    listener=json.loads(f.read())[0]["listener"]
    f.close()
#==================================================
slave_codes={
            "chat":"cat {} | nc {} {} > .chatfile",
            "date_output":"date > .date && nc -w 0 {} {} < .date",
            "date_input":"nc -w 0 -nlvp {} > .src_date"
            }
#==================================================
listener_codes={
                "chat":"nc -nlvp {} > .chatfile",
                "date_output":"date > .date && nc -w 0 {} {} < .date",
                "date_input":"nc -w 0 -nlvp {} > .src_date"
               }
#==================================================
data_info_log_last = {}


#
if args.role == "slave":
    chat_ = slave_codes["chat"].format(slave["chat"]["src"],slave["to"],slave["chat"]["port"])
    ip_ = slave["to"]
    date_input = slave_codes["date_input"].format(slave["date"]["api_port"])
    date_output = slave_codes["date_output"].format(slave["to"],slave["date"]["api_port"])

elif args.role == "master":
    chat_ = listener_codes["chat"].format(listener["chat"]["port"])
    ip_ = listener["from"]
    date_input = listener_codes["date_input"].format(listener["date"]["api_port"])
    date_output = listener_codes["date_output"].format(listener["from"],listener["date"]["api_port"])

#==================================================
if args.u:#place here the option args of temporary user
    username=input("username? :")
    os.system("sudo useradd {}".format(username))
    
#==================================================
time.sleep(10)
os.system("echo [true]>.chat_status")

def chat_fn_():
    os.system(chat_)
    os.system(date_output)
    os.system(date_input)

p_ = Process(target=chat_fn_)
p_.start()

def read_chat(last=20):
    with open(".chatfile",'r') as f:
        data = f.readlines()
        f.close()
    return "\n".join(data[-last:])

def pause_prompt():
    with open(".chat_status",'r') as f:
        chat_prompt = json.loads(f.read())
        f.close()
    chat_prompt = [ not chat_prompt[0] ]
    with open(".chat_status",'w') as f:
        f.write(json.dumps(chat_prompt))
        f.close()

def get_chat_prompt():
    with open(".chat_status", "r") as f:
        c = json.loads(f.read())[0]
        f.close()
    return c



# ================================================== For, Later
from base64 import b64encode as benc
from base64 import b64decode as bdec
from datetime import datetime
# ------
def timestamp():
    return str(datetime.now())

class AutoBase64(object):
    def __init__(self):
        super().__init__()
    
    def that_is_b64(self,test_str):
        try:
            result=bdec(self.auto_coding(test_str,need="encode"))
            return True
        except:
            return False
        return None

    def auto_coding(self,x_str,need="reverse",nop_no_need=True,param_coding=None):
        if type(x_str) == str:
            if need == "decode":
                if (not nop_no_need):
                    if param_coding==None:
                        return x_str.decode()
                    else:
                        return x_str.decode(param_coding)
            elif (need == "reverse") or (need == "encode"):
                if param_coding==None:
                    return x_str.encode()
                else:
                    return x_str.encode(param_coding)
        elif type(x_str) == bytes:
            if need == "encode":
                if (not nop_no_need):
                    if param_coding==None:
                        return x_str.encode()
                    else:
                        return x_str.encode(param_coding)
            if (need == "reverse") or (need == "decode"):
                if param_coding==None:
                    return x_str.decode()
                else:
                    return x_str.decode(param_coding)
            

    def autoB64(self,x_str,mode="auto"):
        if self.that_is_b64(x_str):
            if (mode == "auto") or (mode == "decode"):
                return bdec(self.auto_coding(x_str,need="encode")).decode()
            if mode == "encode":
                return x_str
        if not self.that_is_b64(x_str):
            if (mode == "auto") or (mode == "encode"):
                return benc(self.auto_coding(x_str,need="encode")).decode()
            if mode == "decode":
                return x_str

#==================================================
AB64 = AutoBase64()
# ------

keyboard.add_hotkey('ctrl+shift+p', pause_prompt)
keyboard.add_hotkey('ctrl+shift+!', exit_hackchat)
#keyboard.add_hotkey('ctrl+shift+m', switch_monitoring) 

def run_api_com():
    os.system("systemctl start hackchat.api-com-1.service")
    os.system("systemctl status hackchat.api-com-1.service > .hackchat.api-com-1.status")
    with open (".hackchat.api-com-1.status",'r') as status_f:
        data = { "hackchat.api-com-1": {"status": AB64.autoB64(status_f.read(),mode="encode"), "timestamp": timestamp() } }
    print(("{}{}"+chr(172)+"\n{}").format(colored("hackchat.","yellow","on_grey"),colored("api-com-1","cyan","on_grey"),colored(bdec(data["hackchat.api-com-1"]["status"].encode()).decode(),"white","on_grey")))
    print("\n\t⌊\n\t [timestamp]→ {}".format(colored(data["hackchat.api-com-1"]["timestamp"],"red")))
    data_info_log_last.update(data)
    time.sleep(10)

api_com1_ = Process(target=run_api_com)
api_com1_.start()
api_com1_.join()

if args.role == "master":
    name_adverse = "slave"
    #
    myself_=deepcopy(listener)
    adverse_=deepcopy(slave)
elif args.role == "slave":
    name_adverse = "master"
    #
    myself_=deepcopy(slave)
    adverse_=deepcopy(listener)
    #


if myself_["date"]["api_secure-disabled"] == True:
    myself_["date"]["protocol"] = "http"
elif myself_["date"]["api_secure-disabled"] == False:
    myself_["date"]["protocol"] = "https"
#
if adverse_["date"]["api_secure-disabled"] == True:
    adverse_["date"]["protocol"] = "http"
elif adverse_["date"]["api_secure-disabled"] == False:
    adverse_["date"]["protocol"] = "https"
#
name_myself = args.role 


while True:

    os.system("clear")
    myself_date = requests.get("{}://{}:{}/ask/date".format(myself_["date"]["protocol"],myself_["date"]["api_hostname"],myself_["date"]["api_port"])).json()
    adverse_date = requests.get("{}://{}:{}/ask/date".format(adverse_["date"]["protocol"],adverse_["date"]["api_hostname"],adverse_["date"]["api_port"])).json()
    print("Local Time: {}  \t|\t  {} Time: {}  \t|\t  You are the {} for this connexion.".format(myself_date["date"],name_adverse,adverse_date["date"],name_myself))

    if get_chat_prompt(): 
        print(read_chat())

    time.sleep(.2)





#==================================================

if args.u:
    os.system("sudo userdel {}".format(username))
#==================================================
