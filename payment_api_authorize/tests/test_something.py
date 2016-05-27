# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class SomethingCase(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(SomethingCase, self).setUp(*args, **kwargs)

        # TODO Replace this for something useful or delete this method
        self.do_something_before_all_tests()

    def tearDown(self, *args, **kwargs):
        # TODO Replace this for something useful or delete this method
        self.do_something_after_all_tests()

        super(SomethingCase, self).tearDown(*args, **kwargs)

    def test_something(self):
        """First line of docstring appears in test logs.
        Other lines do not.
        Any method starting with ``test_`` will be tested.
        """
        pass
