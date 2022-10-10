from calc import calc, Result 

def test_simple_expr():
    assert calc("3 + 4") == (Result.SUCCESS, '7')
    assert calc("1 - 2 + 4") == (Result.SUCCESS, '3')
    assert calc("3 * 0 + 1") == (Result.SUCCESS, '1')   

def test_complex_expr():   
    # expr = "1 * 2 + 4 * 2 * 2 - 7 * 3 * 4 - 1 + 333 - 246 + 1738 * -1 - 2"
    expr = "1 * 2 + 4 * 2 * 2 - 7 * 3 * 4 - 1 + 333 - 246 + 1738 * 1 - 2"
    assert (Result.SUCCESS, str(eval(expr))) == calc(expr)

 def test_unexpected_or_extra_parenthesis():
    assert calc("1+2 * (4+5))") == (Result.ERROR, "invalid input") 
    assert calc("1+2 * )(4+5))") == (Result.ERROR, "Unexpected ')' in expression.")
    assert calc("1+2 * (4+5") == (Result.ERROR, "Missing ) in expression.")

def test_invalid_tokens():
    assert calc("penguin") == (Result.ERROR, "invalid tokens used")

def test_unexpected_operators():
    assert calc("1+2 *+ (4+5)") == (Result.ERROR, "invalid input")

def test_arbitrary_spaces():
    assert calc("1+   2 + (4+ 5)  ") == (Result.SUCCESS, '12')

def test_no_space():
    assert calc("3+4") == (Result.SUCCESS, '7')

def test_single_integer():
    assert calc("1") == (Result.SUCCESS, '1')
    assert calc("-1") == (Result.SUCCESS, '-1')
    assert calc("(1)") == (Result.SUCCESS, '1')
    assert calc("(-1)") == (Result.SUCCESS, '-1')
    assert calc("-123") == (Result.SUCCESS, '-123')
    assert calc("123") == (Result.SUCCESS, '123')
