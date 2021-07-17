from PyQt5.Qt import QTextEdit,QPushButton,QWidget,QApplication,QThread,pyqtSignal,QComboBox,QLabel
import sys
import sip
import os
import threading
import time
from create_dic import create_dic

class Worker(QThread):
    sinOut = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        #设置工作状态与初始num数值
        self.working = False
        self.num = 0

    def __del__(self):
        #线程状态改变与线程终止
        self.working = False
        self.wait()
        print('销毁')

    def run(self):
        print('run')
        while True:
            time.sleep(2)
            if self.working:
                print('??')
                #获取文本
                file_str = 'File index{0}'.format(self.num)
                self.num += 1
                # 发射信号
                self.sinOut.emit(file_str)
                # 线程休眠2秒
                self.working=False
                self.__del__()






class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('文件包含字典生成')
        self.resize(500, 400)
        self.bt_list=[]
        self.tmp = os.path.dirname(os.path.realpath(__file__)) + '/tmp'
        if not os.path.exists(self.tmp):
            os.mkdir(self.tmp)

        self.response=''
        self.create_dic=create_dic()  #实例化self.create_dic()类
        self.s = set()
        self.txt = set()
        self.result_file=''

        self.base_password='default.txt'
        self.setup_ui()



    def thread_get_banner(self,keys):
        generate_key=''
        self.lable.setText('正在生成字典...')
        generate_keys=self.create_dic.generate_lfi_dic(5,self.base_password,keys)
        # print(generate_keys)
        self.lable.setText('生成字典成功...')
        # for key in generate_keys:
        #     generate_key+=key.strip()+'\n'
        generate_key=''.join(generate_keys)
        # print(generate_key)

        self.response=generate_key
        print(self.response)
        if self.response:
            name=''
            for i in self.usernames.split('\n'):
                name+=i.strip()+','
            name=name.rstrip(',')
            name=name+'_'+self.base_password.rstrip('.txt')
            self.lable.setText('正在写入磁盘...')
            try:
                with open(self.tmp+'/'+str(time.strftime("%m.%d", time.localtime()))+'+{}.txt'.format(name),'w',encoding='utf-8') as f:
                    f.writelines(self.response)
            except:
                with open(self.tmp+'/'+str(time.strftime("%m.%d-%H.%M", time.localtime()))+'.txt','w',encoding='utf-8') as f:
                    f.writelines(self.response)
        self.lable.setText('正在刷新...')
        self.flush.working = True

    def flush_ui(self,response):

        self.result_button()
        self.lable.setText('完成，点击可打开文件')

    def setup_ui(self):


        self.lable=QLabel(self)
        self.lable.resize(150,50)
        self.lable.move(5,1)
        self.lable.setText('')



        ql_b = QTextEdit(self)
        ql_b.move(0, 50)
        ql_b.resize(200,350)
        ql_b.setPlaceholderText("请输入文件名，以换行分割\n例如:\nindex.php\n/etc/passwd\n\n【*】index.php会循环不同右侧下拉列表可选择服务器常用文件名字典-但生成的lfi字典会很大，default.txt内容为空，可自行在config/static_dic中配置")


        self.ql_c = QTextEdit(self)
        # self.ql_c.setText('还需要手工测试的内容：\n1.php://input方式（POST方式）\n2.远程文件包含:http://\n3.上传结合包含利用的zip:// compress.zlib:// compress.bzip2://')
        self.ql_c.move(205, 50)
        self.ql_c.resize(300, 350)



        btn = QPushButton(self)
        btn.setText('go')
        btn.resize(100,40)
        btn.move(150, 10)

        bt2=QComboBox(self)
        bt2.move(250,11)
        bt2.resize(250,38)
        bt2.AdjustToContentsOnFirstShow
        files=os.listdir(os.path.dirname(os.path.realpath(__file__))+'/config/static_dic')
        bt2.addItems(files)
        bt2.setCurrentIndex(-1)

        self.flush=Worker()
        self.flush.sinOut.connect(self.flush_ui)
        self.result_button()

        def go():
            self.result_button()
            self.usernames = ql_b.toPlainText()
            self.flush.start()
            self.flush.working = False
            t=threading.Thread(target=self.thread_get_banner,args=(self.usernames.split('\n'),))
            t.start()

        btn.clicked.connect(go)
        bt2.currentIndexChanged[str].connect(self.print_value)

    def print_value(self,str):
        self.base_password=str


    def fz(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_file)

    def pop_text(self,file):
        os.popen(self.tmp+'/'+file)

    def del_bt(self,file):
        os.remove(self.tmp+'/'+file)
        self.result_button()

    def result_button(self):
        files=os.listdir(self.tmp)

        n=0
        try:
            if self.bt_list:
                print(self.bt_list)
                for bt in self.bt_list:
                    print('删除',bt.text())
                    sip.delete(bt)
                self.bt_list.clear()
                self.bt_list.clear()
        except:
            self.bt_list.clear()

        for file in files:
            size=(os.path.getsize(self.tmp+'/'+file))/1024/1024
            size='%.1fM' % size
            exec('btt{}=QPushButton(self.ql_c)'.format(n))
            exec('btt{}.setText("{}   {}")'.format(n,file,size))
            exec('btt{}.resize(260,40)'.format(n))
            exec('btt{}.move(0,40*{})'.format(n,n))
            exec('btt{}.clicked.connect(partial(self.pop_text,"{}"))'.format(n,file))
            exec('btt{}.show()'.format(n))
            exec('self.bt_list.append(btt{})'.format(n))

            exec('btd{}=QPushButton(self.ql_c)'.format(n))
            exec('btd{}.setText("{}")'.format(n,'删除'))
            exec('btd{}.resize(40,40)'.format(n))
            exec('btd{}.move(260,40*{})'.format(n,n))
            exec('btd{}.clicked.connect(partial(self.del_bt,"{}"))'.format(n,file))
            exec('btd{}.show()'.format(n))
            exec('self.bt_list.append(btd{})'.format(n))


            n += 1




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())