'''ver:1.0 语法版本
    
#   Vt = {id,int,float,vop,alop}    
        identifier integer float value_giving_operators algorithm_and_logical_operators
    Vn = {ETT,DIGIT,ALS,VGL}        
        entity digit algorithm_and_logical_sentence value_giving_sentence

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

keywords = {
'for':601,
'🦅':602,#in
'while':603,
'and':604,
'or':605,
'🐺':606,#none
'🥛🍎':607,#if 如果
'🙅‍':608,#not
'elif':609,
'else':610,
'🏀':611,#break 
'🚀🥛':612,#import 导入
'☞🔪':613,#until 直到
'💉':614,#true  真
'false':615,
'batt1ebear':616,
'🏠':617,#from 
'🍎':618,#pass 过,
'def':619,
}  
alop={
    '+':101,
    '-':102,
    '*':103,
    '/':104,
    '>':105,
    '<':106,
    '>=':107,
    '<=':108,
    '!=':109,
    '==':110,
}
vop={
    '=':201,
    '+=':202,
    '-=':203,
    '*=':204,
    '/=':205,

}
