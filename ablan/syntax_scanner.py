'''
AbLan 自下而上语法LR(0)规则说明  类似python风格(并不
author:batt1ebear 


#   usage:
    in django : use function getTree()
    input : lex_to_syntax.json
    return:
        function return : result state and
        [
            ['statStk','charStk(expression)','nextSt','explanation of nextSt','remains in buff'],
            [],
            [],
        ···
        ]
'''
# coding=utf-8
import sys
import json
import os
from .dat import LR1Table, Principe

djangoResult=[]
resultStat = 1
charbuff = []
tree="digraph  {\n"

class Dstack:

    charStk=[0]#$
    statStk=[0]

    def actionS(self,nextSt):
        buffStat=int(nextSt[1:])
        self.charStk.append(charbuff[0])
        self.statStk.append(buffStat)
        del charbuff[0]
        djangoResult.append([str(self.statStk),adapter(self.charStk),nextSt,'移入'+adapter(charbuff[0])+'转到状态'+nextSt[1:],adapter(charbuff)])

    def actionR(self,nextSt):
        global tree
        buffPrin=int(nextSt[1:])
        replacingStr,replacedStr = self.restrict(buffPrin)

        for i in range(len(replacedStr)):#分析树
            tree += "{} -> {}\n".format(adapter(replacingStr), adapter(replacedStr[i]))
            
        del self.charStk[-len(replacedStr):]#删除被规约的字符和对等的状态
        del self.statStk[-len(replacedStr):]
        self.charStk.append(replacingStr)#换上规约后的字符
        djangoResult.append([str(self.statStk),adapter(self.charStk),nextSt,'使用规则'+str(buffPrin)+'进行规约',adapter(charbuff)])
        #self.goto(self.statStk[-1],self.charStk[-1])
        
    def goto(self,nextSt):#规约后必goto 跟在actionR后的内部函数
        self.statStk.append(nextSt)#追平两栈高度
        djangoResult.append([str(self.statStk),adapter(self.charStk),nextSt,'goto转到状态'+str(nextSt),adapter(charbuff)])
    def restrict(self,buffPrin):#根据规则规约
            return Principe[buffPrin][0],Principe[buffPrin][1:]

    def topStat(self):
        return self.statStk[-1]
    
    def topChar(self):
        return self.charStk[-1]

    

def findTable(given_status,given_char):#given_char不一定是buff 在goto操作是栈顶字符
    col=-1
    if given_char == 0 :
        col = 0
    elif given_char == 500:#id
        col = 2
    elif 200 <= given_char <= 299:#vop
        col = 3
    elif 100<= given_char <= 199:#alop
        col = 4
    elif given_char == 300:#int
        col = 5
    elif given_char == 400:#float
        col = 6
    elif given_char == 612:#import
        col = 7
    elif given_char == 619:#def
        col = 8
    elif given_char == 704:#:
        col = 9
    elif given_char == 702:#{
        col = 10
    elif given_char == 703:#}
        col =11
    elif given_char == 603:#while
        col = 12
    elif given_char == 700:#(
        col = 13
    elif given_char == 701:#)
        col = 14
    elif given_char == 609:#elif
        col = 15
    elif given_char == 607:#if
        col = 16
    elif given_char == 610:#else
        col = 17
    elif given_char == 620:#return
        col = 18
    elif given_char == 99:#BLK
        col = 20
    elif given_char == 1:#VGL
        col = 21
    elif given_char == 2:#ALS
        col = 22
    elif given_char == 3:#ETT
        col = 23
    elif given_char == 4:#DIGIT
        col = 24
    elif given_char == 5:#IMP
        col = 25
    elif given_char == 7:#DEF
        col = 26
    elif given_char == 8:#WIL
        col = 27
    elif given_char == 9:#ELF
        col = 28
    elif given_char == 10:#IF
        col = 29
    elif given_char == 11:#RET
        col = 30
    elif given_char == 6:#FUC
        col = 31
    
    else:
        print("coding error 0")

    return LR1Table[given_status][col]

def adapter(charStk):#将标识符转换回属性意义
    char=''
    length=0
    if type(charStk) == int:
        tem=charStk
        charStk=[tem]

    for i in range(len(charStk)):
        if charStk[i] == 0 :
            char+='$ '
        elif charStk[i] == 500:#id
            char+= 'id '
        elif 200 <= charStk[i] <= 299:#vop
            char+= 'vop '
        elif 100 <= charStk[i] <= 199:#alop
            char+= 'alop '
        elif charStk[i] == 300:#int
            char+= 'int '
        elif charStk[i] == 400:#float
            char+= 'float '
        elif charStk[i] == 612:#import
            char+= 'import '
        elif charStk[i] == 619:#def
            char+= 'def '
        elif charStk[i] == 704:#:
            char+= ': '
        elif charStk[i] == 702:#{
            char+= '{ '
        elif charStk[i] == 703:#}
            char+='} '
        elif charStk[i] == 603:#while
            char+= 'while '
        elif charStk[i] == 700:#(
            char+= '( '
        elif charStk[i] == 701:#)
            char+= ') '
        elif charStk[i] == 609:#elif
            char+= 'elif '
        elif charStk[i] == 607:#if
            char+= 'if '
        elif charStk[i] == 610:#else
            char+= 'else '
        elif charStk[i] == 620:#return
            char+= 'return '
        elif charStk[i] == 99:#BLK
            char+= 'BLK '
        elif charStk[i] == 1:#VGL
            char+= 'VGL '
        elif charStk[i] == 2:#ALS
            char+= 'ALS '
        elif charStk[i] == 3:#ETT
            char+= 'ETT '
        elif charStk[i] == 4:#DIGIT
            char+= 'DIGIT '
        elif charStk[i] == 5:#IMP
            char+= 'IMP '
        elif charStk[i] == 7:#DEF
            char+= 'DEF '
        elif charStk[i] == 8:#WIL
            char+= 'WIL '
        elif charStk[i] == 9:#ELF
            char+= 'ELF '
        elif charStk[i] == 10:#IF
            char+= 'IF '
        elif charStk[i] == 11:#RET
            char+= 'RET '
        elif charStk[i] == 6:#FUC
            char+= 'FUC '
        else:
            print("coding error 2")
    return char

def readLex():
    with open('lex_to_syntax.json','r') as f:
        raw = json.load(f)    
    return raw

def getTree():
    global resultStat,tree
    raw = readLex()

    
    for i in range(len(raw)):
        charbuff.append(list(raw[i].values())[0])#二元组提取分类标识码

    charbuff.append(0)#末尾加上$
    d=Dstack()
    while(True):
        nextSt = findTable(d.topStat(),charbuff[0])#根据栈顶状态和指针查分析表
        if nextSt == -1:
            print("syntax error ")
            djangoResult.append(["syntax error"])
            resultStat=0
            return djangoResult,resultStat
        elif nextSt[0] == 's':#shift压栈
            d.actionS(nextSt)
        elif nextSt[0] == 'r':#规约
            d.actionR(nextSt)
            nextSt=findTable(d.topStat(),d.topChar())
            if nextSt == -1:
                print("syntax error ")
                djangoResult.append(["syntax error"])
                resultStat=0
                return djangoResult,resultStat
            d.goto(int(nextSt[1:]))
        elif nextSt == 'acc':
            djangoResult.append(['syntax correct'])
            #print(djangoResult)
            tree+="}"
            

            print("syntax correct ")
            return djangoResult,resultStat

           
        else:
            print("coding error 1")
            sys.exit(0)
        #print(djangoResult)

############debug##############
if __name__ == "__main__":
    getTree()
