import requests
from lxml import etree
import pymysql


class Spyder(object):
    def __init__(self, query="2024年4月24日"):
        # 初始化数据
        self.query = query
        self.data_list = []

        self.headers1 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Referer": "https://weixin.sogou.com/weixin?type=2&s_from=input&query=2025%E5%B9%B43%E6%9C%8824%E6%97%A5&ie=utf8&_sug_=y&_sug_type_=&w=01019900&sut=2218&sst0=1742786560666&lkt=1%2C1742786559763%2C1742786559763",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0",
            "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Microsoft Edge\";v=\"134\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        self.cookies1 = {
            "_qimei_uuid42": "1930a0d311510095dc91490d860870e7782260cac7",
            "_qimei_fingerprint": "072165d2177b1ef2f7789b04f382e6d9",
            "_qimei_q36": "",
            "_qimei_h38": "fded39a6dc91490d860870e70200000431930a",
            "ABTEST": "1|1742779732|v1",
            "SUID": "F496FA713954A20B0000000067E0B554",
            "IPLOC": "CN5000",
            "SUV": "00302F6A71FA96F467E0B5585B9CE810",
            "SNUID": "F695F9730305330E8A0801F303376CFC",
            "ariaDefaultTheme": "undefined"
        }
        self.url1 = "https://weixin.sogou.com/weixin"
        self.params1 = {
            "type": "2",
            "s_from": "input",
            "query": self.query,
            "ie": "utf8",
            "_sug_": "y",
            "_sug_type_": "",
            "w": "01019900",
            "sut": "1547",
            "sst0": "1742786647190",
            "lkt": "2,1742786646771,1742786647088"
        }

        # 定义的参数
        self.title = ""
        self.url = ""
        self.content = ""

        # 连接数据库

    def get_url1(self):
        """
        :return:
        """
        response = requests.get(url=self.url1, headers=self.headers1, cookies=self.cookies1, params=self.params1)
        html = etree.HTML(response.text)
        data_list = html.xpath('//ul[@class="news-list"]/li/div[2]')
        for data in data_list:
            list_now = []
            self.title = data.xpath('string(./h3/a/text())')
            self.url = data.xpath('string(./h3/a/@href)')
            self.content = "".join(data.xpath('./p//text()'))
            list_now.append(self.title)
            list_now.append(self.url)
            list_now.append(self.content)
            self.data_list.append(list_now)

    def save_data(self):
        pass

    def run(self):
        """主程序"""
        self.get_url1()
        return self.data_list


if __name__ == '__main__':
    spPro = Spyder()
    spPro.run()
