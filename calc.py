from __future__ import annotations

# TODO:
# Add suport for unary operators
# Update README 
# Update tests 
# Add instructions on how to use the calculator
# Resolve all #TODO in file 

from collections import deque
from enum import Enum, auto
from operator import add, sub, mul
from os import remove

class Result(Enum):
    ERROR = auto()
    SUCCESS = auto()

precedence = {
    '*' : 2,
    '+' : 1,
    '-' : 1,
    '(' : 0
}

operators =  {
    '*' : mul,
    '+' : add,
    '-' : sub
}

digits = set([str(x) for x in range(10)])

def log_error(error_msg):
    # TODO: Use logger
    print(error_msg)

def is_digit(value):
    return value in digits

def is_operator(value):
    return value in operators

def get_precedence(operator):
    return precedence[operator]

def apply_op(left, right, operator):
    return operators[operator](left, right)

def log_result(value, expr):
    # TODO: Use logger
    print(f"{expr} = {value}")


# counts the number of spaces in the expression then runs expression.remove(" ") that many times to remove all the spaces
def remove_spaces(expression):
    
    return expression.replace(" ","")

#checks through list for any invalid tokens and returns false if it finds any
def check_tokens(expression):
    i = 0
    while i < len(expression):
        if (not is_digit(expression[i])) and (not is_operator(expression[i])) and (not expression[i] == "(") and (not expression[i] == ")"):
            return False
        i+=1
    return True

#contains logic for all the scenarios where an expression would not be valid
def check_validity(expression):
    i =0 
    while i < len(expression)-1:
        # Cases: two operators next to one another "+-", opening parenthesis followed by an operator "(+", number followed by opening parenthesis"12(", closing parenthesis followed by digit ")12", operator followed by closing parenthesis "+)"
        if (is_operator(expression[i]) and is_operator(expression[i+1])) or  (expression[i] == "(" and (is_operator(expression[i+1]) and expression[i+1] != "-") ) or (is_digit(expression[i]) and expression[i+1] == "(") or (expression[i] == ")" and is_digit(expression[i+1]) )or (is_operator(expression[i]) and expression[i+1] == ")"):   
            return False
        i += 1
    # if the first or last char in the expression is an operator then the expression is not valid
    if is_operator(expression[len(expression)-1]) or is_operator(expression[0]):
       return False
    i = 0
    count = 0
    while i<len(expression):
        if expression[i] == "(":
            count+=1
        if expression[i] == ")":
            count-=1
        i+= 1
    if count != 0:
        return False
    #otherwise the expression is valid
    return True

def calc(tokens: str) -> list[Result, str]:
    num_stack = deque()
    op_stack = deque()
    i = 0

    tokens = remove_spaces(tokens)
    if not check_tokens(tokens):
        return Result.ERROR, "invalid tokens used"
    digit_test = tokens
    if digit_test.lstrip("-").isdigit() and tokens[0] == "-":
        return Result.SUCCESS, str(tokens)
    if not check_validity(tokens):
        return Result.ERROR, "invalid input"


    while i < len(tokens):
        token = tokens[i]
        if token == " ":
            i += 1
            continue
        elif is_digit(token):
            num = 0
            while i < len(tokens) and is_digit(tokens[i]):
                num = (num * 10) + int(tokens[i])
                i += 1
            i -= 1
            num_stack.append(num)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                if len(num_stack) >= 2:
                    right = num_stack.pop()
                    left = num_stack.pop()
                    op = op_stack.pop()
                    num_stack.append(apply_op(left, right, op))
                else:
                    return Result.ERROR, "Unary operators are not supported."
            if op_stack:
                op_stack.pop()
            else:
                return Result.ERROR, "Unexpected ')' in expression."
        elif is_operator(token):
            while op_stack and get_precedence(op_stack[-1]) >= get_precedence(token):         
                    if len(num_stack) >= 2:
                        right = num_stack.pop()
                        left = num_stack.pop()            
                        op = op_stack.pop()
                        num_stack.append(apply_op(left, right, op))
                    else:
                        return Result.ERROR, f"Unexpected {token} in expression."
        
            op_stack.append(token)
        else:
            return Result.ERROR, f"{token} is not a recognised as valid in an expression."
        i += 1

    while op_stack and num_stack:
        if op_stack[-1] == '(':
            return Result.ERROR, f"Missing ) in expression."
        op = op_stack.pop()
        if len(num_stack) >= 2:
            right = num_stack.pop()
            left = num_stack.pop()
            num_stack.append(apply_op(left, right, op))
        else:
            return Result.ERROR, f"Unexpected {op} in expression."

    if len(num_stack) > 1:
        return Result.ERROR, f"Missing operator in expression."
    if not num_stack:
        return Result.ERROR, f"No integers in expression."

    return Result.SUCCESS, str(num_stack.pop())

if __name__ == '__main__':
    while True:
        expr = input("Enter an expression: ")
        if expr == "quit":
            break
        result, value = calc(expr)
        if result == Result.ERROR:
            log_error(value)
        else:
            log_result(value, expr)
