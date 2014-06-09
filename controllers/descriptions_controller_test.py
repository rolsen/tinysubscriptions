"""Tests for descriptions_controller.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
@license: GNU GPLv3
"""
import copy
import mox

import tiny_subscriptions

class DescriptionsTests(mox.MoxTestBase):

    def setUp(self):
        mox.MoxTestBase.setUp(self)
        tiny_subscriptions.app.debug = True
        self.app = tiny_subscriptions.app.test_client()

    def test_stuuuuuff(self):
        # self.mox.ReplayAll()

        # result = self.app.get(TEST_MANAGE_LISTS_URL)
        # self.assertEqual(200, result.status_code)
        print "descriptions_controller_test Stub"
