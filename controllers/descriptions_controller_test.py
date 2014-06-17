"""Tests for descriptions_controller.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
@license: GNU GPLv3
"""
import copy
import json
import mox

import tiny_subscriptions

from .. import services

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

TEST_DATA = {'descriptions': json.dumps(TEST_DESCRIPTIONS)}

class DescriptionsControllerTests(mox.MoxTestBase):

    def setUp(self):
        mox.MoxTestBase.setUp(self)
        tiny_subscriptions.app.debug = True
        self.app = tiny_subscriptions.app.test_client()

    def test_get_lists(self):
        self.mox.StubOutWithMock(
            services.descriptions_service, 'get_descriptions')
        self.mox.StubOutWithMock(services.subscriptions_service, 'get_lists')

        services.descriptions_service.get_descriptions().AndReturn(
            TEST_DESCRIPTIONS)
        services.subscriptions_service.get_lists().AndReturn(TEST_SUBSCRIPTIONS)

        self.mox.ReplayAll()

        result = self.app.get('/mailing/admin_lists')
        self.assertEqual(200, result.status_code)
        self.assertTrue('name0' in result.data)
        self.assertTrue('name1' in result.data)
        self.assertTrue('name3' in result.data)
        self.assertTrue('name2' not in result.data)

    def test_update_lists(self):
        self.mox.StubOutWithMock(
            services.descriptions_service,
            'update_descriptions'
        )
        services.descriptions_service.update_descriptions(TEST_DESCRIPTIONS)

        self.mox.ReplayAll()

        result = self.app.post('/mailing/admin_lists', data = TEST_DATA)
        self.assertEqual(200, result.status_code)
