# -*- coding: utf-8 -*-
# Copyright (c) 2017 Vantiv eCommerce
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the 'Software'), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import unittest

package_root = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.insert(0, package_root)

from vantivsdk import *

conf = utils.Configuration()


class TestQueryTransaction(unittest.TestCase):
    def test_simple_query_transaction(self):
        transaction = fields.queryTransaction()
        transaction.orderId = '49382'
        transaction.origId = "12345"
        transaction.id = '934820'
        transaction.reportGroup = 'ThisIsAGroup'
        transaction.origActionType = "A"
        transaction.showStatusOnly = "Y"

        response = online.request(transaction, conf)
        self.assertEquals('150',
                          response['queryTransactionResponse']['response'])
        self.assertEquals('Original transaction found',
                          response['queryTransactionResponse']['message'])
        self.assertEquals('sandbox', response['queryTransactionResponse']['location'])

    def test_simple_query_transaction_with_orgActionType(self):
        transaction = fields.queryTransaction()
        transaction.orderId = '49382'
        transaction.origId = "ABCD0"
        transaction.id = '934820'
        transaction.reportGroup = 'ThisIsAGroup'
        transaction.origActionType = "FIVD"
        transaction.showStatusOnly = "Y"

        response = online.request(transaction, conf)
        self.assertEquals('151',
                          response['queryTransactionResponse']['response'])
        self.assertEquals('Original transaction not found',
                          response['queryTransactionResponse']['message'])
        self.assertEquals('sandbox', response['queryTransactionResponse']['location'])

if __name__ == '__main__':
    unittest.main()
