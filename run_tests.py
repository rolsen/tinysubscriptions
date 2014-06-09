import unittest

from services.util_test import *

from controllers.descriptions_controller_test import *
from controllers.subscriptions_controller_test import *

if __name__ == '__main__':
    import tiny_subscriptions
    tiny_subscriptions.attach_blueprints()
    unittest.main()
