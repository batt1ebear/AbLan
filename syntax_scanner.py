'''
AbLan 自下而上语法LR(0)规则说明  类似python风格(并不
author:batt1ebear 20171308074


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
from dat import LR1Table , Principe

djangoResult=[]
resultStat = 1
charbuff = []

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
        buffPrin=int(nextSt[1:])
        replacingStr,replacedStr = self.restrict(buffPrin)
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
    if 100 <= given_char <= 199:#'alop'
        col = 0
    elif 200 <= given_char <= 299:#'vop':
        col = 1
    elif given_char == 300:#'int':
        col = 2
    elif given_char == 400:#'float':
        col = 3
    elif given_char == 500:#'id':
        col = 4
    #elif 600 <= given_char <=699:#keywords
    elif given_char == 0:#'$':
        col = 5
    elif given_char == 1:#'VGL':
        col = 6
    elif given_char == 2:#'ALS':
        col = 7
    elif given_char == 3:#'ETT':
        col = 8
    elif given_char == 4:#'DIGIT':
        col = 9
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
        if 100 <= charStk[i] <= 199:#'alop'
            char+='alop '
        elif 200 <= charStk[i] <= 299:#'vop':
            char+='vop '
        elif charStk[i] == 300:#'int':
            char+='int '
        elif charStk[i] == 400:#'float':
            char+='float '
        elif charStk[i] == 500:#'id':
            char+='id '
        #elif 600 <= given_char <=699:#keywords
        elif charStk[i] == 0:#'$':
            char+='$ '
        elif charStk[i] == 1:#'VGL':
            char+='VGL '
        elif charStk[i] == 2:#'ALS':
            char+='ALS '
        elif charStk[i] == 3:#'ETT':
            char+='ETT '
        elif charStk[i] == 4:#'DIGIT':
            char+='DIGIT '
        else:
            print("coding error 2")
    return char

def readLex():
    with open('lex_to_syntax.json','r') as f:
        raw = json.load(f)    
    return raw

def getTree():
    global resultStat
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
            d.goto(nextSt)
        elif nextSt == 'acc':
            djangoResult.append(['syntax correct'])
            #print(djangoResult)
            print("syntax correct ")
            return djangoResult,resultStat

           
        else:
            print("coding error 1")
            sys.exit(0)

############debug##############
if __name__ == "__main__":
    getTree()
