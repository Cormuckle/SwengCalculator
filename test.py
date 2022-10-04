from calc import calc, Result 

def test_simple_expr():
    assert calc("3 + 4") == (Result.SUCCESS, '7')
    assert calc("1 - 2 + 4") == (Result.SUCCESS, '3')
    assert calc("3 * 0 + 1") == (Result.SUCCESS, '1')   

def test_complex_expr():   
    # expr = "1 * 2 + 4 * 2 * 2 - 7 * 3 * 4 - 1 + 333 - 246 + 1738 * -1 - 2"
    expr = "1 * 2 + 4 * 2 * 2 - 7 * 3 * 4 - 1 + 333 - 246 + 1738 * 1 - 2"
    assert (Result.SUCCESS, str(eval(expr))) == calc(expr)

# def test_unexpected_or_extra_parenthesis():
#     assert False

# def test_invalid_tokens():
#     assert False

# def test_unexpected_operators():
#     assert False

# def test_arbitrary_spaces():
#     assert False

# def test_no_space():
#     assert False

# def test_single_integer():
#     # 1, -1, (1), (-1), (-123), (123)
#     assert False
