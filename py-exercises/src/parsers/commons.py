def swap_with_next(c: tuple, i: int) -> tuple:
    """
    swap tuple i element with the next one, return new tuple
    """
    j = i + 1
    *begin, i_val = c[:j]
    j_val, *end = c[j:]
    return (*begin, j_val, i_val, *end)
