import math

import hoshino
import datetime
import requests
from lxml import etree
from urllib import request
import time

sv = hoshino.Service('version', bundle='pcr娱乐')
url = 'https://minecraft.gamepedia.com/Java_Edition_'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 '
                  'Safari/537.36'}
s = "%B %d, %Y\n"
s2 = ": %B %d, %Y"


def get_date(v):
    detail_url = 'https://minecraft.gamepedia.com/Java_Edition_' + str(v)
    resp = requests.get(detail_url, headers=headers)
    text = resp.text
    html = etree.HTML(text)
    date = html.xpath('//*[@class="infobox-rows"]/tbody/tr[3]/td/p/text()')
    if not date:
        date = html.xpath('//*[@class="infobox-rows"]/tbody/tr[2]/td/p/text()')
        try:
            a = time.mktime(datetime.datetime.strptime(date[0], s).timetuple())
            return a
        except IndexError:
            return -1
    else:
        try:
            a = time.mktime(datetime.datetime.strptime(date[0], s).timetuple())
            return a
        except :
            date = html.xpath('//*[@class="infobox-rows"]/tbody/tr[2]/td/p/text()')
            try:
                a = time.mktime(datetime.datetime.strptime(date[0], s).timetuple())
                return a
            except :
                try:
                    a = time.mktime(datetime.datetime.strptime(date[0], s2).timetuple())
                    return a
                except:
                    date = html.xpath('//*[@class="infobox-rows"]/tbody/tr[4]/td/p/text()')
                    try:
                        a = time.mktime(datetime.datetime.strptime(date[0], s).timetuple())
                        return a
                    except:
                        return -1


@sv.on_prefix('/')
async def version(bot, ev):
    args = ev.message.extract_plain_text().split()
    ti = get_date(args[0])
    if ti != -1:
        now = datetime.datetime.timestamp(datetime.datetime.now())
        seconds = (now - ti)
        day = int(seconds // (3600 * 24))
        hour = int((seconds - day * 3600 * 24) // 3600)
        minute = int((seconds - (day * 24 + hour) * 3600) // 60)
        second = round(seconds - day * 3600 * 24 - hour * 3600 - minute * 60)
        if day < 366:
            msg = f"都过去{day}天{hour}小时{minute}分{second}秒了，你还在玩{args[0]}?"
            await bot.send(ev, msg)
        else:
            year = math.floor(day // 365)
            day = day - year * 365
            msg = f"都过去{year}年{day}天{hour}小时{minute}分{second}秒了，你还在玩{args[0]}?"
            await bot.send(ev, msg)
    else:
        await bot.send(ev, f"{args[0]}并不存在")
