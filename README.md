# AbLan
~~in cmd use~~ :
    ```python scanner.py filename```
 
Abstract Language Compiler
抽象话词法分析器

# Finished Work : Lexical Scanner

Emoji characters can be used as identifiers like:
    ``` 🐎 = 1.14514
    args = 🌶💩💉💧🐮🍺 ```

# Way to use lexical scanner:
In light of poor utf8 support in cmd and other terminals, output is printed in result.txt .
Type ```python lexical_scanner.py youTestFile ``` in cmd and find result.txt to see the output.

# Current Work ： Syntax Scanner
building LR(1) syntax analysis programme


# environment:
+ python3
+ re


# TODO:
in lexical scanner divide special characters into ALOP(arithmetic and logical operators) and VOP(give_value operators) 
    alop -> + | - | * | / | > | < | >= | <= | != | == #算数逻辑运算符 双目
    vop -> = | += | -= | *= | /= #赋值运算符
