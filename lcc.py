# !/usr/bin/python3
# -- coding: utf-8 --
"""
打开小程序-钱包-更多, 找到协议头中的token，还有phone以及userId
设置青龙变量：{lvtoken}：token#phone#userId
多账号@、换行分割
每天跑一到两次就行
如果要开启兑换请设置青龙变量：{SF_IS_EXCHANGE}：true；默认false
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

IS_EXCHANGE = os.environ.get('SF_IS_EXCHANGE', 'false').lower() == 'true'

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
        while attempts < max_attempts:
            try:
                response = self.s.post(url, data=payload, headers=self.headers, timeout=15)
                if not response.ok:
                    print(f"⚠️ 请求失败，状态码：{response.status_code}")
                    return None

                response_data = response.json()
                
                if "deficiencyBack" in response.text:
                    return response
                    
                # 处理已知状态码
                code = response_data.get('code')
                if code == 402:
                    print('🔄 触发402状态码，执行数据更新...')
                    self.UpdateData()
                elif code in (200, -1):
                    return response
                else:
                    print(f"⚠️ 未知响应状态码：{code}，响应内容：{response.text}")
                    
                return response

            except requests.exceptions.RequestException as e:
                print(f"🌐 网络请求异常：{str(e)}")
            except json.JSONDecodeError:
                print("🔠 响应解析失败，非JSON格式")
            except KeyError as e:
                print(f"🔑 JSON字段缺失：{str(e)}")
                
            attempts += 1
            print(f"🔄 正在进行第{attempts}次重试...")
            time.sleep(3)
        print("⚠️ 已达到最大重试次数")
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
        try:
            url = "https://appapi.lvcchong.com/appBaseApi/h5/accessEntrance"
            payload = f"phone={self.phone}&userId={self.userId}&ownerId=0&time=" + self.Timestamp()
            response = self.s.post(url, data=payload, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                print(f"⚠️ 更新token失败，HTTP状态码：{response.status_code}")
                return
            
            response_data = response.json().get('data', {})
            new_token = response_data.get('userToken')
            
            if new_token:
                self.headers["token"] = new_token
                print("✅ Token更新成功")
            else:
                print("⚠️ 获取到空Token，保持原Token")
        except Exception as e:
            print(f"🔥 更新Token时发生异常：{str(e)}")

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
                if "deficiencyBack" in response.text:
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
            # print("999")
        time.sleep(1)

    # 兑换功能
    def Exchange(self):
        try:
            url = "https://appapi.lvcchong.com/appBaseApi/scoreUser/score/createScoreOrder"
            payload = "id=855&price=2000&purchaseNumber=1&orderSource=3&channelName=%E5%BE%AE%E4%BF%A1%E5%B0%8F%E7%A8%8B%E5%BA%8F"
            
            # 强制更新token（即使main里有更新也再更新一次）
            self.UpdateData()
            
            response = self.do_request(url, payload)
            if response and response.status_code == 200:
                message = response.json().get('message', '未知返回')
                print(f"🛒 兑换结果：{message}")
                return True
            return False
        except Exception as e:
            print(f"🔥 兑换过程中发生异常：{str(e)}")
            return False



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
    
    # 新增兑换模式开关
    IS_EXCHANGE = os.environ.get('SF_IS_EXCHANGE', 'false').lower() == 'true'
    
    # 分割变量
    if ENV_NAME in os.environ:
        tokens = [t.strip() for t in re.split("@|\n", os.environ.get(ENV_NAME)) if t.strip()]
    else:
        tokens = []
        print(f'❌ 未找到{ENV_NAME}环境变量')
        exit()

    if not tokens:
        print("⚠️ 未检测到有效的账号配置")
        exit()

    # 兑换模式特殊处理
    if IS_EXCHANGE:
        print("\n🔵🔵🔵 当前处于积分兑换模式 🔵🔵🔵")
        print("❗ 注意：此模式将优先执行所有账号的兑换操作")


        # ================= 第一阶段：执行所有账号的兑换 =================
        print("\n" + "="*30)
        print("💰 开始处理所有账号的兑换操作")
        print("="*30)
        for index, token in enumerate(tokens):
            try:
                print(f"\n▶▶ 正在处理第{index+1}/{len(tokens)}个账号的兑换 ◀◀")
                runner = RUN(token, index)
                # 强制更新token保证兑换有效性
                runner.UpdateData()
                exchange_result = runner.Exchange()
                if exchange_result:
                    print(f"✅ 第{index+1}个账号兑换操作完成")
                else:
                    print(f"⛔ 第{index+1}个账号兑换操作失败")
                # 账号间随机间隔
                if index != len(tokens)-1:
                    time.sleep(random.randint(1, 3))
            except Exception as e:
                print(f"\n❌ 第{index+1}个账号兑换时发生异常：{str(e)}")
                continue

        print("\n" + "="*30)
        print("✅✅ 所有账号兑换操作已完成 ✅✅")
        print("="*30)
        print("🔄 10秒后开始执行常规任务...")
        time.sleep(10)

    # ================= 第二阶段：执行所有账号的常规任务 =================
    print("\n" + "="*30)
    print(f"🏃 开始处理所有账号的常规任务（共{len(tokens)}个账号）")
    print("="*30)
    for index, token in enumerate(tokens):
        try:
            print(f"\n▶▶ 正在处理第{index+1}/{len(tokens)}个账号的常规任务 ◀◀")
            runner = RUN(token, index)
            runner.main()
            # 账号间随机间隔
            if index != len(tokens)-1:
                time.sleep(random.randint(3, 8))
        except Exception as e:
            print(f"\n❌ 第{index+1}个账号执行常规任务时发生异常：{str(e)}")
            continue





