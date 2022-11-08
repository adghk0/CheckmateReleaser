
def _compare_version_(version1: str, version2: str) -> bool:
    result = None
    ver1_spl = version1.split('.')
    ver2_spl = version2.split('.')
    check_len = min(len(ver1_spl), len(ver2_spl))
    for p in range(0, check_len):
        ver1_p = int(ver1_spl[p]) if ver1_spl[p].isnumeric() else ver1_spl[p]
        ver2_p = int(ver2_spl[p]) if ver2_spl[p].isnumeric() else ver2_spl[p]
        if ver1_p > ver2_p:
            result = True
        elif ver1_p < ver2_p:
            result = False
        else:
            if (p == check_len - 1):
                if len(ver1_spl) > len(ver2_spl):
                    result = True
                elif len(ver1_spl) < len(ver2_spl):
                    result = False
                else:
                    result = None
            else:
                continue
    return result
