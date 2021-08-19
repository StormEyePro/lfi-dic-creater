# lfi-dic-creater文件包含漏洞字典生成工具

## php文件包含漏洞原理讲解

https://blog.csdn.net/u013797594/article/details/118865974

参考文章中关于PHP文件包含漏洞的讲解，只写了http、file、compress、php://filter伪协议的绕过。其他的伪协议需要结合文件上传、post提交等方式，因此需要手工测试。

## 字典生成工具

使用条件：

python3 +windows

## 安装

pip3 install -r requirement.txt

### 打包成exe:

#这种方式打包出来运行速度比较快，-F打包的运行起来可能很慢

pyinstaller -c lfi_gui.py --noconsole   

打包后把config、tmp、xuyaode  这三个文件夹放到生成的目录里面。

## 介绍

运行lfi_gui.py，是一个图像工具

![image-20210819150925813](https://gitee.com/dd123456yybb/img/raw/master/image-20210819150925813.png)

config目录中放了配置文件

![image-20210718011000124](https://gitee.com/dd123456yybb/img/raw/master/image-20210718011000124.png)

static_dic目录中的文件是静态字典，可以自己去添加，一般没啥用，生成的字典数量太多。

![image-20210718011028999](https://gitee.com/dd123456yybb/img/raw/master/image-20210718011028999.png)

## 工具原理

![image-20210819151104547](https://gitee.com/dd123456yybb/img/raw/master/image-20210819151104547.png)



1.目录层将输入的文件名添加上../    ../../这样的上级目录，将结果存入集合1。

2.目前可选http/file/compress/php伪协议，选择后按照config/bypassdic1.txt中对应规则替换存入集合2，并将结果与集合1并集

3.可选去后缀、双写、大小写 绕过方式，选择后按照config/bypassdic2.txt中对应规则替换存入集合3，并将结果与集合2、集合1并集。

4.可选去“后缀绕过”，选择后按照config/bypassdic3.txt中对应规则替换存入集合4，并将结果与集合3、集合2、集合1并集。



