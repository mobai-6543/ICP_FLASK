import re

import requests
import urllib3
import json
import time
import hashlib
import base64
import ujson
import random
import os
import ddddocr

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ICP:
    def __init__(self):
        self.auth_data = None
        self.cookie = None
        self.cookie_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32'}
        self.home = 'https://beian.miit.gov.cn/'
        self.url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth'
        # self.getCheckImage = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage'
        self.getCheckImage = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImagePoint'
        self.checkImage = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/checkImage'
        # 正常查询
        self.queryByCondition = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'
        # 违法违规域名查询
        self.blackqueryByCondition = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/blackListDomain/queryByCondition'
        # 违法违规APP,小程序,快应用
        self.blackappAndMiniByCondition = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/blackListDomain/queryByCondition_appAndMini'
        self.p_uuid = ''
        self.token = ''
        self.clientUid = ''
        self.clientUid_data = ''
        self.try_again = 5
        # self.exdir()
        self.DEBUG = False

    def debugprint(self, output):
        if self.DEBUG:
            print("DEBUG：" + str(output))

    @staticmethod
    def exdir():
        base_img_path = 'assets/img'
        os.makedirs(base_img_path, exist_ok=True)
        os.makedirs(f'{base_img_path}/big', exist_ok=True)
        os.makedirs(f'{base_img_path}/small', exist_ok=True)

    def _init_session(self):
        """
           初始化一个同步的 requests 会话
           """
        self.session = requests.Session()
        self.session.trust_env = False  # 禁用从系统环境读取代理配置
        # 如果需要忽略 SSL 验证，可以加上 verify=False
        self.session.verify = False
        # 添加默认的 headers 或其他配置
        self.session.headers.update({
            "User-Agent": self.cookie_headers['User-Agent'],
        })

    def close_session(self):
        if self.session:
            self.session.close()

    def get_token(self):
        timeStamp = round(time.time() * 1000)
        authSecret = 'testtest' + str(timeStamp)
        authKey = hashlib.md5(authSecret.encode(encoding='UTF-8')).hexdigest()
        self.auth_data = {'authKey': authKey, 'timeStamp': timeStamp}
        self.cookie = self.get_cookie() # 没什么用
        self.base_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
            'Origin': 'https://beian.miit.gov.cn',
            'Referer': 'https://beian.miit.gov.cn/',
            # 'Cookie': f'__jsluid_s={self.cookie}',
            'Accept': 'application/json, text/plain, */*'
        }
        try:
            with self.session.request(method="POST", url=self.url, data=self.auth_data, headers=self.base_header) as req:
                req = req.text
                t = ujson.loads(req)
                self.debugprint(t)
                return t['params']['bussiness']
        except Exception as e:
            return e

    def get_cookie(self):
        with self.session.request(method="GET", url=self.home, headers=self.cookie_headers) as req:
            self.debugprint(req.cookies)
            jsluid_s = re.compile('[0-9a-z]{32}').search(str(req.cookies))[0]

            return jsluid_s

    # 新增的UID加密生成算法
    def get_clientUid(self):
        characters = "0123456789abcdef"
        unique_id = ['0'] * 36

        for i in range(36):
            unique_id[i] = random.choice(characters)

        unique_id[14] = '4'
        unique_id[19] = characters[(3 & int(unique_id[19], 16)) | 8]
        unique_id[8] = unique_id[13] = unique_id[18] = unique_id[23] = "-"

        point_id = "point-" + ''.join(unique_id)

        return ujson.dumps({"clientUid": point_id})

    def get_img(self):
        length = str(len(str(self.clientUid_data).encode('utf-8')))
        self.base_header.update({'Content-Length': length, 'Token': self.token})
        self.base_header['Content-Type'] = 'application/json'
        with self.session.request(method="POST", url=self.getCheckImage, data=self.clientUid_data, headers=self.base_header) as req:
            response = req.json()
            self.debugprint(response)
            self.p_uuid = response['params']['uuid']
            big_image = response['params']['bigImage']
            small_image = response['params']['smallImage']

            # # 保存大图
            # with open(f"./img/big/a-{tid}-{str(i)}.jpg", "wb") as big_img_file:
            #     big_img_file.write(base64.b64decode(big_image))
            #
            # # 保存小图
            # with open(f"./img/small/a-{tid}-{str(i)}.jpg", "wb") as small_img_file:
            #     small_img_file.write(base64.b64decode(small_image))
            # print(f"已获取{str(i)}张验证码")
        return big_image, small_image

    def check_img(self, big_image, small_image):
        try:
            big_bytes = base64.b64decode(big_image)
            small_bytes = base64.b64decode(small_image)
            
            # 使用 ddddocr 进行滑块缺口识别
            ocr = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
            res = ocr.slide_match(small_bytes, big_bytes, simple_target=True)
            
            if not res or 'target' not in res:
                return {"code": 101, "msg": "滑块缺口识别失败"}
                
            # x_offset 为缺口 X 坐标
            x_offset = res['target'][0]
            
            data = {
                "key": self.p_uuid,
                "value": str(x_offset)
            }
            
            # 交由 requests 自动计算和设置正确的 Content-Length
            if 'Content-Length' in self.base_header:
                del self.base_header['Content-Length']
                
            with self.session.request(method="POST", url=self.checkImage, json=data, headers=self.base_header) as req:
                resp_data = req.json()
                if not resp_data.get("success"):
                    self.debugprint(f"验证码识别失败 {resp_data}")
                    return {"code": 104, "msg": "验证码识别失败"}
                
                # 兼容不同返回格式：有些版本 params 内含 sign 字典，有些直接就是 sign 字符串
                params = resp_data.get("params", {})
                sign = params.get("sign", "") if isinstance(params, dict) else params
                return {"code": 200, "data": sign}
        except Exception as e:
            self.debugprint(f"滑块验证异常: {e}")
            return {"code": 103, "msg": f"滑块验证异常: {e}"}

    def get_beian(self, sign, domain):
        info = {'pageNum': '', 'pageSize': '', 'unitName': domain, "serviceType": 1}
        # 验证码识别成功，获取数据
        length = str(len(str(ujson.dumps(info, ensure_ascii=False)).encode('utf-8')))
        self.base_header.update({'Content-Length': length, 'Uuid': self.p_uuid, 'Token': self.token, 'Sign': sign})
        with self.session.request(method="POST", url=self.queryByCondition, data=ujson.dumps(info, ensure_ascii=False),
                                  headers=self.base_header) as req:
            res = req.text
            return ujson.loads(res)

    def main(self, domain):
        for i in range(self.try_again):
            self._init_session()
            try:
                # 获取验证码前的参数
                self.token = self.get_token()
                self.clientUid_data = self.get_clientUid()
                self.clientUid = ujson.loads(self.clientUid_data)["clientUid"]

                # 获取并且识别验证码
                big_image, small_image = self.get_img()
                sign = self.check_img(big_image, small_image)

                if sign["code"] != 200:
                    self.debugprint(f"尝试 {i+1} 失败: {sign['msg']}")
                    continue
                
                sign = sign["data"]
                # 获取数据
                data = self.get_beian(sign, domain)
                if data['code'] == 500:
                    self.debugprint(f"尝试 {i+1} 失败: 工信部服务器异常")
                    continue
                
                print(data)
                return data
            except Exception as e:
                self.debugprint(f"尝试 {i+1} 异常: {str(e)}")
                continue
            finally:
                self.close_session()
        
        return {"code": 104, "msg": "验证码识别多次失败，请稍后再试"}


if __name__ == '__main__':
    start = time.time()

    a = ICP()
    a.main("qq.com")

    end = time.time()
    print(end - start)
