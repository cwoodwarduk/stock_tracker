from dotenv import load_dotenv
import os
import smtplib
import imghdr
from email.message import EmailMessage

import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

load_dotenv()
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

message = EmailMessage()

yf.pdr_override()
start = dt.datetime(2019,12,1)
now = dt.datetime.now()

stock = "gm"

targetPrice = 180

message["subject"] = "Go to the bank, please"
message["from"] = EMAIL_ADDRESS
message["to"] = "calum.james.woodward@gmail.com"

