import hashlib
import json
import time
from urllib.parse import urlparse, parse_qs, urlencode
import requests
import datetime
import os


def md5(str):
    return hashlib.md5(str.encode('utf-8')).hexdigest().lower()


def get_sign(options):
    json_str = None
    keys = sorted(options.keys())
    signstr = "FcuhuxfY2vMSafr3"

    for k in keys:
        v = options[k]
        if k == 'json':
            json_str = v
        else:
            signstr += k + str(v)

    if json_str:
        signstr += json.dumps(json_str, separators=(',', ':'))

    return md5(signstr)


def get_13_digit_timestamp():
    return int(time.time() * 1000)


def extract_url_params(account_url):
    parsed_url = urlparse(account_url)
    query_params = parse_qs(parsed_url.query)
    params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
    params['timestamp'] = get_13_digit_timestamp()
    return params


def CreateTeam(account_url):
    print("\n[创建队伍] 开始创建队伍...")
    object = extract_url_params(account_url)
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://m.yonghuivip.com',
        'Referer': 'https://m.yonghuivip.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Redmi K20 Pro Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340129 MMWEBSDK/20250201 MMWEBID/6119 MicroMessenger/8.0.60.2860(0x28003C53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxc9cf7c95499ee604',
        'X-Requested-With': 'com.tencent.mm',
        '$X-YH-Biz-Params': 'ncjkdy=,Q)H&nzggzmdy=(&xdotdy=\\u0021&gib=--,0+__-)\\u0021*(\\u0021---++&gvo=_\'0--$,+\'*\\u0021\'\'\'),(\\u0021&vkkdy=yKWHqna(DlqXsuHhk)',
        'X-YH-Context': 'origin=h5&morse=1',
    }
    url = 'https://api.yonghuivip.com/web/coupon/credit/dividePoint/createTeam'
    params = (
        ('timestamp', object['timestamp']),
        ('channel', '512'),
        ('platform', 'wechatminiprogram'),
        ('v', '11.6.0.125'),
        ('app_version', '11.6.0.125'),
        ('appid', 'wxc9cf7c95499ee604'),
        ('wechatunionid', object['wechatunionid']),
        ('deviceid', object['deviceid']),
        ('sellerid', '7'),
        ('cityid', '4'),
        ('shopid', object['shopid']),
        ('channelSub', ''),
        ('brand', object['brand']),
        ('model', object['model']),
        ('os', object['os']),
        ('osVersion', object['osVersion']),
        ('networkType', 'wifi'),
        ('screen', object['screen']),
        ('productLine', 'YhStore'),
        ('jysessionid', object['jysessionid']),
        ('appType', 'h5'),
        ('access_token', object['access_token']),
    )
    params_dict = {key: value for key, value in params}
    sign = get_sign(params_dict)
    params_dict['sign'] = sign
    query_string = urlencode(params_dict)
    full_url = f"{url}?{query_string}"
    payload = {
        "shopId": object['shopid'],
    }
    response = requests.request("POST", full_url, data=json.dumps(payload), headers=headers)
    teamCode = response.json()['data']['teamCode']
    print(f"[创建队伍] 成功，队伍码: {teamCode}")
    return teamCode


def JoinTeam(account_url, teamCode):
    print(f"[加入队伍] 正在加入队伍 {teamCode}...")
    object = extract_url_params(account_url)
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://m.yonghuivip.com',
        'Referer': 'https://m.yonghuivip.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Redmi K20 Pro Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340129 MMWEBSDK/20250201 MMWEBID/6119 MicroMessenger/8.0.60.2860(0x28003C53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxc9cf7c95499ee604',
        'X-Requested-With': 'com.tencent.mm',
        '$X-YH-Biz-Params': 'ncjkdy=,Q)H&nzggzmdy=(&xdotdy=\\\\u0021&gib=--,0+__-)\\\\u0021*(\\\\u0021---++&gvo=_\'0--$,+\'*\\\\u0021\'\'\'),(\\\\u0021&vkkdy=yKWHqna(DlqXsuHhk)',
        'X-YH-Context': 'origin=h5&morse=1',
    }
    url = 'https://api.yonghuivip.com/web/coupon/credit/dividePoint/joinTheParty'
    params = (
        ('timestamp', object['timestamp']),
        ('channel', '512'),
        ('platform', 'wechatminiprogram'),
        ('v', '11.6.0.125'),
        ('app_version', '11.6.0.125'),
        ('appid', 'wxc9cf7c95499ee604'),
        ('wechatunionid', object['wechatunionid']),
        ('deviceid', object['deviceid']),
        ('sellerid', '7'),
        ('cityid', '4'),
        ('shopid', object['shopid']),
        ('channelSub', ''),
        ('brand', object['brand']),
        ('model', object['model']),
        ('os', object['os']),
        ('osVersion', object['osVersion']),
        ('networkType', 'wifi'),
        ('screen', object['screen']),
        ('productLine', 'YhStore'),
        ('jysessionid', object['jysessionid']),
        ('appType', 'h5'),
        ('access_token', object['access_token']),
    )
    params_dict = {key: value for key, value in params}
    sign = get_sign(params_dict)
    params_dict['sign'] = sign
    query_string = urlencode(params_dict)
    full_url = f"{url}?{query_string}"
    payload = {
        "teamCode": teamCode,
        "shopId": object['shopid'],
    }
    response = requests.request("POST", full_url, data=json.dumps(payload), headers=headers)
    resp_json = response.json()
    if resp_json.get('code') == 0 and resp_json.get('data', {}).get('isSuccess'):
        print("[加入队伍] 成功")
    else:
        message = resp_json.get('message', '未知错误')
        print(f"[加入队伍] 失败: {message}")


