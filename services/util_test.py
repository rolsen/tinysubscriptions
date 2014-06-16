"""Tests for util functions

@author: Rory Olsen (rolsen, Gleap LLC 2014)
@license: GNU GPLv3
"""
import copy
import mox

import util

TEST_SUBSCRIPTIONS = [
    'name0',
    'name1',
    'name3'
]

TEST_DESCRIPTIONS = {
    'name0': {'description': 'description0'},
    'name1': {'description': 'description1'},
    'name2': {'description': 'description2'}
}

TEST_LISTS = {
    'name0': {'description': 'description0', 'subscribed':True},
    'name1': {'description': 'description1', 'subscribed':True},
    'name2': {'description': 'description2', 'subscribed':False}
}

TEST_NEW_LISTS = {
    'name0': {'subscribed':True},
    'name1': {'subscribed':False},
    'name2': {'subscribed':True}
}

TEST_NEW_LISTS_COERCED = [
    'name0',
    'name2'
]

TEST_NEW_SUBSCR = ['name2']
TEST_DEL_SUBSCR = ['name1', 'name3']
TEST_DIFF = {
    util.POS_DIFF_KEY: TEST_NEW_SUBSCR,
    util.NEG_DIFF_KEY: TEST_DEL_SUBSCR
}

TEST_EMAIL = 'test@example.com'
TEST_MANAGE_LISTS_URL = '/manage_lists?email=%s' % TEST_EMAIL

class UtilTests(mox.MoxTestBase):

    def test_merge_subscriptions_and_descriptions(self):
        results = util.merge_subscriptions_and_descriptions(
            TEST_SUBSCRIPTIONS,
            TEST_DESCRIPTIONS
        )
        for name, expected in TEST_LISTS.iteritems():
            self.assertTrue(results.get(name, None) != None)
            self.assertEqual(expected['description'], results[name]['description'])
            self.assertEqual(expected['subscribed'], results[name]['subscribed'])

    def test_get_diff(self):
        self.mox.StubOutWithMock(util, 'coerce_to_subscription_name_list')

        util.coerce_to_subscription_name_list(TEST_SUBSCRIPTIONS) \
            .AndReturn(TEST_SUBSCRIPTIONS)
        util.coerce_to_subscription_name_list(TEST_NEW_LISTS) \
            .AndReturn(TEST_NEW_LISTS_COERCED)

        self.mox.ReplayAll()

        results = util.get_diff(
            TEST_SUBSCRIPTIONS,
            TEST_NEW_LISTS
        )
        self.assertTrue(results.get(util.POS_DIFF_KEY, None) != None)
        self.assertTrue(results.get(util.NEG_DIFF_KEY, None) != None)

        self.assertTrue('name2' in results[util.POS_DIFF_KEY])
        self.assertTrue('name1' in results[util.NEG_DIFF_KEY])
        self.assertTrue('name3' in results[util.NEG_DIFF_KEY])

        self.assertTrue('name0' not in results[util.POS_DIFF_KEY])
        self.assertTrue('name1' not in results[util.POS_DIFF_KEY])
        self.assertTrue('name3' not in results[util.POS_DIFF_KEY])

        self.assertTrue('name0' not in results[util.NEG_DIFF_KEY])
        self.assertTrue('name2' not in results[util.NEG_DIFF_KEY])

    def test_coerce_to_subscription_name_list_no_convert(self):
        test_list = ['name0', 'name1', 'name2']
        results = util.coerce_to_subscription_name_list(test_list)
        self.assertEqual(test_list, results)

    def test_coerce_to_subscription_name_list_convert(self):
        test_dict = {
            'name0': {'subscribed': True},
            'name1': {'subscribed': False},
            'name2': {'subscribed': True}
        }
        results = util.coerce_to_subscription_name_list(test_dict)
        self.assertTrue('name0' in results)
        self.assertTrue('name1' not in results)
        self.assertTrue('name2' in results)

    def test_coerce_to_subscription_name_list_invalid_type(self):
        test_invalid_type = 'name0 name1 name2'
        self.assertRaises(
            TypeError,
            util.coerce_to_subscription_name_list,
            test_invalid_type
        )
