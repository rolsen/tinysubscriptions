"""Tests for subscriptions_controller

@author: Rory Olsen (rolsen, Gleap LLC 2014)
@license: GNU GPLv3
"""
import copy
import json
import mox

from .. import tiny_subscriptions

from .. import services

import subscriptions_controller

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

TEST_MERGED_LISTS = {
    'name0': {'description': 'description0', 'subscribed':True},
    'name1': {'description': 'description1', 'subscribed':False},
    'name2': {'description': 'description2', 'subscribed':True}
}

TEST_NEW_SUBSCR = ['name2']
TEST_DEL_SUBSCR = ['name1']
TEST_DIFF = {
    services.util.POS_DIFF_KEY: TEST_NEW_SUBSCR,
    services.util.NEG_DIFF_KEY: TEST_DEL_SUBSCR
}

TEST_EMAIL = 'test@example.com'
TEST_MANAGE_LISTS_URL = 'mailing/manage_lists?email=%s' % TEST_EMAIL

class SubscriptionsControllerTests(mox.MoxTestBase):

    def setUp(self):
        mox.MoxTestBase.setUp(self)
        tiny_subscriptions.app.debug = True
        self.app = tiny_subscriptions.app.test_client()

    def test_manage_lists_get(self):
        self.mox.StubOutWithMock(
            services.subscriptions_service,
            'get_user_subscriptions'
        )
        self.mox.StubOutWithMock(
            services.descriptions_service,
            'get_descriptions'
        )
        self.mox.StubOutWithMock(
            services.util,
            'merge_subscriptions_and_descriptions'
        )

        services.subscriptions_service.get_user_subscriptions(TEST_EMAIL) \
            .AndReturn(TEST_SUBSCRIPTIONS)
        services.descriptions_service.get_descriptions() \
            .AndReturn(TEST_DESCRIPTIONS)
        services.util.merge_subscriptions_and_descriptions(
            TEST_SUBSCRIPTIONS,
            TEST_DESCRIPTIONS
        ).AndReturn(TEST_LISTS)

        self.mox.ReplayAll()

        result = self.app.get(TEST_MANAGE_LISTS_URL)
        self.assertEqual(200, result.status_code)
        self.assertTrue('name0' in result.data)
        self.assertTrue('description0' in result.data)
        self.assertTrue('name1' in result.data)
        self.assertTrue('description1' in result.data)
        self.assertTrue('name2' in result.data)
        self.assertTrue('description2' in result.data)

    def test_manage_lists_post(self):
        self.mox.StubOutWithMock(
            services.subscriptions_service,
            'get_user_subscriptions'
        )
        self.mox.StubOutWithMock(services.util, 'get_diff')
        self.mox.StubOutWithMock(services.subscriptions_service, 'subscribe')
        self.mox.StubOutWithMock(services.subscriptions_service, 'unsubscribe')

        services.subscriptions_service.get_user_subscriptions(TEST_EMAIL) \
            .AndReturn(TEST_SUBSCRIPTIONS)
        services.util.get_diff(
            TEST_SUBSCRIPTIONS,
            TEST_NEW_LISTS
        ).AndReturn(TEST_DIFF)
        services.subscriptions_service.subscribe(TEST_EMAIL, TEST_NEW_SUBSCR)
        services.subscriptions_service.unsubscribe(TEST_EMAIL, TEST_DEL_SUBSCR)

        self.mox.ReplayAll()

        result = self.app.post(
            TEST_MANAGE_LISTS_URL,
            data=dict(subscriptions = json.dumps(TEST_NEW_LISTS))
        )
        self.assertEqual(200, result.status_code)
