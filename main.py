import os
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import lxml
import re
import logging

base_onsei_url = 'https://www.dlsite.com/maniax/work/=/product_id/'

file_name_group = {'alpha': [], 'num': [], 'kana': [], 'kanji': [], 'unknown': []}
kana = '[ぁ-ん\u30A1-\u30F4]+'
alpha = r'^[a-zA-Z]+$'
kanji = r'^[\u4E00-\u9FD0]+$'
num = r'^[0-9]+$'


def bs_parse_movies(html):
    soup = BeautifulSoup(html, "lxml")
    # 查找所有class属性为maker_name的span标签
    span = soup.find_all('span', class_='maker_name')
    # 获取span中的a中的文本
    for each in span:
        return each.a.text


def get_group_name(onsei_id):
    logging.info("文件名：" + onsei_id)
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))

    onsei_url = base_onsei_url + onsei_id.strip() + '.html'
    onsei_request = session.get(onsei_url, timeout=10).text
    group_name = bs_parse_movies(onsei_request)
    logging.info("社团名：" + group_name)
    # 删除不符合windows系统文件命名要求的字符
    group_name = re.sub('[\\/:*?\"<>|]', '', group_name)
    return group_name


def scan_files(directory):
    # 不存在则创建文件夹
    if not os.path.exists(directory):
        logging.info("创建文件夹：" + directory)
        os.mkdir(directory)
    for file in os.listdir(directory):
        try:
            file_name = file.split(".")[0]
            group_name = get_group_name(file_name)
            group_name_type = check_char(group_name)
            file_name_group_name_dict = [file_name, group_name]
            file_name_group[group_name_type].append(file_name_group_name_dict)
        except BaseException as e:
            logging.info(e)
            logging.info("异常")
    # file_name_group : {{type:[filename, groupname], ....}, ....}
    return file_name_group


def check_char(str):
    if len(str) == 0:
        return "unknown"
    if re.compile(kana).match(str[0]) is not None:
        return "kana"
    elif re.compile(kanji).match(str[0]) is not None:
        return "kanji"
    elif re.compile(alpha).match(str[0]) is not None:
        return "alpha"
    elif re.compile(num).match(str[0]) is not None:
        return "num"
    else:
        return "unknown"