def DOTask(account_url, taskId, taskCode):
    object = extract_url_params(account_url)
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://m.yonghuivip.com',
        'Referer': 'https://m.yonghuivip.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Redmi K20 Pro Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340129 MMWEBSDK/20250201 MMWEBID/6119 MicroMessenger/8.0.60.2860(0x28003C53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxc9cf7c95499ee604',
        'X-Requested-With': 'com.tencent.mm',
        '$X-YH-Biz-Params': 'ncjkdy=,Q)H&nzggzmdy=(&xdotdy=\\\\u0021&gib=--,0+__-)\\\\u0021*(\\\\u0021---++&gvo=_\'0--$,+\'*\\\\u0021\'\'\'),(\\\\u0021&vkkdy=yKWHqna(DlqXsuHhk)',
        'X-YH-Context': 'origin=h5&morse=1',
    }
    url = 'https://api.yonghuivip.com/web/member/task/doTask'
    params = (
        ('timestamp', object['timestamp']),
        ('channel', '512'),
        ('platform', 'wechatminiprogram'),
        ('v', '11.6.0.125'),
        ('app_version', '11.6.0.125'),
        ('appid', 'wxc9cf7c95499ee604'),
        ('wechatunionid', object['wechatunionid']),
        ('deviceid', object['deviceid']),
        ('sellerid', '7'),
        ('cityid', '4'),
        ('shopid', object['shopid']),
        ('channelSub', ''),
        ('brand', object['brand']),
        ('model', object['model']),
        ('os', object['os']),
        ('osVersion', object['osVersion']),
        ('networkType', 'wifi'),
        ('screen', object['screen']),
        ('productLine', 'YhStore'),
        ('jysessionid', object['jysessionid']),
        ('appType', 'h5'),
        ('access_token', object['access_token']),
    )
    params_dict = {key: value for key, value in params}
    sign = get_sign(params_dict)
    params_dict['sign'] = sign
    query_string = urlencode(params_dict)
    full_url = f"{url}?{query_string}"
    payload = {
        "taskId": taskId,
        "shopId": object['shopid'],
        "taskCode": taskCode
    }
    response = requests.request("POST", full_url, data=json.dumps(payload), headers=headers)
    if response.json()['code'] == 0:
        return "任务已完成"
    elif response.json()['code'] == 700005:
        return response.json()['message']
    else:
        return response.text


