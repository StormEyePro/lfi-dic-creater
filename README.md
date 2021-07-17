# lfi-dic-creater文件包含漏洞字典生成工具

## php文件包含漏洞原理讲解

https://blog.csdn.net/u013797594/article/details/118865974

## 字典生成工具

使用条件：

python3 +windows

## 介绍

运行lfi_gui.py，是一个图像工具

![image-20210718012134768](https://gitee.com/dd123456yybb/img/raw/master/image-20210718012134768.png)

config目录中放了配置文件

![image-20210718011000124](https://gitee.com/dd123456yybb/img/raw/master/image-20210718011000124.png)

static_dic目录中的文件是静态字典，可以自己去添加，一般没啥用，生成的字典数量太多。

![image-20210718011028999](https://gitee.com/dd123456yybb/img/raw/master/image-20210718011028999.png)

## 工具原理

根据文件包含漏洞的漏洞原理，将它分为利用姿势和绕过姿势，组合了bypassdic1.txt、bypassdic2.txt、bypassdic3.txt   这3个文件，bypassdic1.txt放入的是文件包含的利用姿势，可自行添加。bypassdic2.txt和bypassdic3.txt放入的是绕过姿势，生成字典按照bypassdic1.txt-》bypassdic2.txt-》bypassdic3.txt的顺序运行。

### 第一步：

如输入flag.php，则会自动添加上相对路径../flag、../../flag等，目前最高添加到8级，可在config.txt中进行修改。如果是/etc/passwd这样的文件则不会添加相对路径。生成的内容加入到字典池。

### 第二步：

第一步及之前生成的所有字典按照bypassdic1.txt的内容进行替换，生成的内容加入到字典池。

根据漏洞原理，对相对路径、绝对路径、data://、file://、http://、compress.zlib、compress.bzip2、php://filter进行爆破。

### 第三步：

第二步及之前生成的所有字典按照bypassdic2.txt的内容进行转换，生成的内容加入到字典池。

进行大小写、双写和去掉后缀处理

### 第四步：

第三步及之前生成的所有字典按照bypassdic3.txt的内容进行转换，生成的内容加入到字典池。

末尾添加%00  ::$data  ./ . /. “  < > + 空格进行绕过。



最后所有的字典池合在一起就是结果。
