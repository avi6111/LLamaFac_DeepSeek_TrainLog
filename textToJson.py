import json
import os
import sys
# 一行代码，三行备注！！！！，备注都写这里了，另外的小代码就不提供备注了
"""原代码基础上，已经尽量（力）改了一些代码；让代码更“健壮”适配性更强；
所以一定的代码“迭代”能力还是必须的；
而且，又碰到坑了，当然每次我都要请至少有“亿点点”经验同事才能解决以下的中文编码读取问题；
（其中文问题每个python程序员都碰过，但每个都不说，其实多年前看过这个文章（最终解）https://zhuanlan.zhihu.com/p/403014557）
这次也只能我自己改了，花了很多时间+功夫；
如果你也有“亿点点”的代码水平，应该能从下面代码看出我改了些什么，除了编码，逻辑，“结构”应该也改了一点点；
(功能：读取 《中文.txt》需配合郭老，的对话文本.txt)
用的方法：命令行>python textToJson.py "tokens-data/crosstalk/郭德纲 樊光耀相声《这一夜两岸说相声》文本.txt"
另外依赖：
- 需要安装chardet，检测文件真正编码
"""
# 需安装 chardet：pip install chardet
import chardet

def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read(1000)  # 读取部分内容检测编码
        result = chardet.detect(raw_data)
        return result["encoding"]

txtPath = "E:/AiChatdata/tokenWithMao.txt"
#jsonPath = os.path.join((os.path.splitext(txtPath)[0]+'.json'))#TMD,这段原代码，还是写错了吧？？
jsonPath = os.path.splitext(txtPath)[0]+'.json'
#sp1 = "对话A"
#sp2 = "对话B"
sp1 = "逗"# 郭德纲 樊光耀相声《这一夜两岸说相声》文本.txt"
sp2 = "捧"# 郭德纲 樊光耀相声《这一夜两岸说相声》文本.txt"
script_dir = os.path.dirname(os.path.abspath(__file__))
def read_txt(path):
    encoding = detect_encoding(path)
    print(f"检测到编码：{encoding}")
    #GB2321，和utf-8都能读到文件，虽然有错；gbk??不行？？？
    #encodings = ["gbk","GB2312","utf-8", "gb18030", "latin-1", "iso-8859-1"]
    encodings = ["utf-8", "gb18030", "latin-1", "iso-8859-1"]#本来需要做一个编码自动判断的，但现在代码乱了 这里没做逻辑处理，现在：强行第一个执行的就是 utf-8
    #with open(path, 'r', encoding='utf-8') as f:
    for encoding in encodings:
        #with open(path, 'r') as f:
        with open(path, 'r',encoding=encoding) as f:
            #简单点，现在直接先“物理上，人为的”把.txt先改成utf-*编码；另外再提供一个“代码”以判断和转换 utf-8
            #所以这里是否有encoding 不重要了，参数传不传都可以
        
            lines = f.readlines()
            print('测试，（这DeepSeek给的实现）读取到 Encoding = ' + encoding)
            break

        

    tokenlog_list = []
    prev_speaker = None
    prev_line = None

    for line in lines:
        line = line.strip()#有做空格截断（本来的代码），但有没有更好的处理代码？
        if line.startswith(sp1) or line.startswith(sp2):
            #current_speaker = line.split("：")[0]
            #current_content = line.split("：")[1]
            strs = line.split("：")
            speaker = strs[0]
            content = "".join(strs[1:])

            if prev_speaker ==sp2:
                tokenlog_list.append((prev_line, content))#现在这逻辑，只能处理 1.单行对话，不能连续或者多行；2.一对一的对话，必须一问一答
            
            prev_speaker = speaker
            prev_line = content
    
    return tokenlog_list
# def changeToUTf8(s):# 没用的方法了；测试过，踩过坑，才知道：这种‘传统’处理代码，就算转对了编码 ，后面输出： json.dump(all_data, 会有问题的。。。。；
#     #u = f.decode('gb2312') #以文件保存格式对内容进行解码，获得unicode字符串
#     return s.encode('utf-8')
def save_json(tokenlog_list, jsonPath):
    all_data = []  
    for idx,tokens in enumerate(tokenlog_list):
        tokenA, tokenB = tokens #因为我用cmd测试比较多（中文gb2321环境），前面read()的时候，已经是Unicode(gb2321)，所以这里直接能读中文了，（下面测试一次：也能测出）
        #tokenA = changeToUTf8(tokenA)
        #tokenB = changeToUTf8(tokenB)
        
        if(idx==0):
            print('测试一次中文：',tokenA,tokenB)
        data = {
            "instruction": tokenA,
            "input": "",
            "output": tokenB
        }
        all_data.append(data) 

    with open(jsonPath, 'w', encoding='utf-8-sig') as f:
    #with open(jsonPath, 'w', encoding='utf-8') as f:
    #with open(jsonPath, 'w',encoding='GB2312') as f:#？？？？none, no Done!!!
        #json.dump(all_data, f,indent=4,ensure_ascii=True) #errro0,ensure_ascii 不知道的参数，就不要用，测试过，也解决不了编码和调试（开发）环境的问题。。
        json.dump(all_data, f,indent=4,ensure_ascii=False) # errro1,前面的gb2321读取解决了，这里才有用：ensure_ascii=False；前面中文读取错了，乱了，这个参数并没有用的；
                                                    # json.dump() 本身的问题
                                                    # 这个参数，就是json.dump()方法的一个别扭的处理方法，all_data本身编码是对的，非要再转unicode，
                                                    # 传这个参数，就是要json.dump（）不要转//和前面的encode decode处理冲突的。。。
        #json.dump(all_data, f, indent=4) #error2,必须：ensure_ascii=False?

def main_processdir(folder,dest):
    """.folder(src) 尽量不要有子目录"""
    for root,dirs,files in os.walk(folder):
        for file in files:
            txtPath = os.path.join(root,file)
            jsonPath = os.path.join(dest,os.path.splitext(file)[0]+'.json')
            list = read_txt(txtPath)
            save_json(list, jsonPath)  
        print(f'saved to dest={jsonPath} total={len(files)}')      
    
def main(filePath):
    """暂时只处理相对路径 filePath"""
    if(filePath!=None):
        txtPath = script_dir+"/"+filePath
        jsonPath = os.path.join((os.path.splitext(txtPath)[0]+'.json'))
    list = read_txt(txtPath)
    save_json(list, jsonPath)
    print("生成Json:"+jsonPath)

#还是写一个 main 吧，原代码，居然连 main 都不写。。。。
# 越写越多了，基本上，个人写，都很少会是单一功能的.py
#传一个参数，直接同目录转出一个.json文件
#传两个参数，src目录，输出到 dest目录
if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args)>1:
        main_processdir(args[0],args[1])
    elif(len(args)>0):
        main(args[0])
    else:
        main()
    