import valkey
from typing import List

default_glob = '&'
default_valkey_host = 'localhost'
default_valkey_port = 6379

###
# Core function
###
# Converts a permission string to an array of strings that would also provide that permission
# E.g. perm_to_list('foo.bar') = ['foo.bar', 'foo.&', 'foo.&&', '&&']
#      perm_to_list('baz.*')   = ['baz.&', 'baz.&&', '&&']
#      perm_to_list('qux.**')  = ['qux.&&', '&&']
#
#
# To guess the expected length of the returned array
# X = len(perm_raw.split('.'))
# if perm_raw ends in .**
#   len(perm_to_list) = X
# if perm_raw ends in .*
#   len(perm_to_list) = X + 2
# if perm_raw doesnt end in .** or .*
#   len(perm_to_list) = X + 3
def perm_to_list(perm_raw: str, glob: str = default_glob) -> List[str]:
    perm = perm_raw.replace('*', glob).strip('.')
    perm_split = perm.split('.')
    res = []

    if perm_split[-1] == f'{glob}{glob}':
        res.append(perm)
        perm_split.pop()
        perm_split.pop()
        perm_len = len(perm_split)
        for i in range(perm_len, -1, -1):
            perm_join = '.'.join(perm_split[:i])
            if i != 0:
                res.append(perm_join + f'.{glob}{glob}')
            else:
                res.append(f'{glob}{glob}')
    else:
        perm_len = len(perm_split)
        for i in range(perm_len, -1, -1):
            perm_join = '.'.join(perm_split[:i])
            if i == perm_len and perm_split[i-1] == glob:
                continue
            elif i == perm_len:
                res.append(perm_join)
            elif perm_len == 1:
                res.append(perm_join + f'{glob}')
                res.append(perm_join + f'{glob}{glob}')
            elif i == perm_len - 1:
                res.append(perm_join + f'.{glob}')
                res.append(perm_join + f'.{glob}{glob}')
            elif i == 0:
                res.append(f'{glob}{glob}')
            else:
                res.append(perm_join + f'.{glob}{glob}')
    return res

###
# Valkey Functions
###

# O(1)
def valkey_query_user(uid: str, host: str = default_valkey_host, port: int = default_valkey_port, db: int = 0) -> List[str]:
    print(uid)
    db = valkey.Valkey(host=host, port=port, db=db)
    # Map converts incoming b'' to ''
    x = list(map(lambda member: member.decode('utf-8'), db.smembers('user:' + uid)))
    return x

# O(1)
def valkey_query_perm(perm: str, host: str = default_valkey_host, port: int = default_valkey_port, db: int = 0) -> List[str]:
    db = valkey.Valkey(host=host, port=port, db=db)
    return list(map(lambda member: member.decode('utf-8'), db.smembers('perm:' + perm)))

# O(1)
def valkey_check(uid: str, perm: str, host: str = default_valkey_host, port: int = default_valkey_port, db: int = 0) -> bool:
    user_perms =  valkey_query_user(uid, host=host, port=port, db=db)
    perm_list = perm_to_list(perm)
    intersection = list(set(user_perms) & set(perm_list))
    if len(intersection) >= 1:
        return True
    else:
        return False

# O(2)
# O(3) if requires != ''
def valkey_set(uid: str, perm_raw: str, requires: str = '', glob: str = default_glob, host: str = default_valkey_host, port: int = default_valkey_port, db: int = 0) -> bool:
    db = valkey.Valkey(host=host, port=port, db=db)
    requires = requires.strip('.')
    perm = perm_raw.replace('*', glob).strip('.')
    if requires != '' and db.sismember('perm:' + requires, uid) or requires == '':
        db.sadd('perm:' + perm, uid)
        db.sadd('user:' + uid, perm)
        return True
    else:
        return False

###
# Alias Functions
###

vset   = valkey_set
vcheck = valkey_check
