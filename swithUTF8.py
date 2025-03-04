import os
import sys
import chardet
#调用前必须保证 file 是 gb2321格式，只能 gb2321转 utf-8; 否则一转换就会乱掉；
def switch_gb2312_to_utf8(input_file, output_file):
    try:
        # 读取 GB2312 文件
        #with open(input_file, "r", encoding="gb2312", errors="strict") as f_in:
        #with open(input_file, "r", encoding="gb2312") as f_in:
        with open(input_file,'r',encoding="gb18030") as f_in:#参考自：https://blog.csdn.net/Junkichan/article/details/51913845
            content = f_in.read()
        
        # 写入 UTF-8 文件
        with open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write(content)
        
        print(f"转换成功: {input_file} -> {output_file}")
        return True
    except UnicodeDecodeError as e:
        print(f"转换失败（遇到非法字符）: {e}")
        print("建议使用更全的编码（如 gb18030）重新尝试")
        #if raise_error:raise ValueError(e)
        return False

def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read(1000)  # 读取部分内容检测编码
        result = chardet.detect(raw_data)
        return result["encoding"]   

def main(p):
    total = 0
    alreadyCount = 0
    swtichedCount = 0
    for root,dirs,files in os.walk(p):
        total = len(files)

        for file in files:
            file_path = os.path.join(root, file)
            encode = detect_encoding(file_path)
            if(not (encode.startswith("utf-8") or encode.startswith("UTF-8"))):
                print('Switching....path='+file_path+" encode=" + encode)
                if switch_gb2312_to_utf8(file_path,file_path):
                    swtichedCount+=1
            else:
                alreadyCount+=1
    print(f"Swtich 统计: total={total} ac={alreadyCount} sc={swtichedCount}(DONE!) err={total-alreadyCount-swtichedCount}")
"""
批量转换成 utf-8;
建议先备份，直接转换的，请注意!!
支持调用写法：
python switchUTF8.py -s [文件路径]
python switchUTF8.py -dir [目录]
python switchUTF8.py [目录] """
if __name__ == "__main__":
    args = sys.argv[1:]
    if(len(args)>0):
        if args[0].startswith("-"):
            match args[0]:
                case "-s":
                    encode = detect_encoding(args[1])
                    print("打印 encode ="+ encode)
                    if(encode.startswith("utf-8") or encode.startswith("UTF-8")):
                        print('已经是 utf-8')
                    else:
                        switch_gb2312_to_utf8(args[1],args[1])
                    pass
                case "-dir":
                    main(args[1])#直接整个目录转，同下面默认的逻辑：main(args[0])
                case _:
                    print("no command of ??" + args[0])
        else:
            main(args[0])
            print("Switch Done (by Folder Name)!!")
    else:
        print('至少需要一个参数, usage: python switchUTF8.py [dir]')