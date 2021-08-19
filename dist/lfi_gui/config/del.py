import re

# l=[]
#
# with open('small.txt','r',encoding='utf-8') as f:
#     for i in f:
#         if not re.search(r'%00',i):
#             l.append(i)
#
# with open('small_dic.txt','a+',encoding='utf-8') as f:
#     for x in l:
#         f.write(x)

win=set()
linux=set()
with open('static_dic/large_dic.txt', 'r', encoding='utf-8') as f:
    for i in f:
        if re.match(r'C:|c:|d:|D:|%SystemDrive%',i):
            print('windows')
            win.add(i)
        else:
            print('linux')
            linux.add(i)

with open('static_dic/windows_large.txt', 'w', encoding='utf-8') as f:
    f.close()
with open('static_dic/linux_large.txt', 'w', encoding='utf-8') as f:
    f.close()
with open('static_dic/windows_large.txt', 'a+', encoding='utf-8') as f:
    for w in win:
        f.write(w)

with open('static_dic/linux_large.txt', 'a+', encoding='utf-8') as f:
    for lin in linux:
        f.write(lin)