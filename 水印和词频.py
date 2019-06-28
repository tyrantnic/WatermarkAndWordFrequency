from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog
from PIL import Image, ImageDraw,ImageFont
import numpy as np
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pylab import mpl

def add_wordmark(): # 用于添加可视水印的函数
    markword = e2.get() # 从相应的输入框获取信息
    picture = e1.get()
    newpicture = "加可视水印.png"
    im = Image.open(picture).convert('RGBA')# 打开图片
    txt=Image.new('RGBA', im.size, (0,0,0,0))# 新建一个尺寸与打开图片一样的空白图片
    fnt=ImageFont.truetype("c:/Windows/Fonts/msyh.ttc", 28)# 设置字体为微软雅黑,大小为28
    d=ImageDraw.Draw(txt)# 将新建的图片添入画板
    d.text((txt.size[0]-115,txt.size[1]-80), markword,font=fnt, fill=(255,255,255,255))
                                                                                       # 在新建的图片上添加字体
    img_new=Image.alpha_composite(im, txt)# 合并两个图片
    img_new.save(newpicture)

def get_bits(s): #将字符串转换为二进制数的列表
    bs = ''
    for c in s:
        bs += bin(ord(c))[2:].zfill(8)
    return list(bs)

def add_info(): # 用于添加数字睡水印的函数
    info = e3.get()
    picture = e1.get()
    newpicture = "加数字水印.png"
    img = Image.open(picture).convert('RGB')# 读取图片
    pixels = list(img.getdata())#获取图片的像素信息
    bits = get_bits(info)# 将密码信息转换加密字符串
    num = len(pixels)//len(bits)
    fullbits = []
    for i in range(num):
        fullbits +=bits# 将加密字符扩充
    new_pixel_list = []
    for pixel in pixels: # 遍历图片的每个像素
        new_pixel = []
        for c in pixel: # 遍历像素的3个颜色值 
            c = c // 2 * 2 # 取出颜色值二进制数的末位   
            if len(fullbits) > 0: 
                c += int(fullbits.pop(0))# 从加密字符串中取出第一位加在颜色值上
            new_pixel.append(c)
        new_pixel_list.append(tuple(new_pixel)) # 把新的像素值加到列表中
    img_new = Image.new("RGB", img.size) # 创建同样大小的新图片
    img_new.putdata(data=new_pixel_list) # 添加像素值
    img_new.save(newpicture) # 保存图片

def decode_bits(bits_list):#将二进制数转化为字符串
    s = ''
    for bits in bits_list:
        c = chr(int(bits, 2))
        s += c
    return s

def get_info(): # 用于将数字水印解密的函数
    picture = e4.get()
    infofile = "密文内容.txt"
    img = Image.open(picture).convert('RGB')# 读取图片
    pixels = list(img.getdata())# 提取加密图片的像素信息
    bits_list = []
    bits =""
    for pixel in pixels: #遍历所有像素
        for c in pixel:
            bits += str(c % 2)# 获取每个颜色的末位值，并且进行拼接
            if len(bits) == 8:# 对每8个字符为一组进行处理
                bits_list.append(bits)# 添加二进制字符串到列表中
                bits =""
    s = decode_bits(bits_list) #将加密字符解析出密文
    f = open(infofile,"w") #打开文件
    f.write(s)#写入
    f.close()

def get_wordtxt():  #分析文本的函数
    file = e5.get()
    txt = open(file, "r", encoding='gb18030').read() #读的方式打开文本文件，编码格式为gb18030
    words  = jieba.lcut(txt)  #结巴分词
    counts = {} 
    for word in words:
        if len(word) == 1:  #剔除一个字的分词结果
            continue
        else:
            counts[word] = counts.get(word,0) + 1  #按单词统计
    items = list(counts.items())  #转变成列表
    items.sort(key=lambda x:x[1], reverse=True)  #按词频数降序排列
    fo = open("词频结果文本.txt","w+") #覆盖读写模式打开文件.txt
    for i in range(len(items)):  #输出所有高频词
        word, count = items[i]  
        fo.writelines("{0:<10}{1:>5}\n".format(word, count)) #将结果写入.txt文件里
    fo.close()

