# coding=utf-8
#python抽象话词法分析器
#author:batt1ebear

#语法规则：ascii字符和emoji可以作为标识符 标识符数字不能开头 {}作为注释
#使用方法 python scanner.py inputFile ->输出到目录下新建的result.py
import sys
import re

keywords = ['for',
'🦅',#in
'while',
'and',
'or',
'🐺',#none
'🥛🍎',#if 如果
'🙅‍',#not
'elif',
'else',
'🏀',#break 
'🚀🥛',#import 导入
'☞🔪',#until 直到
'💉',#true  真
'false',
'batt1ebear',
'🏠',#from
'🍎'#pass 过,
'def'
]  

'''Speacial character :
+ - * / ! < > = += -= *= /= != <= >= == , ( ) :
'''

def preprocessing(raw):#预处理 去除多余空格和空行
    if not raw:
                print("----scanner completed successfully----")
                sys.exit(0)#末尾程序出口

    elif raw[0] == '\n':
        return False #空行不计入

    elif raw[-1]!='\n':#末尾行加上\n保证一致处理
        raw+='\n'
    
    else: 
        pass
    
    i=0
    while raw[i]==' ' or raw[i]=='\t':
        i+=1
    line = raw[i:]
    return line


def getToken(filename):
    try:
        f_read = open(filename,'r',encoding='utf8')
        f_write = open('/example/result.txt','w',encoding='utf8')
        row_counter=1#行数计数器
        while True:

            raw = f_read.readline()
            f_read.flush()
            read = preprocessing(raw)#预处理
            if not read:#跳过空行
                continue

            f_write.write("ROW "+str(row_counter) + ': ' + read[:-1]+"\n")#防止显示\n
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
                            f_write.write("  [error]："+read[bs:i+1]+" is illegal , need }\n")#{没有封闭
                            break
                        i += 1
                    pass#省略注释 注：注释不可跨行
                
                elif read[i] == "+":
                    if read[i+1] == "=":
                        i +=1
                        f_write.write("  Speacial character --- +=\n")
                    else :
                        f_write.write("  Speacial character --- +\n")
                elif read[i] == "-":
                    if read[i+1] == "=":
                        i +=1
                        f_write.write("  Speacial character --- -=\n")
                    else :
                        f_write.write("  Speacial character --- -\n")
                elif read[i] == "*":
                    if read[i+1] == "=":
                        i +=1
                        f_write.write("  Speacial character --- *=\n")
                    else :
                        f_write.write("  Speacial character --- *\n")
                elif read[i] == "/":
                    if read[i+1] == "=":
                        i +=1
                        f_write.write("  Speacial character --- /=\n")
                    else :
                        f_write.write("  Speacial character --- /\n")
                elif read[i] == "!":
                    if read[i+1] == "=":
                        i +=1
                        f_write.write("  Speacial character --- !=\n")
                    else :
                        f_write.write("  Speacial character --- !\n")
                elif read[i] == ">":
                    if read[i+1] == "=":
                        i +=1
                        f_write.write("  Speacial character --- >=\n")
                    else :
                        f_write.write("  Speacial character --- >\n")
                elif read[i] == "<":
                    if read[i+1] == "=":
                        i +=1
                        f_write.write("  Speacial character --- <=\n")
                    else :
                        f_write.write("  Speacial character --- <\n")
                elif read[i] == "=":
                    if read[i+1] == "=":
                        i +=1
                        f_write.write("  Speacial character --- ==\n")
                    else :
                        f_write.write("  Speacial character --- =\n")

                # elif read[i] == "|":
                #     f_write.write("  Speacial character --- |\n")
                # elif read[i] == "&":
                #     f_write.write("  Speacial character --- &\n")
                elif read[i] == ",":
                    f_write.write("  Speacial character --- ,\n")
                elif read[i] == "(":
                    f_write.write("  Speacial character --- (\n")#左右括号匹配交给语法分析
                elif read[i] == ")":
                    f_write.write("  Speacial character --- )\n")
                elif read[i] == ":":
                    f_write.write("  Speacial character --- :\n")

                elif re.search('[a-zA-Z]',read[i])!=None or \
                ('e29880'<= read[i].encode('utf8').hex() <= 'e2a7bf') or \
                    ('f09f8080'<= read[i].encode('utf8').hex() <= 'f09fadaf'):
                    #拉丁字符 即'A'<=read[i]<='Z' or 'a'<=read[i]<='z'
                    #将一个emoji字符转换成utf8 hex码
                    #查表确定编码范围
                    bs = i
                    while i <length-1:
                        if re.search('[0-9a-zA-Z]',read[i+1])!=None or \
                            ('e29880'<= read[i+1].encode('utf8').hex() <= 'e2a7bf') or \
                                ('f09f8080'<= read[i+1].encode('utf8').hex() <= 'f09fadaf'):
                            i += 1
                        else:
                            keywordRecg(read[bs:i+1],f_write)
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
                                            f_write.write("  [error]:"+read[bs:i+1]+"is illegal\n")
                                            break
                                        f_write.write("  float --- value = "+read[bs:i+1]+"\n")
                                        break
                                    else:#错误字符
                                        while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                            i+=1
                                        f_write.write("  [error]: "+read[bs:i+1]+" is illegal.\n")
                                        break
                                break
                            elif read[i+1] == ' ' or read[i+1] == '\n' or read[i+1] == '\t':#结束
                                f_write.write("  integer --- value = 0\n")
                                break
                            else:#错误字符
                                while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                    i+=1
                                f_write.write("  [error]: "+read[bs:i+1]+" is illegal.\n")
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
                                            f_write.write("  [error]:"+read[bs:i+1]+"is illegal\n")
                                            break
                                        f_write.write("  float --- value = "+read[bs:i+1]+"\n")
                                        break
                                    else:#错误字符
                                        while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                            i+=1
                                        f_write.write("  [error]: "+read[bs:i+1]+" is illegal.\n")
                                        break
                                break
                            elif re.search('[0-9]',read[i+1])!=None:#继续整数
                                i+=1
                                pass
                            elif read[i+1] == ' ' or read[i+1] == '\n' or read[i+1] == '\t' or re.search('[%&*()\-+=:]',read[i+1])!=None:#结束
                                f_write.write("  integer --- value = "+read[bs:i+1]+"\n")
                                break
                            else:#错误字符
                                while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                    i+=1
                                f_write.write("  [error]: "+read[bs:i+1]+" is illegal.\n")
                                break       


                elif read[i] == '\n':
                    row_counter += 1#下一行

                elif read[i] == '\t':
                    pass

                else:
                    f_write.write("  [error]: illegal character : "+ read[i]+"\n")

    except Exception as e:
        print(e)


def keywordRecg(Slice,f_write):
    if Slice in keywords:
        f_write.write("  reservered keywords --- "+Slice+"\n")
    else:
        f_write.write("  identifier --- "+Slice+"\n")
    #TODO

def main():
    if len(sys.argv) < 2:
        test()
    else:
        try:
            getToken(sys.argv[1]) 
        except Exception as e:
            print("No file inputed.Please use 'python scanner.py youFile' in cmd.")

def test():
    getToken('emojiTest.txt')
    


if __name__ == '__main__':
    main()

