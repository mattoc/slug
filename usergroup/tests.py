#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

import cStringIO as StringIO
import datetime
import os
import re
import socket
import subprocess
import sys

import django.test.simple

from django_testing_fixes import suite as fix_suite
from django_testing_fixes import fix_finish_response, fix_finish_request
from django_testing_fixes import fix_fixtures
from django_testing_fixes import fix_exceptions

from usergroup.test_utils import display_servers
from usergroup import event_lists

class UserGroupTestSuiteRunner(fix_suite.TestSuiteRunner):
    """A test suite runner which can use a display."""

    def run_tests(self, *args, **kw):
        TEST_DISPLAY = os.environ.get('TEST_DISPLAY', '')

        convenient_date = datetime.datetime(2012, 03, 20)
        def convenient_date_func(**kw):
            return convenient_date.replace(**kw)

        event_lists.get_date = convenient_date_func

        if TEST_DISPLAY:
            if TEST_DISPLAY in ('1', 'True'):
                server = display_servers.RealDisplay()
            else:
                server = display_servers.VNCDisplay()
            with server:
                return fix_suite.TestSuiteRunner.run_tests(self, *args, **kw)
        else:
            #No display needed, just use the normal runner
            return django.test.simple.DjangoTestSuiteRunner.run_tests(self,
                    *args, **kw)

suite = fix_suite.create_suite(os.path.dirname(__file__), 'usergroup')