def FreeList(account_url):
    print("\n[试用任务] 开始执行试用任务...")
    object = extract_url_params(account_url)
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://m.yonghuivip.com',
        'Referer': 'https://m.yonghuivip.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Redmi K20 Pro Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340129 MMWEBSDK/20250201 MMWEBID/6119 MicroMessenger/8.0.60.2860(0x28003C53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxc9cf7c95499ee604',
        'X-Requested-Width': 'com.tencent.mm',
        '$X-YH-Biz-Params': 'ncjkdy=,Q)H&nzggzmdy=(&xdotdy=\\\\u0021&gib=--,0+__-)\\\\u0021*(\\\\u0021---++&gvo=_\'0--$,+\'*\\\\u0021\'\'\'),(\\\\u0021&vkkdy=yKWHqna(DlqXsuHhk)',
        'X-YH-Context': 'origin=h5&morse=1',
    }
    url = 'https://api.yonghuivip.com/web/marketing/free/trial/issue/prize/landing/page'
    params = (
        ('timestamp', object['timestamp']),
        ('channel', '512'),
        ('platform', 'wechatminiprogram'),
        ('v', '11.6.0.125'),
        ('app_version', '11.6.0.125'),
        ('appid', 'wxc9cf7c95499ee604'),
        ('wechatunionid', object['wechatunionid']),
        ('deviceid', object['deviceid']),
        ('sellerid', '7'),
        ('cityid', '4'),
        ('shopid', object['shopid']),
        ('channelSub', ''),
        ('brand', object['brand']),
        ('model', object['model']),
        ('os', object['os']),
        ('osVersion', object['osVersion']),
        ('networkType', 'wifi'),
        ('screen', object['screen']),
        ('productLine', 'YhStore'),
        ('jysessionid', object['jysessionid']),
        ('appType', 'h5'),
        ('access_token', object['access_token']),
    )
    params_dict = {key: value for key, value in params}
    sign = get_sign(params_dict)
    params_dict['sign'] = sign
    query_string = urlencode(params_dict)
    full_url = f"{url}?{query_string}"
    response = requests.request("GET", full_url, headers=headers)
    try:
        data = response.json().get('data', {})
        currTab = data.get('currTab', {})
        signUpStartAt = int(currTab.get('signUpStartAt', 0))
        signUpEndAt = int(currTab.get('signUpEndAt', 0))
        print(
            f"[试用任务] 活动时间: {datetime.datetime.fromtimestamp(signUpStartAt / 1000).strftime('%Y-%m-%d %H:%M:%S')} 至 {datetime.datetime.fromtimestamp(signUpEndAt / 1000).strftime('%Y-%m-%d %H:%M:%S')}")

        landingPagePrizeVOList = currTab.get('landingPagePrizeVOList', [])
        if not landingPagePrizeVOList:
            print("[试用任务] 未找到可报名的试用商品")
            return

        for item in landingPagePrizeVOList:
            prizeId = item.get('prizeId', '')
            skuTitle = item.get('skuTitle', '')
            skuPrice = item.get('skuPrice', 0)
            memberLvDesc = item.get('memberLvDesc', '')
            buttonState = item.get('buttonState', 0)

            product_info = f"[试用任务] 商品: {skuTitle} (价格: ¥{skuPrice}, 要求: {memberLvDesc}) - "

            if buttonState == 1:
                result = ApplyFree(account_url, prizeId)
                if result == "报名成功":
                    print(f"{product_info}成功")
                else:
                    print(f"{product_info}{result}")
            elif buttonState == 2:
                print(f"{product_info}已报名")
            else:
                print(f"{product_info}不可报名")
            time.sleep(1)
    except Exception as e:
        print(f"[试用任务] 解析失败: {str(e)}")


def ApplyFree(account_url, prizeId):
    object = extract_url_params(account_url)
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://m.yonghuivip.com',
        'Referer': 'https://m.yonghuivip.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Redmi K20 Pro Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340129 MMWEBSDK/20250201 MMWEBID/6119 MicroMessenger/8.0.60.2860(0x28003C53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxc9cf7c95499ee604',
        'X-Requested-With': 'com.tencent.mm',
        '$X-YH-Biz-Params': 'ncjkdy=,Q)H&nzggzmdy=(&xdotdy=\\\\u0021&gib=--,0+__-)\\\\u0021*(\\\\u0021---++&gvo=_\'0--$,+\'*\\\\u0021\'\'\'),(\\\\u0021&vkkdy=yKWHqna(DlqXsuHhk)',
        'X-YH-Context': 'origin=h5&morse=1',
    }
    url = 'https://api.yonghuivip.com/web/marketing/free/trial/sign/up/fire'
    params = (
        ('timestamp', object['timestamp']),
        ('channel', '512'),
        ('platform', 'wechatminiprogram'),
        ('v', '11.6.0.125'),
        ('app_version', '11.6.0.125'),
        ('appid', 'wxc9cf7c95499ee604'),
        ('wechatunionid', object['wechatunionid']),
        ('deviceid', object['deviceid']),
        ('sellerid', '7'),
        ('cityid', '4'),
        ('shopid', object['shopid']),
        ('channelSub', ''),
        ('brand', object['brand']),
        ('model', object['model']),
        ('os', object['os']),
        ('osVersion', object['osVersion']),
        ('networkType', 'wifi'),
        ('screen', object['screen']),
        ('productLine', 'YhStore'),
        ('jysessionid', object['jysessionid']),
        ('appType', 'h5'),
        ('access_token', object['access_token']),
    )
    params_dict = {key: value for key, value in params}
    sign = get_sign(params_dict)
    params_dict['sign'] = sign
    query_string = urlencode(params_dict)
    full_url = f"{url}?{query_string}"
    payload = {
        "prizeId": prizeId
    }
    response = requests.request("POST", full_url, data=json.dumps(payload), headers=headers)
    resp_data = response.json()
    if resp_data.get('code') == 0:
        return "报名成功"
    elif resp_data.get('code') == 2003:
        return "已报名"
    else:
        return resp_data.get('message', '未知错误')


