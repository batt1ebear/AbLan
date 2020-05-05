# coding=utf-8
#python自动机思想词法分析器
#author:batt1ebear
import sys
import re

keywords = {}   

# 关键字1xx
keywords["for"] = 101
keywords["in"] = 102
keywords["while"] = 103
keywords["true"] = 104
keywords["false"] = 105
keywords["and"] = 106
keywords["or"] = 107
keywords["none"] = 108
keywords["from"] = 109
keywords["not"] = 110
keywords["if"] = 111
keywords["elif"] = 112
keywords["break"] = 113
keywords["import"] = 114
keywords["until"] = 115

def preprocessing(raw):#预处理 去除多余空格
    if raw[-1]!='\n':
        raw+='\n'
    i=0
    while raw[i]==' ' or raw[i]=='\t':
        i+=1
    line = raw[i:]
    return line


def scanner(filename):
    try:
        f_read = open(filename,'r')
        row_counter=1#行数计数器
        while True:

            raw = f_read.readline()
            if not raw:
                print("----scanner completed----")
                break#无字符或者读到跳出

            read = preprocessing(raw)#预处理

            print("ROW "+str(row_counter) + ': ' + read[:-1])#防止显示\n
            length = len(read)#本行长度
            i = -1

            while i <length -1:#length-1 为 行末尾\n
                i += 1
                if read[i] == " ":
                    continue#遇到空格继续状态0
                elif read[i] == "\t":
                    continue#遇到制表符继续状态0
                elif read[i] == "{":
                    bs = i #bufferstart 单词起始位置
                    i += 1
                    while read[i] != "}" :
                        if i+1 >=length-1 :
                            print("  [error]："+read[bs:i+1]+" is illegal , need }")#{没有封闭
                            break
                        i += 1
                    pass#省略注释 注：注释不可跨行
                
                elif read[i] == "+":
                    if read[i+1] == "=":
                        i +=1
                        print("  Speacial character --- +=")
                    else :
                        print("  Speacial character --- +")
                elif read[i] == "-":
                    if read[i+1] == "=":
                        i +=1
                        print("  Speacial character --- -=")
                    else :
                        print("  Speacial character --- -")
                elif read[i] == "*":
                    if read[i+1] == "=":
                        i +=1
                        print("  Speacial character --- *=")
                    else :
                        print("  Speacial character --- *")
                elif read[i] == "/":
                    if read[i+1] == "=":
                        i +=1
                        print("  Speacial character --- /=")
                    else :
                        print("  Speacial character --- /")
                elif read[i] == "!":
                    if read[i+1] == "=":
                        i +=1
                        print("  Speacial character --- !=")
                    else :
                        print("  Speacial character --- !")
                elif read[i] == "=":
                    if read[i+1] == "=":
                        i +=1
                        print("  Speacial character --- ==")
                    else :
                        print("  Speacial character --- =")

                elif read[i] == "|":
                    print("  Speacial character --- |")
                elif read[i] == "&":
                    print("  Speacial character --- &")
                elif read[i] == ",":
                    print("  Speacial character --- ,")
                elif read[i] == "(":
                    print("  Speacial character --- (")#左右括号匹配交给语法分析
                elif read[i] == ")":
                    print("  Speacial character --- )")
                elif read[i] == ":":
                    print("  Speacial character --- :")

                elif  ("A" <= sentence[sign] <= "Z") or ("a" <= sentence[sign] <= "z") :
                    bs = i
                    while i <length-1:
                        if re.search('[0-9a-zA-Z]',read[i+1])!=None:
                            i += 1
                        else:
                            keywordRecg(read[bs:i+1])
                            break
                
                elif re.search('[0-9]',read[i])!=None:
                    if read[i] == '0':#0开头
                        bs=i
                        while True:
                            if read[i+1] =='.':#小数
                                i+=1
                                
                                while True:
                                    if re.search('[0-9]',read[i+1])!=None:#继续数字
                                        i+=1
                                        pass
                                    elif read[i+1] == ' ' or read[i+1] == '\n' or read[i+1] == '\t' or re.search('[%&*()\-+=:]',read[i+1])!=None:#结束
                                        if read[i]=='.':#0. 错误输入
                                            print("  [error]:"+read[bs:i+1]+"is illegal")
                                            break
                                        print("  float --- value = "+read[bs:i+1])
                                        break
                                    else:#错误字符
                                        while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                            i+=1
                                        print("  [error]: "+read[bs:i+1]+" is illegal.")
                                        break
                                break
                            elif read[i+1] == ' ' or read[i+1] == '\n' or read[i+1] == '\t':#结束
                                print("  integer --- value = 0")
                                break
                            else:#错误字符
                                while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                    i+=1
                                print("  [error]: "+read[bs:i+1]+" is illegal.")
                                break
                    
                    else:#非0开头
                        bs = i
                        while True:
                            if read[i+1] =='.':#小数
                                i+=1
                                
                                while True:
                                    if re.search('[0-9]',read[i+1])!=None:#继续数字
                                        i+=1
                                        pass
                                    elif read[i+1] == ' ' or read[i+1] == '\n' or read[i+1] == '\t':#结束
                                        if read[i]=='.':#x.错误输入
                                            print("  [error]:"+read[bs:i+1]+"is illegal")
                                            break
                                        print("  float --- value = "+read[bs:i+1])
                                        break
                                    else:#错误字符
                                        while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                            i+=1
                                        print("  [error]: "+read[bs:i+1]+" is illegal.")
                                        break
                                break
                            elif re.search('[0-9]',read[i+1])!=None:#继续整数
                                i+=1
                                pass
                            elif read[i+1] == ' ' or read[i+1] == '\n' or read[i+1] == '\t' or re.search('[%&*()\-+=:]',read[i+1])!=None:#结束
                                print("  integer --- value = "+read[bs:i+1])
                                break
                            else:#错误字符
                                while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                    i+=1
                                print("  [error]: "+read[bs:i+1]+" is illegal.")
                                break       


                elif read[i] == '\n':
                    row_counter += 1#下一行

                elif read[i] == '\t':
                    pass

                else:
                    print("  [error]: illegal cahracter.")

    except Exception as e:
        print(e)


def keywordRecg(Slice):
    if Slice in keywords.keys():
        print("  reservered keywords --- "+Slice)
    else:
        print("  identifier --- "+Slice)
    #TODO

def main():
    if len(sys.argv) < 2:
        print("No filename, in cmd use 'python lexAnl.py youFileName'.")
    else:
        try:
            scanner(sys.argv[1]) 
        except Exception as e:
            print(e)
    
    


if __name__ == '__main__':
    main()
