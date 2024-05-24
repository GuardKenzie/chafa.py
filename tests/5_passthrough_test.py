from chafa import *

def test_passthrough():
    config = CanvasConfig()

    through = config.passthrough
    print("Before:", through)

    config.passthrough = Passthrough.CHAFA_PASSTHROUGH_SCREEN

    print("After:", config.passthrough)

    assert config.passthrough != through