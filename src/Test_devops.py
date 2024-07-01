import devops 

def test_security():
    result = print("Authorization Granted")
    assert(result == devops.security(5,6,7))