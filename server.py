import os
import datetime
import json
import robot_utils
import requests


def load_dingxiangyuan_news_data():
    url = "https://file1.dxycdn.com/2020/0127/794/3393185296027391740-115.json"
    payload = {}
    headers = {
        'authority': 'file1.dxycdn.com',
        'accept': 'application/json',
        'origin': 'https://3g.dxy.cn',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'content-type': 'application/json;charset=utf-8',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://3g.dxy.cn/newh5/view/pneumonia_timeline',
    }
    response = requests.request(
        "GET", url, headers=headers, data=payload, timeout=60)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(
            f"load_dingxiangyuan_news_data fail,response.text:{response.text}")
        return []


def news_notify(dxy_news_data=[], source="央视新闻", news_flag_key=""):
    last_news_count = robot_utils.redis_client.get(news_flag_key)
    news_data = [x for x in dxy_news_data if source in x["infoSource"]]
    now_news_count = len(news_data)
    robot_utils.LOGGER.info(
        f"source:{source}, last_news_count:{last_news_count}, now_news_count:{now_news_count}")
    if last_news_count and int(last_news_count) == now_news_count:
        robot_utils.LOGGER.info(
            f"source:{source} news no update,skip!")
        return
    last_new_data = news_data[0]
    email_content = f"内容：「{last_new_data['summary']}』」\n 链接：{last_new_data['sourceUrl']}"
    robot_utils.send_email(
        f"{last_new_data['infoSource']}更新了-{last_new_data['title']}", email_content)
    robot_utils.LOGGER.info(f"send {source} email success!")
    robot_utils.redis_client.set(news_flag_key, now_news_count)


news_flags_list = robot_utils.__config__["NEWS_FLAGS_KEYS"]


def run():
    dxy_news_data = load_dingxiangyuan_news_data()
    for new_flags in news_flags_list:
        news_notify(dxy_news_data,
                    new_flags["source"], new_flags["flag_key"])


run()
