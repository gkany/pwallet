# 最小长度5，最大长度63，
# 可以.分隔，分隔的每一部分要求以小写字母开头，以数字或小写字母结尾; 每一部分的中间部分可以为：小写字母、数字、-; 每一部分的长度5~63
MIN_ACCOUNT_NAME_LENGTH = 5
MAX_ACCOUNT_NAME_LENGTH = 63
lower_alpha = 'abcdefghijklmnopqrstuvwxyz'
def is_lower_alpha(ch):
    if lower_alpha.find(ch) == -1:
        return False
    return True

def is_valid_name(name):
    length = len(name)
    if length < MIN_ACCOUNT_NAME_LENGTH or length > MAX_ACCOUNT_NAME_LENGTH:
        return False

    begin = 0
    while True:
        end = name.find('.', begin)
        if end == -1:
            end = length
        if end - begin < MIN_ACCOUNT_NAME_LENGTH:
            return False
        
        if not is_lower_alpha(name[begin]):
            return False
        if not (is_lower_alpha(name[end-1]) or name[end-1].isdigit()):
            return False
        for index in range(begin+1, end-1):
            ch = name[index]
            if not (is_lower_alpha(ch) or ch.isdigit() or ch == '-'):
                return False
        if end == length:
            break
        begin = end + 1
    return True