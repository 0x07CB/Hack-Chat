#!/usr/bin/python3
#coding: utf-8
#============================================================
from flask import Flask, escape, request
from flask import flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from copy import deepcopy
import os, hashlib, gzip
from base64 import b64encode as b64enc
from base64 import b64decode as b64dec
#from flask_cors import CORS
import requests
import json
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
# =====================================
from multiprocessing import Process
#==============================
import time
from datetime import datetime
#==============================
def create_app():

    #==================================================
    # =====================================
    app = Flask(__name__,template_folder="templates",static_folder="static")
    app.secret_key = os.urandom(4096)
    app.WTF_CSRF_SECRET_KEY = os.urandom(4096)
    #CORS(app)
    csrf = CSRFProtect()
    csrf.init_app(app)
    ##ALLOWED_EXTENSIONS_DOWNLOAD = ["json","csv"]
    #==================================================
    ##def allowed_file(filename):
    ##    return '.' in filename and \
    ##        filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS_DOWNLOAD
    
    #==================================================
    #==================================================
    @app.route('/ask/date',methods=["GET"])
    def call_main_route():
        os.system("date > .date")
        with open(".date",'r') as f:
            date_=f.read()
            f.close()
        return {"date":date_}
    #==================================================

    #==================================================
    #for just use... you know... that:
    #app.run("127.0.0.1",8000,True)
    #or launch command: gunicorn3 -b '127.0.0.1':'8000' --workers=2 'API:create_app()'
    return app
#============================================================