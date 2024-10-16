__all__ = ["compare_decimal_places"]

def compare_decimal_places(num1, num2):
    """
    Compares to which decimal point 2 values match. Returns True if they are an exact match.

    Parameters
    ----------
        num1 (number)
        num2 (number)
        
    Returns
    -------
        result: int or True
            If the two values are an exact match, it returns `True`. It returns integer of decimal places if they match until some decimal point.
            e.g.,
            compare_decimal_places(0.01, 0.011): 2
            compare_decimal_places(0.01, 0.01): True

    """
    if num1 == num2:
        return True

    decimal_places = 0
    while True:
        # We compare until the 20-th decimal point
        if decimal_places >= 20:
            break
        
        num1 *= 10
        num2 *= 10
        diff = abs(num1 - num2)
        
        if diff >= 1:
            break
        
        decimal_places += 1


    return decimal_places
