'''AbLan 自下而上语法LR(0)规则说明  类似python风格
    ver:1.0 (无emoji版本)
    
    Vt = {id,int,float,vop,alop} #identifier integer algorithm_and_logical_operators value_giving_operators

    ETT -> id | DIGIT #实体
    DIGIT -> int | float  #数字

    ALS -> ETT alop ETT | ALS alop ETT  #运算与逻辑语句  双目 
    GVL -> identifier vop ALS | identifier vop ETT #赋值运算语句
    
    divided principle:
    0 S -> GVL					
    1 GVL -> id vop ETT			
    2 GVL -> id vop ALS			
    3 ALS -> ETT alop ETT			
    4 ALS -> ALS alop ETT			
    5 ETT -> id					
    6 ETT -> DIGIT				
    7 DIGIT -> int					
    8 DIGIT -> float	

	


'''
# coding=utf-8

