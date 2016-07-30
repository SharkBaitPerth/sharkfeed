"""
Sends SMS via Twilio! Config because I like not sharing secrets.
Mostly yoinked from http://www.blog.pythonlibrary.org/2014/09/23/python-101-how-to-send-smsmms-with-twilio/
"""
import configparser
from twilio.rest import TwilioRestClient


CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

def send_sms(msg):
    """Send custom message SMS via Twilio"""
    sid = CONFIG['Twilio']['Sid']
    auth_token = CONFIG['Twilio']['AuthToken']
    twilio_number = CONFIG['Twilio']['TwilioNumber']
    to_number = CONFIG['Twilio']['Phone']

    client = TwilioRestClient(sid, auth_token)

    client.messages.create(
        body=msg,
        from_=twilio_number,
        to=to_number,
    )
