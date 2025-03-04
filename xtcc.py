# !/usr/bin/python3
# -- coding: utf-8 --
"""
✨✨✨ 小兔充充脚本 ✨✨✨
✨ 功能：
       ▸ 广告抽奖
✨ 抓包步骤：
       ▸ 打开小程序-抓取协议头或提交请求中的uid
       ▸ 示例：uid=5458888
✨ 变量设置：
       ▸ 青龙变量：{tutuuid}
       ▸ 多账号使用 @ 或换行分隔
✨ 执行频率：
       ▸ 每日1-2次即可
■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
"""
import hashlib
import hmac
import json
import os
import random
import time
import re
from datetime import datetime, timedelta
from sys import exit
import requests
from urllib3.exceptions import InsecureRequestWarning

os.environ['NEW_VAR'] = 'tutuuid'
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

class RUN:
    def __init__(self, uid, index):
        self.uid = uid
        self.headers = {
            'Host': "mapi.xiaotucc.com",
            'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39(0x18002732) NetType/WIFI Language/zh_CN",
            'content-type': "application/x-www-form-urlencoded",
            'Referer': "https://servicewechat.com/wxa3dde54e66082a1b/281/page-frame.html",
            'Connection': "keep-alive",
            'Origin': "https://servicewechat.com/wxa3dde54e66082a1b/281/page-frame.html",
        }
        self.index = index + 1
        self.s = requests.session()
        self.s.verify = False
        print(f"\n{Color.CYAN}■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■{Color.END}")
        print(f"{Color.BOLD}🚀 开始执行第 {Color.GREEN}{self.index}{Color.END}{Color.BOLD} 个账号 {Color.CYAN}▶▶▶{Color.END}")

    def do_request(self, url, payload):
        max_attempts = 2
        attempts = 0
        while attempts < max_attempts:
            try:
                response = self.s.post(url, data=payload, headers=self.headers, timeout=15)
                if not response.ok:
                    print(f"{Color.RED}⚠️ 请求失败 | 状态码：{response.status_code}{Color.END}")
                    return None
                response_data = response.json()
                code = response_data.get('status')
                if code == 402:
                    print(f"{Color.YELLOW}🔄 触发数据更新（402）...{Color.END}")
                elif code in (200, -1):
                    return response
                else:
                    print(f"{Color.RED}⚠️ 未知状态码 {code} | 响应：{response.text}{Color.END}")
                return response
            except requests.exceptions.RequestException as e:
                print(f"{Color.RED}🌐 网络异常：{str(e)}{Color.END}")
            except json.JSONDecodeError:
                print(f"{Color.RED}🔠 响应解析失败{Color.END}")
            except KeyError as e:
                print(f"{Color.RED}🔑 缺失字段：{str(e)}{Color.END}")
            attempts += 1
            print(f"{Color.YELLOW}🔄 第 {attempts} 次重试中...{Color.END}")
            time.sleep(3)
        print(f"{Color.RED}⛔ 已达最大重试次数{Color.END}")
        return None

    def Timestamp(self):
        return str(round(time.time() * 1000))

    def GetToken(self):
        timestamp = self.Timestamp()
        s = f"xiaotu{timestamp}xiaotu{self.uid}xiaotu"
        o = hashlib.md5(s.encode("utf-8")).hexdigest()
        params = {
            "timestamp": timestamp,
            "sign": o,
            "uid": self.uid
        }
        sorted_keys = sorted(params.keys())
        param_str = "&".join([f"{k}={params[k]}" for k in sorted_keys])
        secret = "6D025A4E0DF3E14139F4CD3BCC6E8CDBC36824AE".encode("latin-1")
        hmac_sha1 = hmac.new(secret, param_str.encode("utf-8"), hashlib.sha1)
        return timestamp, o, self.uid, hmac_sha1.hexdigest().upper()

    def Raffle(self):
        try:
            for i in range(1, 13):
                print(f"\n{Color.CYAN}🎯 第 {i} 次抽奖尝试 {Color.END}")
                timestamp, o, uid, token = self.GetToken()
                url = "https://mapi.xiaotucc.com/user/lottery/take"
                payload = f"uid={uid}&sign={o}&timestamp={timestamp}&token={token}"
                response = self.do_request(url, payload)

                if not response:
                    continue

                resp_json = response.json()
                message = resp_json.get('message', '')
                data = resp_json.get('data', {})

                if "请求繁忙" in message:
                    print(f"{Color.YELLOW}⏳ 触发频率限制，等待 60 秒...{Color.END}")
                    time.sleep(60)
                elif "当天抽奖次数已用完" in message:
                    print(f"{Color.GREEN}✅ 今日抽奖次数已耗尽{Color.END}")
                    break
                elif isinstance(data, dict) and 'sName' in data:
                    print(f"{Color.GREEN}🎉 获得奖励：{Color.BOLD}{data['sName']}{Color.END}")
                    delay = random.uniform(30, 40)
                    print(f"{Color.YELLOW}⏲️ 等待 {delay:.1f} 秒...{Color.END}")
                    time.sleep(delay)
                else:
                    print(f"{Color.RED}❓ 未知响应：{resp_json}{Color.END}")
            return True
        except Exception as e:
            print(f"{Color.RED}🔥 抽奖异常：{e}{Color.END}")
            return False

    def main(self):
        self.Raffle()
        time.sleep(0.5)
        return True

if __name__ == '__main__':
    APP_NAME = '小兔充充'
    ENV_NAME = 'tutuuid'
    print(f'''
{Color.CYAN}╔══════════════════════════════════════════╗
║　　　　　　{Color.BOLD}{APP_NAME}自动化脚本{Color.END}{Color.CYAN}　　　　　　║
╠══════════════════════════════════════════╣
║🔍 {Color.YELLOW}功能概览{Color.END}{Color.CYAN}　　　　　　　　　　　　　　 ║
║ ▸ 广告抽奖自动执行　　　　　　　　　　　　║
║　　　　　　　　　　　　　　　　　　　　　　║
║🔧 {Color.YELLOW}变量设置{Color.END}{Color.CYAN}　　　　　　　　　　　　　　 ║
║ ▸ 青龙变量名：{ENV_NAME}　　　　　　　　　　║
║ ▸ 多账号使用 @ 或换行分隔　　　　　　　　 ║
╚══════════════════════════════════════════╝{Color.END}''')

    if ENV_NAME in os.environ:
        uids = re.split("@|\n", os.environ.get(ENV_NAME))
    else:
        uids = [""]
        print(f'\n{Color.RED}❌ 未找到环境变量 {ENV_NAME}{Color.END}')
        exit()

    if len(uids) > 0:
        print(f"\n{Color.GREEN}✔ 检测到 {len(uids)} 个账号 {Color.CYAN}◀◀◀{Color.END}")
        for index, uid in enumerate(uids):
            try:
                if not uid.strip():
                    print(f"{Color.RED}⚡ 第 {index+1} 个账号参数为空，跳过{Color.END}")
                    continue
                RUN(uid, index).main()
                print(f"{Color.GREEN}✅ 第 {index+1} 个账号执行完成 {Color.CYAN}◀◀◀{Color.END}")
            except Exception as e:
                print(f"\n{Color.RED}💥 异常账号：第 {index+1} 个")
                print(f"❗ 错误信息：{str(e)}")
                print(f"⏩ 跳过异常继续执行...{Color.END}")
                continue