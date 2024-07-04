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
import datetime
conf = utils.Configuration()

# vendorCredit transaction is also getting tested in 'tests/functional/test_funding_instruction.py'
class TestVendorCredit(unittest.TestCase):
    
    def test_vendor_credit(self):
        transaction = fields.vendorCredit()
        transaction.id = 'ThisIsID'
        transaction.reportGroup = 'Default Report Group'
        transaction.fundingSubmerchantId = "value for fundingSubmerchantId"
        transaction.fundsTransferId = "value for fundsTransferId"
        transaction.vendorName = "Vantiv"
        transaction.amount = 1512

        account_info = fields.echeckTypeCtx()
        account_info.accType = 'Savings'
        account_info.accNum = "1234"
        account_info.routingNum = "12345678"

        transaction.accountInfo = account_info

        response = online.request(transaction, conf)
        self.assertEquals('000', response['vendorCreditResponse']['response'])
        self.assertEquals('sandbox', response['vendorCreditResponse']['location'])

    def test_vendor_credit_with_address(self):
        transaction = fields.vendorCredit()
        transaction.id = 'ThisIsID'
        transaction.reportGroup = 'Default Report Group'
        transaction.fundingSubmerchantId = "value for fundingSubmerchantId"
        transaction.fundsTransferId = "value for fundsTransferId"
        transaction.vendorName = "Vantiv"
        transaction.amount = 1512151215

        account_info = fields.echeckTypeCtx()
        account_info.accType = 'Savings'
        account_info.accNum = "1234"
        account_info.routingNum = "12345678"

        vendor_address = fields.address()
        vendor_address.addressLine1 = "37 Main Street"
        vendor_address.addressLine2 = ""
        vendor_address.addressLine3 = ""
        vendor_address.city = "Augusta"
        vendor_address.state = "Wisconsin"
        vendor_address.zip = "28209"
        vendor_address.country = 'USA'

        transaction.accountInfo = account_info
        transaction.vendorAddress = vendor_address

        response = online.request(transaction, conf)
        self.assertEquals('000', response['vendorCreditResponse']['response'])
        self.assertEquals('sandbox', response['vendorCreditResponse']['location'])

if __name__ == '__main__':
    unittest.main()

