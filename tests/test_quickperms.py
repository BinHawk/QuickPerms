import os
os.environ['VALKEY_HOST'] = 'localhost'
os.environ['VALKEY_PORT'] = '6379'
os.environ['VALKKEY_DB'] = '9'
#os.environ['VALKKEY_PASS'] =  ''

from quickperms.quickperms import *
import valkey

print(os.getenv('VALKEY_HOST'))
print(int(os.getenv('VALKEY_PORT', '500')))
print(int(os.getenv('VALKKEY_DB', '501')))
print(os.getenv('VALKKEY_PASS'))

def test_valkey_pre_flush_db():
    db.flushdb()

def test_perm_to_list_expected_output():
    assert perm_to_list('x.y.z', glob='&') == ['x.y.z', 'x.y.&', 'x.y.&&', 'x.&&', '&&']
    # Test command with no '.' or splits
    assert perm_to_list('x', glob='&') == ['x', '&', '&&']
    # Test output ending in .*
    assert perm_to_list('bar.*', glob='&') == ['bar.&', 'bar.&&', '&&']
    # Test output ending in .**
    assert perm_to_list('foo.**', glob='&') == ['foo.&&', '&&']
    # Test different glob input
    assert perm_to_list('x', glob='^') == ['x', '^', '^^']
    assert perm_to_list('y.*', glob='^') == ['y.^', 'y.^^', '^^']
    assert perm_to_list('z.**', glob='^') == ['z.^^', '^^']

def test_valkey_set_writes_user_and_perm_keys():
    valkey_set('testuser', 'x.y.z')
    assert db.sismember('user:testuser', 'x.y.z')
    assert db.sismember('perm:x.y.z', 'testuser')

    # Test single glob replacement
    valkey_set('testuser', 'a.b.*', glob='&')
    assert db.sismember('user:testuser', 'a.b.&')
    assert db.sismember('perm:a.b.&', 'testuser')

    # Test double glob replacement
    valkey_set('testuser', '1.2.**', glob='&')
    assert db.sismember('user:testuser', '1.2.&&')
    assert db.sismember('perm:1.2.&&', 'testuser')

def test_valkey_get_user_perms_expected_output():
    assert valkey_get_user_perms('testuser') == ['x.y.z', 'a.b.&', '1.2.&&']

def test_valkey_get_perm_users_expected_output():
    assert valkey_get_perm_users('x.y.z') == ['testuser']
    assert valkey_get_perm_users('a.b.&') == ['testuser']
    assert valkey_get_perm_users('1.2.&&') == ['testuser']
    
def test_valkey_check_user_by_get_expected_output_and_globbing():
    # Test expected output for permission 'x.y.z'
    assert valkey_check_user_by_get('testuser', 'x.y.z')
    assert valkey_check_user_by_get('testuser', 'x.y.z.a') == False

    # Test expected output for permission 'a.b.*'
    assert valkey_check_user_by_get('testuser', 'a.b.c')
    assert valkey_check_user_by_get('testuser', 'a.b.q')
    assert valkey_check_user_by_get('testuser', 'a.b.c.d') == False

    # Test expected output for permission '1.2.**'
    assert valkey_check_user_by_get('testuser', '1.2.3')
    assert valkey_check_user_by_get('testuser', '1.2.3.4')
    assert valkey_check_user_by_get('testuser', '1') == False
    assert valkey_check_user_by_get('testuser', '1.2') == False
    assert valkey_check_user_by_get('testuser', '1.2.*')
    assert valkey_check_user_by_get('testuser', '1.2.**')
    assert valkey_check_user_by_get('testuser', '1.2.3.*')
    assert valkey_check_user_by_get('testuser', '1.2.3.**')

def test_valkey_delete_expected_output():
    db.flushdb()
