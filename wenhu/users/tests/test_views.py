#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.test import RequestFactory
from test_plus.test import TestCase

from wenhu.users.views import UserUpdateView


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.make_user()


class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        super(TestUserUpdateView, self).setUp()
        self.view = UserUpdateView()
        request = self.factory.get('/fake-url')
        print(self.factory)
        print(request)
        print(type(request))
        request.user = self.user
        self.view.request = request

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), '/users/testuser/')

    def test_get_object(self):
        self.assertEqual(self.view.get_object(), self.user)
