from chafa import *

def test_capabilities():
    db = TermDb()
    info = db.detect()

    capabilites = info.detect_capabilities()

    print(capabilites)