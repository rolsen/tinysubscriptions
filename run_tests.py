import unittest

from services.util_test import *

from controllers.descriptions_controller_test import *
from controllers.subscriptions_controller_test import *

def setup_tests():
    import tiny_subscriptions
    tiny_subscriptions.initialize_standalone()


if __name__ == '__main__':
    setup_tests()
    unittest.main()
