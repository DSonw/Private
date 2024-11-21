# !/usr/bin/python3
# -- coding: utf-8 --
"""
打开小程序-钱包-更多, 找到协议头中的token，还有phone以及userId
设置青龙变量：{lvtoken}：token#phone#userId
多账号@、换行分割
每天跑一到两次就行
"""
# cron: 11 6,9,12,15,18 * * *
# const $ = new Env("顺丰速运");
import hashlib
import json
import os
import random
import time
import re
from datetime import datetime, timedelta
from sys import exit
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

os.environ['NEW_VAR'] = 'lvtoken'  # 环境变量
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class RUN:
    def __init__(self,token,index):
        parts = token.split('#')
        self.token = parts[0]
        self.phone = parts[1]
        self.userId = parts[2]
        self.headers = {
            'Host': "appapi.lvcchong.com",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11529",
            'content-type': "application/x-www-form-urlencoded",
            'Referer': "https://h5.lvcchong.com/",
            'Origin': "https://h5.lvcchong.com",
            "token": self.token
        }
        self.index = index + 1
        self.s = requests.session()
        self.s.verify = False
        print(f"\n---------开始执行第{self.index}个账号>>>>>")

    def do_request(self, url, payload,):
        max_attempts = 2
        attempts = 0
        try:
            while attempts < max_attempts:
                response = self.s.post(url, data=payload, headers=self.headers)
                # print(response.text)
                if response.json()['code'] == 402:
                    print('✨✨✨状态码 402，正在更新数据...✨✨✨')
                    self.UpdateData()
                elif response.json()['code'] == 200:
                    return response
                    break
                elif response.json()['code'] == -1:
                    return response
                    break
                elif response.json()['success'] == True:
                    return response
                    break
                else:
                    print(f'✨✨✨请求失败，返回内容：{response.text}✨✨✨')
                    break
                attempts += 1
                time.sleep(1)
            if attempts == max_attempts:
                print('已达到最大尝试次数。')
                return None
        except requests.exceptions.RequestException as e:
            print('Request failed:', e)
            return None
        except json.JSONDecodeError as e:
            print('JSON decoding failed:', e)
            return None


    #积分查询
    def PointsInquiry(self):
        url = "https://appapi.lvcchong.com/appBaseApi/scoreUser/getUserScoreDetails?channelMessage=LVCC-WP-PH_9.1.53_Tencent-G9"
        payload = "entranceType=2"
        response = self.do_request(url,payload)
        try:
            print(f"✨✨✨当前积分{response.json()['data']['score']}✨✨✨")
        except Exception as e:
            print(e)


    #更新token
    def UpdateData(self):
        url = "https://appapi.lvcchong.com/appBaseApi/h5/accessEntrance"
        payload = f"phone={self.phone}&userId={self.userId}&ownerId=0&time=" + self.Timestamp()
        response =  self.s.post( url, data=payload, headers=self.headers)
        # print(response.json()['data']['userToken'])
        self.headers["token"] = response.json()['data']['userToken']

    #获取时间戳
    def Timestamp(self):
        return str(round(time.time()*1000))

    # #获取用户信息
    # def Userinfo(self):
    #     url = "https://appapi.lvcchong.com/user/userInfo?channelMessage=LVCC-WP-PH_9.1.53_Tencent-G9"
    #     payload = "{}"
    #     response = self.s.post(url, data=payload, headers=self.headers)
    #     userId = response.json()['data']['id']
    #     phone = response.json()['data']['phone']
    #     return phone,userId


    #做任务
    def Dotask(self,taskType,remaining):
        try:
            for i in range(12):
                url = "https://appapi.lvcchong.com/appBaseApi/scoreUser/task/receiveTaskScore"
                payload = f"taskType={taskType}&status=1&isApp=0&sourceType=3"
                response = self.do_request(url, payload)
                print(f"✨✨✨{response.json()['code']}✨✨✨")
                if response.json()['code'] == -1:
                    # print(f"✨✨✨{response.text}✨✨✨")
                    return True
                random_delay = random.uniform(30, 40)
                print(f"✨✨✨Delaying for {random_delay:.2f} seconds...✨✨✨")
                time.sleep(random_delay)
            return True
        except Exception as e:
            print(e)
            return e



    #签到
    def UserSign(self):
        url = "https://appapi.lvcchong.com/appBaseApi/scoreUser/sign/userSign"
        payload = "sourceType=3"
        response = self.do_request(url,payload)
        if response != None and response.json()['code'] == 200:
            print(f"✨✨✨签到成功✨✨✨当前累计签到天数为{response.json()['data']['signDays']}天✨✨✨\n✨✨✨获得{response.json()['data']['score']}✨✨✨")
        else:
            print(f"✨✨✨已签到✨✨✨")



    #领取积分
    def ReceiveTaskScore(self,taskType):
        url = "https://appapi.lvcchong.com/appBaseApi/scoreUser/task/receiveTaskScore"
        payload = f"taskType={taskType}&status=2&isApp=0&sourceType=3"
        response = self.do_request(url,payload)
        if response.json()['code'] == 200:
            return True
        else:
            return False
    #获取任务信息
    def GetTaskList(self):
        url = "https://appapi.lvcchong.com/appBaseApi/scoreUser/task/getTaskList"
        payload = "sourceType=3"
        response = self.do_request(url,payload)
        print(f"✨✨✨查询到当前有{len(response.json()['data'])}条任务✨✨✨")
        for i, item in enumerate(response.json()['data']):
            taskName = response.json()['data'][i]['taskName']
            type = response.json()['data'][i]['type']
            score = response.json()['data'][i]['score']
            status = str(response.json()['data'][i]['status'])
            finishTimes = int(response.json()['data'][i]['finishTimes'])
            times = int(response.json()['data'][0]['times'])
            # print(times,finishTimes)
            remaining = int(times - finishTimes)
            if status == "0" :
                # print(remaining)
                # time.sleep(999)
                if self.Dotask(type,remaining) == True:
                    print(f"✨✨✨完成任务：{taskName}✨✨✨")
            elif status == "1" :
                if self.ReceiveTaskScore(type) == True:
                    print(f"✨✨✨完成任务：{taskName}，本次领取已完成任务积分{score}分✨✨✨")
            else:
                print(f"✨✨✨任务：{taskName}已完成,跳过✨✨✨")
                continue

    #拆红包
    def RedPacket(self):
        url = "https://appapi.lvcchong.com/appBaseApi/redPacket/result"
        payload = "redPacketId=4&inviterId="
        try:
            for i in range(6):
                response = self.do_request(url, payload)
                # print(response.text)
                if response != None and response.json()['success'] == True:
                    print(
                        f"✨✨✨恭喜你抽中了{response.json()['data']['name']}，数量为{response.json()['data']['number']}✨✨✨")
                    random_delay = random.uniform(30, 40)
                    print(f"✨✨✨Delaying for {random_delay:.2f} seconds...✨✨✨")
                    time.sleep(random_delay)
                elif response.json()['success'] == False:
                    print(f"✨✨✨红包已经拆完了，明天再来吧✨✨✨")
                    break
                else:
                    print(f"✨✨✨{response.text}✨✨✨")
                    break
                time.sleep(1)
        except Exception as e:
            print(e)
            print("999")
        time.sleep(1)





    def main(self):
        self.UpdateData()#更新token
        time.sleep(0.3)
        self.PointsInquiry()#获取积分
        time.sleep(0.3)
        self.UserSign()#开始签到
        time.sleep(0.3)
        self.GetTaskList()#查询任务
        time.sleep(0.3)
        self.RedPacket()#拆红包
        print(f"✨✨✨重新检查一次第{self.index}个账号任务情况✨✨✨")
        time.sleep(0.5)
        self.GetTaskList()  # 查询任务
        time.sleep(0.5)
        self.PointsInquiry()#获取积分
        return True






if __name__ == '__main__':
    APP_NAME = '驴充充'
    ENV_NAME = 'lvtoken'
    print(f'''
    ✨✨✨ {APP_NAME}脚本✨✨✨
    ✨ 功能：
          积分签到
          签到任务
          开红包
    ✨ 抓包步骤：
          打开{APP_NAME}小程序
          打开抓包工具
          点击 钱包
          点击“更多”，以下几种url之一：
            找到协议头中的token:ey..... 
    ✨ 设置青龙变量：{ENV_NAME}
        多账号@、换行分割
    ✨✨✨ ✨✨✨
        ''')
    # 分割变量
    if ENV_NAME in os.environ:
        tokens = re.split("@|\n", os.environ.get(ENV_NAME))
    else:
        tokens = ['']
        print(f'无{ENV_NAME}变量')
        exit()
    if len(tokens) > 0:
        print(f"\n>>>>>>>>>>共获取到{len(tokens)}个账号<<<<<<<<<<")
        for index, token in enumerate(tokens):
            run_result = RUN(token,index).main()
            if not run_result:
                continue






