'''AbLan 自下而上语法LR(0)规则说明  类似python风格
    ver:1.0 (无emoji版本)
    
    Vt = {id,int,float,vop,alop} #identifier integer algorithm_and_logical_operators value_giving_operators

    ETT -> id | DIGIT #实体
    DIGIT -> int | float  #数字

    ALS -> ETT alop ETT | ALS alop ETT  #运算与逻辑语句  双目 
    GVL -> identifier vop ALS | identifier vop ETT #赋值运算语句
    

'''
# coding=utf-8

