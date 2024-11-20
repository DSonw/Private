import requests
import time
from urllib.parse import quote
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os


os.environ['NEW_VAR'] = 'YTLT'  # 环境变量
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.session()
def Login(user,password):
  url = "https://bbs.yantuchina.com/login.php"
  headers = {
    "Host": "bbs.yantuchina.com",
    "Connection": "keep-alive",
    "Origin": "https://www.yantuchina.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "https://www.yantuchina.com/login?t=bbs.yantuchina.com%2Fu.php",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": str(Encoding()) + "; 48c7e_lastpos=other"

  }

  login_data = "forward=&jumpurl=www.yantuchina.com%2Flogin%3Ft%3Dbbs.yantuchina.com%252Findex.php&step=2&ed=http%3A%2F%2Fbbs.yantuchina.com%2F&pwuser=" + user + "&pwpwd=" + password + "&remember=0"
  response = session.request("POST", url=url, headers=headers, data=login_data,allow_redirects=False)
  Login_URL = response.headers['Location']
  return Login_URL

def Login_2(Login_URL):
  url = Login_URL
  headers = {
    "Host": "www.yantuchina.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "https://www.yantuchina.com/login?t=bbs.yantuchina.com%2Findex.php",
  }
  response = session.request("GET",url = url,headers=headers,allow_redirects=False)
  Login_URL2 = response.headers['Location']
  return Login_URL2

def Login_3(Login_URL2):
  url = Login_URL2
  headers = {
    "Host": "bbs.yantuchina.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "https://www.yantuchina.com/login?t=bbs.yantuchina.com%2Findex.php",
  }
  response = session.request("GET",url = url,headers=headers,allow_redirects=False)
  verify = str(re.findall(r"verifyhash = '(.*?)'",response.text,re.M)[0])
  return verify

def Account_Sign(verify):
  url = "https://bbs.yantuchina.com/jobcenter.php?action=punch&verify=" + verify + "&nowtime=" + str(round(time.time()*1000)) + "&verify=" + verify
  sign_data = "step=2"
  headers = {
    "Host": "bbs.yantuchina.com",
    "Origin": "https://bbs.yantuchina.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "https://bbs.yantuchina.com/u.php",
  }
  sign_req = session.request("POST",url = url,data=sign_data,headers=headers,allow_redirects=False)
  message_re = """"message":'(.*?)',"""
  # print(sign_req.text)
  message = re.findall(message_re, sign_req.text, re.M)[0]
  print(message)


def Timestamp():
  return str(round(time.time()))


def Encoding():
  concent = '0	' + Timestamp() + '	/u.php'
  s = quote(concent)
  return s





if __name__ == '__main__':
  APP_NAME = '岩土论坛签到'
  ENV_NAME = "YTLT"
  print(f'''
  ✨✨✨ {APP_NAME}脚本✨✨✨
  ✨ 功能：
        签到打卡
  ✨ 抓包步骤：
        打开{APP_NAME}网址：https://www.yantuchina.com/
      多账号换行分割 
  ✨ 设置青龙变量：
  export {ENV_NAME}='账号@密码'多账号换行分割

  ✨✨✨ ✨✨✨
      ''')
  # 分割变量
  if ENV_NAME in os.environ:
    tokens = re.split("\n", os.environ.get(ENV_NAME))
  else:
    tokens = ['']
    print(f'无{ENV_NAME}变量')
    exit()

  if len(tokens) > 0:
    print(f"\n>>>>>>>>>>共获取到{len(tokens)}个账号<<<<<<<<<<")
  for i in range(len(tokens)):
    input_string = tokens[i]
    account, password = input_string.split('@')
    Login_URL = Login(account,password)
    Login_URL2 = Login_2(Login_URL)
    verify = Login_3(Login_URL2)
    Account_Sign(verify)
