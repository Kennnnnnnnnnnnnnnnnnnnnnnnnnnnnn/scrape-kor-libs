def stripTitle(val):
    if val.find(']') != -1:
        #print("tt %s, %d\n" % (val, val.find(']')))
        val = val.split(']', maxsplit=1)[1]
    if "합본:" in val:
        val = val.split(':', maxsplit=1)[1]
    val = val.strip()
    c = val.count(')')
    idx = val.rfind(')')
    #print("cc %d, %d, %s" % (idx, len(val), val))    #
    if c > 0 and idx == len(val) - 1:
        idx = val.rfind('(')
        val = val[:idx]
    c = val.count(':')
    if c > 0:
        arr = val.split(':', maxsplit=2)
        if len(arr) == 1:
            val = arr[0]
        elif len(arr) == 2:
            val = arr[1]
        else:
            val = arr[1] + arr[2]
    val = val.strip()
    return val