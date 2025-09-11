from quickperms.quickperms import *
import valkey
dbn = 9
db = valkey.Valkey(host='localhost', port=6379, db=dbn)

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

def test_valkey_set_writes_user_and_perm_keys():
    valkey_set('testuser', 'x.y.z', db=dbn)
    assert db.sismember('user:testuser', 'x.y.z')
    assert db.sismember('perm:x.y.z', 'testuser')

    # Test single glob replacement
    valkey_set('testuser', 'a.b.*', glob='&', db=dbn)
    assert db.sismember('user:testuser', 'a.b.&')
    assert db.sismember('perm:a.b.&', 'testuser')

    # Test double glob replacement
    valkey_set('testuser', '1.2.**', glob='&', db=dbn)
    assert db.sismember('user:testuser', '1.2.&&')
    assert db.sismember('perm:1.2.&&', 'testuser')

def test_valkey_query_user_expected_output():
    assert valkey_query_user('testuser', db=dbn) == ['x.y.z', 'a.b.&', '1.2.&&']

def test_valkey_query_perm_expected_output():
    assert valkey_query_perm('x.y.z', db=dbn) == ['testuser']
    assert valkey_query_perm('a.b.&', db=dbn) == ['testuser']
    assert valkey_query_perm('1.2.&&', db=dbn) == ['testuser']
    
def test_valkey_check_expected_output_and_globbing():
    # Test expected output for permission 'x.y.z'
    assert valkey_check('testuser', 'x.y.z', db=dbn)
    assert valkey_check('testuser', 'x.y.z.a', db=dbn) == False

    # Test expected output for permission 'a.b.*'
    assert valkey_check('testuser', 'a.b.c', db=dbn)
    assert valkey_check('testuser', 'a.b.q', db=dbn)
    assert valkey_check('testuser', 'a.b.c.d', db=dbn) == False

    # Test expected output for permission '1.2.**'
    assert valkey_check('testuser', '1.2.3', db=dbn)
    assert valkey_check('testuser', '1.2.3.4', db=dbn)
    assert valkey_check('testuser', '1.2', db=dbn) == False

# Comment this out to inspect test db with redis insight
def test_valkey_post_flush_db():
    db.flushdb()