def ListAllTasks(account_url):
    print("\n[每日任务] 开始执行每日任务...")
    object = extract_url_params(account_url)
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://m.yonghuivip.com',
        'Referer': 'https://m.yonghuivip.com/',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Redmi K20 Pro Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.136 Mobile Safari/537.36 XWEB/1340129 MMWEBSDK/20250201 MMWEBID/6119 MicroMessenger/8.0.60.2860(0x28003C53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram/wxc9cf7c95499ee604',
        'X-Requested-With': 'com.tencent.mm',
        '$X-YH-Biz-Params': 'ncjkdy=,Q)H&nzggzmdy=(&xdotdy=\\\\u0021&gib=--,0+__-)\\\\u0021*(\\\\u0021---++&gvo=_\'0--$,+\'*\\\\u0021\'\'\'),(\\\\u0021&vkkdy=yKWHqna(DlqXsuHhk)',
        'X-YH-Context': 'origin=h5&morse=1',
    }
    url = 'https://api.yonghuivip.com/web/member/task/listAllTasks'
    params = (
        ('timestamp', object['timestamp']),
        ('channel', '512'),
        ('platform', 'wechatminiprogram'),
        ('v', '11.6.0.125'),
        ('app_version', '11.6.0.125'),
        ('appid', 'wxc9cf7c95499ee604'),
        ('wechatunionid', object['wechatunionid']),
        ('deviceid', object['deviceid']),
        ('sellerid', '7'),
        ('cityid', '4'),
        ('shopid', object['shopid']),
        ('channelSub', ''),
        ('brand', object['brand']),
        ('model', object['model']),
        ('os', object['os']),
        ('osVersion', object['osVersion']),
        ('networkType', 'wifi'),
        ('screen', object['screen']),
        ('productLine', 'YhStore'),
        ('jysessionid', object['jysessionid']),
        ('appType', 'h5'),
        ('access_token', object['access_token']),
    )
    params_dict = {key: value for key, value in params}
    sign = get_sign(params_dict)
    params_dict['sign'] = sign
    query_string = urlencode(params_dict)
    full_url = f"{url}?{query_string}"
    payload = {
        "businessCode": "membershipSystem",
        "shopId": object['shopid'],
        "isOpenPublishNotice": "false"
    }
    response = requests.request("POST", full_url, data=json.dumps(payload), headers=headers)
    try:
        tasks = response.json().get('data', {}).get('subTasks', [])
        taskCode = response.json().get('data', {}).get('taskCode', '')

        for task in tasks:
            taskName = task.get('taskPoint', {}).get('taskTypeName', '未知任务')
            status = task.get('doTaskStatus', 0)
            taskId = task.get('taskId', '')

            print(f"[每日任务] 发现任务: {taskName} - ", end='')

            if status == 1:
                result = DOTask(account_url, taskId, taskCode)
                print(result)
            elif status == 2:
                print("已完成")
            else:
                print("不可执行")
            time.sleep(1)
    except Exception as e:
        print(f"[每日任务] 解析失败: {str(e)}")


def process_account(account_url, index):
    print(f"\n{'=' * 40}")
    print(f"开始执行账号 #{index + 1}")
    print(f"{'=' * 40}")

    # 执行每日任务
    ListAllTasks(account_url)
    time.sleep(2)

    # 执行试用任务
    FreeList(account_url)
    time.sleep(2)

    # 创建队伍
    teamCode = CreateTeam(account_url)

    return teamCode


def main():
    # 从环境变量获取账号
    accounts = os.environ.get('YHSH', '').split('\n')
    accounts = [acc.strip() for acc in accounts if acc.strip()]

    if not accounts:
        print("未找到有效的账号信息，请检查环境变量YHSH")
        return

    print(f"共找到 {len(accounts)} 个账号")

    team_codes = []

    # 第一轮：所有账号执行任务并创建队伍
    for idx, account_url in enumerate(accounts):
        try:
            teamCode = process_account(account_url, idx)
            if teamCode:
                team_codes.append(teamCode)
            time.sleep(3)
        except Exception as e:
            print(f"账号 #{idx + 1} 执行失败: {str(e)}")

    # 第二轮：所有账号加入所有队伍
    if team_codes:
        print("\n" + "=" * 40)
        print("开始组队任务")
        print("=" * 40)

        for team_code in team_codes:
            for idx, account_url in enumerate(accounts):
                try:
                    print(f"\n账号 #{idx + 1} 正在加入队伍 {team_code}...")
                    JoinTeam(account_url, team_code)
                    time.sleep(2)
                except Exception as e:
                    print(f"加入队伍失败: {str(e)}")
            time.sleep(3)


if __name__ == '__main__':
    main()