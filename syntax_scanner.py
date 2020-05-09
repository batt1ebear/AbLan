'''AbLan 自下而上语法LR(0)规则说明  类似python风格(并不
    ver:1.0 (无emoji测试版本)
    
#   Vt = {id,int,float,vop,alop}    #identifier integer float value_giving_operators algorithm_and_logical_operators
    Vn = {ETT,DIGIT,ALS,VGL}        #entity digit algorithm_and_logical_sentence value_giving_sentence

#   repersent codes of Vt and Vn:
    alop    : 100
    vop     : 200
    int     : 300
    float   : 400
    id      : 500

    VGL     : 1
    ALS     : 2
    ETT     : 3
    DIGIT   : 4

    $       : 0

#   principle:
    ETT     -> id | DIGIT 
    DIGIT   -> int | float 
    ALS     -> ETT alop ETT | ALS alop ETT  
    VGL     -> identifier vop ALS | identifier vop ETT 
    
#   divided principle:
    0 S     -> VGL					
    1 VGL   -> id vop ETT		1 -> 500,200,3	
    2 VGL   -> id vop ALS		1 -> 500,200,2	
    3 ALS   -> ETT alop ETT		2 -> 3,100,3	
    4 ALS   -> ALS alop ETT		2 -> 2,100,3	
    5 ETT   -> id				3 -> 500	
    6 ETT   -> DIGIT			3 -> 4	
    7 DIGIT -> int				4 -> 300	
    8 DIGIT -> float			4 -> 400

'''
# coding=utf-8
import sys

#        action         |       goto
# alop vop int float id | VGL ALS ETT DIGIT
LR1Table = [   
[-1,-1,-1,-1,'s2',-1,1,-1,-1,-1],
[-1,-1,-1,-1,-1,'acc',-1,-1,-1,-1],
[-1,'s3',-1,-1,-1,-1,-1,-1,-1,-1],
[-1,-1,'s15','s16','s13',-1,-1,17,4,14],
['s5',-1,-1,-1,-1,'r1',-1,-1,-1,-1],
[-1,-1,'s15','s16','s13',-1,-1,-1,6,14],
['s7',-1,-1,-1,-1,'r3',-1,-1,-1,-1],
[-1,-1,'s11','s12','s9',-1,-1,-1,8,1-1],
['r3',-1,-1,-1,-1,-1,-1,-1,-1,-1],
['r5',-1,-1,-1,-1,-1,-1,-1,-1,-1],
['r6',-1,-1,-1,-1,-1,-1,-1,-1,-1],
['r7',-1,-1,-1,-1,-1,-1,-1,-1,-1],
['r8',-1,-1,-1,-1,-1,-1,-1,-1,-1],
['r5',-1,-1,-1,-1,'r5',-1,-1,-1,-1],
['r6',-1,-1,-1,-1,'r6',-1,-1,-1,-1],
['r7',-1,-1,-1,-1,'r7',-1,-1,-1,-1],
['r8',-1,-1,-1,-1,'r8',-1,-1,-1,-1],
['s18',-1,-1,-1,-1,'r2',-1,-1,-1,-1],
[-1,-1,'s15','s16','s13',-1,-1,-1,19,14],
['r4',-1,-1,-1,-1,'r4',-1,-1,-1,-1],
]

Principe=[
    [-1,-1],#0号规则用不到 无意义
    [1,500,200,3],
    [1,500,200,2],
    [2,3,100,3],
    [2,2,100,3],
    [3,500],
    [3,4],
    [4,300],
    [4,400],
]

class Dstack:

    charStk=[0]#$
    statStk=[0]

    def actionS(self,buffStat,buffChar):
        self.charStk.append(buffChar)
        self.statStk.append(buffStat)

    def actionR(self,buffPrin):
        replacingStr,replacedStr = self.restrict(buffPrin)
        del self.charStk[-len(replacedStr):]#删除被规约的字符和对等的状态
        del self.statStk[-len(replacedStr):]
        self.charStk.append(replacingStr)#换上规约后的字符
        self.goto(self.statStk[-1],self.charStk[-1])
        
    def goto(self,topStat,topChar):#规约后必goto 跟在actionR后的内部函数
        nextSt=findTable(topStat,topChar)
        if nextSt == -1:
            print("syntax error")
            sys.exit(0)
        else:
            self.statStk.append(nextSt)#追平两栈高度
    def restrict(self,buffPrin):#根据规则规约
            return Principe[buffPrin][0],Principe[buffPrin][1:]

    def topStat(self):
        return self.statStk[-1]
    
    def topChar(self):
        return self.charStk[-1]

    

def findTable(given_status,given_char):#given_char不一定是buff 在goto操作是栈顶字符
    col=-1
    if given_char == 100:#'alop'
        col = 0
    elif given_char == 200:#'vop':
        col = 1
    elif given_char == 300:#'int':
        col = 2
    elif given_char == 400:#'float':
        col = 3
    elif given_char == 500:#'id':
        col = 4
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



def mainControl():
    testStr=[500,200,500,100,300]
    testStr.append(0)#末尾加上$
    d=Dstack()
    while(True):
        point = testStr[0]#指针所指
        nextSt = findTable(d.topStat(),point)#根据栈顶状态和指针查分析表
        if nextSt[0] == 's':#shift压栈
            buffStat=int(nextSt[1:])
            d.actionS(buffStat,point)
            del testStr[0]
        elif nextSt[0] == 'r':#规约
            buffPrin=int(nextSt[1:])
            d.actionR(buffPrin)
        elif nextSt == 'acc':
            print("syntax correct ")
            sys.exit(0)
        elif nextSt == -1:
            print("syntax error ")
            sys.exit(0)
        else:
            print("coding error 1")
            sys.exit(0)

def readLex():
    #TODO
    return -1

if __name__ == "__main__":
    mainControl()
