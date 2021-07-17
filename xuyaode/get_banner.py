
import chardet
import requests,re
import os
from threading import Thread,activeCount
from sys import argv
from queue import Queue
from xml.dom.minidom import parse

requests.packages.urllib3.disable_warnings()
new_targets = []

class get_banner():
    def __init__(self):
        print('init get_banner')
        self.n=0
        self.result=''
        banner_xml=os.path.dirname(os.path.realpath(__file__))+'/banner.xml'
        with open(banner_xml,'r',encoding='utf-8') as f:
            f.read()
        requests.packages.urllib3.disable_warnings()
        self.proxy={
            'http':'http://127.0.0.1:8080',
            'https':'http://127.0.0.1:8080'
        }
        self.proxy=False
        self.header={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept': '*/*'
        }
        print('init get_banner end')



    def read_xml_root_node(self,xml_path):
        dom = parse(xml_path)
        root = dom.documentElement
        return root

    def read_child_label(self,node, label_name):
        child = node.getElementsByTagName(label_name)
        return child

    def read_attribute(self,node, attr_name):
        attribute = node.getAttribute(attr_name)
        return attribute

    def response_value(self,response,fun):
        try:
            a=getattr(response,fun)
        except:
            print('response no such fun:',fun)


        return  a

    def re_compare(self,name,re_value,response,location,value):
        n=0
        name_l=[]
        for re_v in re_value:
            n+=1
            try:
                v = re.compile(str(re_v),re.I).search(str(self.response_value(response, location)))
                # print('1111111111111111111111',re_value,location)
                # print(str(self.response_value(response, location)))
                # print('------------end----------')
            except:
                v = False
                print('[error] re.search error')

            if value == 'yes':
                try:
                    name = v.group()
                except:
                    pass
            value = ''

            if v:
                print('match[', name, ']rule:', re_v)
                name=name
            else:
                name=''
            name_l.append(name)

        if len(set(name_l))==1:
            name=name_l[0]
        else:
            name=''

        return name

    def my_banner(self,response,target):

        rootNode=self.read_xml_root_node('banner.xml')
        # print(rootNode.nodeName)
        childNodes=self.read_child_label(rootNode,"banner")
        re_name=set()
        re_send_url_set=set()
        for child in childNodes:
            name=self.read_attribute(child,"name")
            location = self.read_attribute(child, "location")
            value=self.read_attribute(child, "value")
            re_values=child.getElementsByTagName('re_value')
            re_value=[]
            n=0
            for i in re_values:
                # print('??')
                re_value.append(re_values[n].childNodes[0].nodeValue)
                n += 1

            # print('----start---')
            # print(re_values)
            # print('----end-----')
            # print()
            re_send_url=self.read_attribute(child, "send_url")
            if re_send_url:
                re_send_url_set.add(str(re_send_url))

            #第一次比较

            resu = self.re_compare(name, re_value, response, location, value)
            if resu:
                re_name.add(resu)

        #根据banner.xml中定义的send_url发送request，再对返回包进行一次re指纹识别，send_url的request会在其他匹配执行完成后再执行，否则会扰乱乱来的响应包。
        # try:
        #     for re_send_url in re_send_url_set:
        #         target=target+re_send_url
        #
        #         response=requests.get(target,verify=False,headers=self.header,timeout=(5,20))
        #         resu=self.re_compare(name,re_value,response,location,value)
        #         if resu:
        #             re_name.add(resu)
        # except:
        #     print('[error] second send request error,target:',target)
        # finally:
        #     re_send_url=''

        return str(re_name)

    def get_result(self):
        return self.result

    def get_banner(self,url):
        if not re.match(r'http|https',url): #判断有无协议
            target = 'https://' + url.strip()
            try:
                requests.get(target,verify=False,headers=self.header,timeout=(5,20),proxies=self.proxy)
            except:
                print('not https')
                target='http://' + url.strip()
        else:
            target=url.strip()

        try:
            req = requests.get(target,verify=False,headers=self.header,timeout=(5,20),proxies=self.proxy)  #allow_redirects=False
            if 'charset' not in req.headers.get('Content-Type', " "):
                req.encoding = chardet.detect(req.content).get('encoding')  # 解决网页编码问题
            code = req.status_code

            if '30' in str(code):
                if req.headers['Location'] == 'https://' + target.strip('http://') + '/':
                    req_30x = requests.get('https://{}'.format(target.strip('http://')),verify=False,headers=self.header,timeout=(5,20),proxies=self.proxy)
                    code_30x = str(req_30x.status_code).strip()
                    if 'charset' not in req_30x.headers.get('Content-Type', " "):
                        req_30x.encoding = chardet.detect(req_30x.content).get('encoding')  # 解决网页编码问题
                    try:
                        title_30x = re.findall(r'<title>(.*?)</title>',req_30x.text,re.S)[0].strip()
                    except:
                        title_30x = 'None'
                    try:
                        mybanner = self.my_banner(req,target)
                    except:
                        mybanner = ''

                    if 'Server' in req_30x.headers:
                        server_30x = req_30x.headers['Server'].strip()
                    else:
                        server_30x = ''
                    if 'Content-Type' in req_30x.headers:
                        type_30x = req_30x.headers['Content-Type'].strip()
                    else:
                        type_30x = ''
                    if 'X-Powered-By' in req_30x.headers:
                        x_powered_by_30x = req_30x.headers['X-Powered-By'].strip()
                    else:
                      x_powered_by_30x = ''

                    print('[+] {} {} {} {} {} {} {}'.format(mybanner,code_30x,target,title_30x,server_30x,type_30x,x_powered_by_30x))
                    self.result='[+] {} {} {} {} {} {} {} '.format(mybanner,code_30x,target,title_30x,server_30x,type_30x,x_powered_by_30x)
                else:
                    title = '302_redirection'
                    location = req.headers['Location']
                    try:
                        mybanner = self.my_banner(req,target)
                    except:
                        mybanner = ''

                    print('[+] {} {} {} Location：{} {}'.format(mybanner,code,target,title,location))
                    self.result='[+] {} {} {} Location：{} {}'.format(mybanner,code,target,title,location)
            else:
                try:
                    title = re.findall(r'<title>(.*?)</title>',req.text,re.S)[0].strip()
                except:
                    title = 'None'
                try:
                    mybanner=self.my_banner(req,target)
                except:
                    mybanner=''

                if 'Server' in req.headers:
                    server = req.headers['Server'].strip()
                else:
                    server = ''
                if 'Content-Type' in req.headers:
                    type = req.headers['Content-Type'].strip()
                else:
                    type = ''
                if 'X-Powered-By' in req.headers:
                    x_powered_by = req.headers['X-Powered-By'].strip()
                else:
                    x_powered_by = ''

                print('[+] {} {} {} {} {} {}'.format(mybanner,code,target,title,server,x_powered_by))
                self.result='[+] {} {} {} {} {} {}'.format(mybanner,code,target,title,server,x_powered_by)

        except Exception as e:
            print('[-]Error {} {} '.format(target,str(e)))
            self.result = '[error]'
        finally:

            return  self.get_result()

if __name__ == '__main__':
    try:
        url='http://47.92.29.189:8085/login'

        x=get_banner().get_banner(url)
        # print(x)

    except IndexError:
        print('Usage：python3 get_banner.py urls.txt new_urls.txt')