def get_wordcloud(): # 得到词云的函数
    file = e5.get()
    txt = open(file, "r", encoding='gb18030').read() #读的方式打开文本文件，编码格式为gb18030
    words  = jieba.lcut(txt)  #结巴分词
    wordc = ' '.join(words)  #将分开的词用空格连接，便于生成词云
    font = r'C:\Windows\Fonts\STXINGKA.TTF'#设置字体为华文行楷常规
    wc = WordCloud(font_path=font, #生成词云的一些属性  添加字体路径
               background_color='white',  #设置背景色为白色
               width=1400,  #设置宽1400
               height=1000,  #高1000
               ).generate(wordc)
    wc.to_file("词云.jpg") #保存词云图片为.jpg

#GUI界面实现
win = Tk(className="水印&词频") # 创建主窗口
sw = win.winfo_screenwidth()# 得到屏幕宽度
sh = win.winfo_screenheight()# 得到屏幕高度
ww = 375
wh = 450
x = int((sw-ww) / 2) #让界面显示在屏幕中央
y = int((sh-wh) / 2)
win.geometry("{}x{}+{}+{}".format(ww,wh,x,y))

Label0 = Label(win,text="加水印").grid(row=0,column=1,padx=10,pady=10)
Label1 = Label(win,text="选择原图片:").grid(row=1,column=0,padx=10,pady=5)
Label2 = Label(win,text="输入可视水印:").grid(row=2,column=0,padx=10,pady=5)
Label3 = Label(win,text="输入数字水印:").grid(row=3,column=0,padx=10,pady=5)
Label4 = Label(win,text="获取密文").grid(row=4,column=1,padx=10,pady=10)
Label5 = Label(win,text="选择加密图片:").grid(row=5,column=0,padx=10,pady=5)
Label6 = Label(win,text="文本词频分析").grid(row=7,column=1,padx=10,pady=10)
Label7 = Label(win,text="选择文本:").grid(row=8,column=0,padx=10,pady=5)

e1 = Entry(win,textvariable=StringVar())# 字符串接收框 用来放原图路径
e2 = Entry(win,textvariable=StringVar()) #  可视水印内容
e3 = Entry(win,textvariable=StringVar())#  数字水印内容
e4 = Entry(win,textvariable=StringVar()) #  需解密图片路径
e5 = Entry(win,textvariable=StringVar()) #  需分析文本路径
e1.grid(row=1,column=1,padx=10,pady=5)
e2.grid(row=2,column=1,padx=10,pady=5) 
e3.grid(row=3,column=1,padx=10,pady=5)
e4.grid(row=5,column=1,padx=10,pady=5)
e5.grid(row=8,column=1,padx=10,pady=5)

def select1(): # 实现浏览按钮1的功能
    filename = tkinter.filedialog.askopenfilename()
    if filename != "":
        e1.delete(0,END)
        e1.insert(0,filename)
    
Button(win,text="浏览",width=10,command=select1)\
    .grid(row=1,column=2,padx=10,pady=5)

Button(win,text="添加并生成",width=10,command=add_wordmark)\
    .grid(row=2,column=2,padx=10,pady=5)

Button(win,text="添加并生成",width=10,command=add_info)\
    .grid(row=3,column=2,padx=10,pady=5)

def select2(): # 实现浏览按钮2的功能
    filename = tkinter.filedialog.askopenfilename()
    if filename != "":
        e4.delete(0,END)
        e4.insert(0,filename);
        
Button(win,text="浏览",width=10,command=select2)\
    .grid(row=5,column=2,padx=10,pady=5)

Button(win,text="生成密文本",width=10,command=get_info)\
    .grid(row=6,column=1,padx=10,pady=5)

def select3(): # 实现浏览按钮3的功能
    filename = tkinter.filedialog.askopenfilename()
    if filename != "":
        e5.delete(0,END)
        e5.insert(0,filename);

Button(win,text="浏览",width=10,command=select3)\
    .grid(row=8,column=2,padx=10,pady=5)

Button(win,text="生成词频",width=10,command=get_wordtxt)\
    .grid(row=9,column=1,padx=10,pady=5)

Button(win,text="生成词云图",width=10,command=get_wordcloud)\
    .grid(row=10,column=1,padx=10,pady=5)


win.mainloop()# 进入消息循环
