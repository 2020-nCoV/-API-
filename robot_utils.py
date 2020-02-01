import os
import redis
import smtplib
import datetime
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_config():
    config_path = os.path.dirname(os.path.abspath(__file__)) + "/conf.json"
    with open(config_path, 'r') as f:
        temp = json.loads(f.read())
        return temp


logging.basicConfig(level=logging.INFO, format=('%(levelname) -5s %(asctime)s %(name) -5s %(funcName) '
                                                '-5s %(lineno) -5d: %(message)s'))
LOGGER = logging.getLogger("ncov-news-robot")
__config__ = get_config()


def send_email(subject, content):
    smtp_client = smtplib.SMTP_SSL("smtp.exmail.qq.com", port="465")
    smtp_client.login(__config__["EMAIL_ACCOUNT"],
                      __config__["EMAIL_PASSWORD"])
    message = MIMEText(content, _charset='utf-8')
    message['Subject'] = subject
    message['From'] = f"ncov-news robot<{__config__['EMAIL_ACCOUNT']}>"
    to_email_list = __config__["RECEIVERS"]
    message['To'] = ";".join(to_email_list)
    result = smtp_client.sendmail(
        __config__["EMAIL_ACCOUNT"], to_email_list, message.as_string())
    LOGGER.info(f"send_email result:{result}")
    smtp_client.close()


redis_client = redis.Redis(host=__config__["REDIS_HOST"],
                           port=__config__["REDIS_PORT"],
                           password=__config__["REDIS_PASSWORD"],
                           db=4,
                           decode_responses=True)
LOGGER.info("redis ready!")
