'''
AbLan lexical scanner
author:batt1ebear 20171308074

#lex principle：ascii字符和emoji可以作为标识符 标识符数字不能开头 %%作为注释

#usage:
    in django: use function getToken(filepath)
    
    return:
        function return : result state and
            [
                'ROW []: STR',
            '   JUDGING',
            '   JUDGING',
            ···
            ]
            
            for django display if state is 0 , you cannot enter syntax scanner and lex_to_syntax.json will not be built

        output file ->lex_to_syntax.json : 
            [{value1:cataCode1},{value2:cataCode2},···]

            for syntax scanner

    in terminals : now not supported
'''

# coding=utf-8
import sys
import re
import json
from dat import vop,alop,keywords



djangoResult=[]
lexToDjango=[]
resultStat = 1

def preprocessing(raw):#预处理 去除多余空格和空行
    if not raw:#EOF
        djangoResult.append("----scanner completed successfully----")
        return 1

    elif raw[0] == '\n':
        return 0 #空行不计入

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
        global resultStat
        f_read = open(filename,'r',encoding='utf8')
        #f_write = open('/example/lexical_result.txt','w',encoding='utf8')
        row_counter=1#行数计数器
        while True:

            raw = f_read.readline()
            f_read.flush()

            read = preprocessing(raw)#预处理 
            if read == 1:#EOF跳出 返回resultStat 和 djangoResult           -----程序出口-------
                if resultStat == 1:#全部正确可以生成json进行语法分析
                    with open('lex_to_syntax.json','w') as f:
                        json.dump(lexToDjango,f) 
                    print("lexical correct")
                return djangoResult,resultStat
            elif read == 0:#空行
                continue
            else:#正常串继续
                pass

            djangoResult.append("ROW "+str(row_counter) + ': ' + read[:-1])#防止显示\n
            length = len(read)#本行长度
            i = -1

            while i <length -1:#length-1 为 行末尾\n
                i += 1
                if read[i] == " ":
                    continue#遇到空格继续状态0
                elif read[i] == "\t":
                    continue#遇到制表符继续状态0
                elif read[i] == "%":
                    bs = i #bufferstart 单词起始位置
                    i += 1
                    while read[i] != "%" :
                        if i+1 >=length-1 :
                            djangoResult.append("  [error]："+read[bs:i+1]+" is illegal , need %")#{没有封闭
                            resultStat = 0
                            break
                        i += 1
                    pass#省略注释 注：注释不可跨行
                
                elif read[i] == "+":
                    if read[i+1] == "=":
                        i +=1
                        djangoResult.append("  Speacial character --- +=")
                        lexToDjango.append({read[i-1:i+1]:vop[read[i-1:i+1]]})
                    else :
                        djangoResult.append("  Speacial character --- +")
                        lexToDjango.append({read[i]:alop[read[i]]})
                elif read[i] == "-":
                    if read[i+1] == "=":
                        i +=1
                        djangoResult.append("  Speacial character --- -=")
                        lexToDjango.append({read[i-1:i+1]:vop[read[i-1:i+1]]})
                    else :
                        djangoResult.append("  Speacial character --- -")
                        lexToDjango.append({read[i]:alop[read[i]]})
                elif read[i] == "*":
                    if read[i+1] == "=":
                        i +=1
                        djangoResult.append("  Speacial character --- *=")
                        lexToDjango.append({read[i-1:i+1]:vop[read[i-1:i+1]]})
                    else :
                        djangoResult.append("  Speacial character --- *")
                        lexToDjango.append({read[i]:alop[read[i]]})
                elif read[i] == "/":
                    if read[i+1] == "=":
                        i +=1
                        djangoResult.append("  Speacial character --- /=")
                        lexToDjango.append({read[i-1:i+1]:vop[read[i-1:i+1]]})
                    else :
                        djangoResult.append("  Speacial character --- /")
                        lexToDjango.append({read[i]:alop[read[i]]})
                elif read[i] == "!":
                    if read[i+1] == "=":
                        i +=1
                        djangoResult.append("  Speacial character --- !=")
                        lexToDjango.append({read[i-1:i+1]:alop[read[i-1:i+1]]})
                    else :
                        djangoResult.append("  Speacial character --- !")
                        lexToDjango.append({read[i]:alop[read[i]]})
                elif read[i] == ">":
                    if read[i+1] == "=":
                        i +=1
                        djangoResult.append("  Speacial character --- >=")
                        lexToDjango.append({read[i-1:i+1]:alop[read[i-1:i+1]]})
                    else :
                        djangoResult.append("  Speacial character --- >")
                        lexToDjango.append({read[i]:alop[read[i]]})
                elif read[i] == "<":
                    if read[i+1] == "=":
                        i +=1
                        djangoResult.append("  Speacial character --- <=")
                        lexToDjango.append({read[i-1:i+1]:alop[read[i-1:i+1]]})
                    else :
                        djangoResult.append("  Speacial character --- <")
                        lexToDjango.append({read[i]:alop[read[i]]})
                elif read[i] == "=":
                    if read[i+1] == "=":
                        i +=1
                        djangoResult.append("  Speacial character --- ==")
                        lexToDjango.append({read[i-1:i+1]:alop[read[i-1:i+1]]})
                    else :
                        djangoResult.append("  Speacial character --- =")
                        lexToDjango.append({read[i]:vop[read[i]]})

                # elif read[i] == "|":
                #     djangoResult.append("  Speacial character --- |\n")
                # elif read[i] == "&":
                #     djangoResult.append("  Speacial character --- &\n")
                #TODO:new catagory
                elif read[i] == ",":
                    djangoResult.append("  Speacial character --- ,")
                elif read[i] == "(":
                    djangoResult.append("  Speacial character --- (")#左右括号匹配交给语法分析
                elif read[i] == ")":
                    djangoResult.append("  Speacial character --- )")
                elif read[i] == ":":
                    djangoResult.append("  Speacial character --- :")

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
                                            djangoResult.append("  [error]:"+read[bs:i+1]+"is illegal")
                                            resultStat = 0
                                            break
                                        djangoResult.append("  float --- value = "+read[bs:i+1]+"")
                                        lexToDjango.append({read[bs:i+1]:400})
                                        break
                                    else:#错误字符
                                        while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                            i+=1
                                        djangoResult.append("  [error]: "+read[bs:i+1]+" is illegal.")
                                        resultStat = 0
                                        break
                                break
                            elif read[i+1] == ' ' or read[i+1] == '\n' or read[i+1] == '\t':#结束
                                djangoResult.append("  integer --- value = 0\n")
                                lexToDjango.append({0:300})
                                break
                            else:#错误字符
                                while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                    i+=1
                                djangoResult.append("  [error]: "+read[bs:i+1]+" is illegal.")
                                resultStat = 0
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
                                            djangoResult.append("  [error]:"+read[bs:i+1]+"is illegal")
                                            resultStat = 0
                                            break
                                        djangoResult.append("  float --- value = "+read[bs:i+1])
                                        lexToDjango.append({read[bs:i+1]:400})
                                        break
                                    else:#错误字符
                                        while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                            i+=1
                                        djangoResult.append("  [error]: "+read[bs:i+1]+" is illegal.")
                                        resultStat = 0
                                        break
                                break
                            elif re.search('[0-9]',read[i+1])!=None:#继续整数
                                i+=1
                                pass
                            elif read[i+1] == ' ' or read[i+1] == '\n' or read[i+1] == '\t' or re.search('[%&*()\-+=:]',read[i+1])!=None:#结束
                                djangoResult.append("  integer --- value = "+read[bs:i+1])
                                lexToDjango.append({read[bs:i+1]:300})
                                break
                            else:#错误字符
                                while read[i+1]!=' ' and read[i+1]!='\n' and read[i+1]!='\t':
                                    i+=1
                                djangoResult.append("  [error]: "+read[bs:i+1]+" is illegal.")
                                resultStat = 0
                                break       


                elif read[i] == '\n':
                    row_counter += 1#下一行

                elif read[i] == '\t':
                    pass

                else:
                    djangoResult.append("  [error]: illegal character : "+ read[i])
                    resultStat = 0

    except Exception as e:
        print(e)


def keywordRecg(Slice):
    if Slice in keywords:
        djangoResult.append("  reservered keywords --- "+Slice)
        lexToDjango.append({Slice:600})
    else:
        djangoResult.append("  identifier --- "+Slice)
        lexToDjango.append({Slice:500})
    #TODO

###########debug#############
def main():
    if len(sys.argv) < 2:
        test()
    else:
        try:
            getToken(sys.argv[1]) 
        except Exception as e:
            print("No file inputed.Please use 'python scanner.py youFile' in cmd.")

def test():
    getToken('example\\syntax_correct_test.txt')
    


if __name__ == '__main__':
    main()

