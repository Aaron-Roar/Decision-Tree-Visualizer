def float_test(arbitrary_column):
    try:
        float(arbitrary_column[0])
    except ValueError:
        return False
    else:
        return True

def float_convert(variable):
    if(float_test(variable) == True):
        return float(variable)
    return variable

print(float_convert("1"))
