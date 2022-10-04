from __future__ import annotations

# TODO:
# Add suport for unary operators
# Update README 
# Update tests 
# Resolve all #TODO in file 

from collections import deque
from enum import Enum, auto
from operator import add, sub, mul

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

def calc(tokens: str) -> list[Result, str]:
    num_stack = deque()
    op_stack = deque()
    i = 0

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
                right = num_stack.pop()
                left = num_stack.pop()
                op = op_stack.pop()
                num_stack.append(apply_op(left, right, op))
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
        op = op_stack.pop()
        right = num_stack.pop()
        if num_stack:
            left = num_stack.pop()
            num_stack.append(apply_op(left, right, op))
        else:
            return Result.ERROR, f"Missing operand in expression."

    if len(num_stack) > 1:
        return Result.ERROR, f"Missing operator in expression."
    if not num_stack:
        return Result.ERROR, f"Missing ) in expression."

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
