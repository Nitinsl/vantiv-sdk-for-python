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
import time
import filecmp
from subprocess import call

package_root = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.insert(0, package_root)

from vantivsdk import *
from vantivsdk import (batch, pgp_helper)

import datetime

conf = utils.Configuration()

preliveStatus = "down"
if "preliveStatus" in os.environ:
   preliveStatus = os.environ['preliveStatus']
else:
   print("preliveStatus environment variable is not defined. Defaulting to down.")

class TestBatch(unittest.TestCase):

    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_submit(self):
        # Initial Transactions container
        transactions = batch.Transactions()
        # Transactions presented by dict
        txn_dict = {
            'authorization':{
                'reportGroup': 'Planets',
                'orderId': '12344',
                'amount': '106',
                'orderSource': 'ecommerce',
                'id': 'thisisid',
                'card': {
                    'expDate': '1210',
                    'number': '4100000000000000',
                    'type': 'VI',
                }
            }
        }
        transactions.add(txn_dict)

        # Card
        card = fields.cardType()
        card.number = '4457010000000009'
        card.expDate = '0121'
        card.cardValidationNum = '349'
        card.type = 'VI'

        # eCheck
        # echeck = fields.echeck()
        # echeck.accType = 'Checking'
        # echeck.accNum = '4099999992'
        # echeck.routingNum = '011075150'

        # billtoaddress
        billtoaddress = fields.contact()
        billtoaddress.firstName = 'Mike'
        billtoaddress.middleInitial = 'J'
        billtoaddress.lastName = 'Hammer'
        billtoaddress.phone = '999-999-9999'

        # Initial authorization
        authorization = fields.authorization()
        authorization.orderId = '1'
        authorization.amount = 10010
        authorization.reportGroup = 'Planets'
        authorization.orderSource = 'ecommerce'
        authorization.card = card
        authorization.billtoaddress = billtoaddress
        authorization.id = 'thisisid'
        authorization.businessIndicator = 'agentCashOut'
        authorization.orderChannel = 'SMART_TV'
        authorization.fraudCheckAction = 'APPROVED_SKIP_FRAUD_CHECK'

        customerInfo = fields.customerInfo()

        customerInfo.accountUserName = 'Jack'
        customerInfo.userAccountNumber = '1234'
        customerInfo.userAccountEmail = 'gmail@gmail.com'
        customerInfo.membershipId = '11111'
        customerInfo.membershipPhone = '123456'
        customerInfo.membershipEmail = 'gmail@gmail.com'
        customerInfo.membershipName = 'fran'
        customerInfo.accountCreatedDate = datetime.datetime.now().strftime("%Y-%m-%d")
        customerInfo.userAccountPhone = '000461223'

        authorization.customerInfo = customerInfo
        detailTaxList = list()
        detailTax = fields.detailTax()
        detailTax.taxAmount = 100
        detailTax2 = fields.detailTax()
        detailTax2.taxAmount = 200
        detailTaxList.append(detailTax)
        detailTaxList.append(detailTax2)
        lineItemDataList = list()
        lineItemData = fields.lineItemData()
        lineItemData.itemDescription = 'des'
        lineItemData.itemCategory = 'Chock'
        lineItemData.itemCategory = 'Chock'
        lineItemData.itemSubCategory = 'pen'
        lineItemData.productId = '001'
        lineItemData.productName = 'prod'
        lineItemDataList.append(lineItemData)
        enhancedData = fields.enhancedData()
        enhancedData.detailTax = detailTaxList
        enhancedData.lineItemData = lineItemDataList
        enhancedData.discountCode = '001'
        enhancedData.discountPercent = '10'
        enhancedData.fulfilmentMethodType = 'STANDARD_SHIPPING'

        authorization.enhancedData = enhancedData

        additionalCOFData = fields.additionalCOFData()
        additionalCOFData.totalPaymentCount = '35'
        additionalCOFData.paymentType = 'Fixed Amount'
        additionalCOFData.uniqueId = '12345wereew233'
        additionalCOFData.frequencyOfMIT = 'BiWeekly'
        additionalCOFData.validationReference = 're3298rhriw4wrw'
        additionalCOFData.sequenceIndicator = '2'

        authorization.additionalCOFData = additionalCOFData

        contact = fields.contact()
        contact.name = 'john & Mary Smith'
        contact.addressLine1 = '1st Main Street'
        contact.city = 'Burlington'
        contact.state = 'MA'
        contact.zip = '01867-4456'
        contact.country = 'USA'

        authorization.retailerAddress = contact

        authorization.businessIndicator = 'consumerBillPayment'
        authorization.crypto = False
        authorization.checkoutId = '123tyhgr34'
        authorization.orderChannel = 'PHONE'
        authorization.fraudCheckStatus = 'Not Approved'

        # Create accountFundingTransactionData
        accountfundingtransactiondata = fields.accountFundingTransactionData()
        accountfundingtransactiondata.receiverLastName = 'Smith'
        accountfundingtransactiondata.receiverState = 'AZ'
        accountfundingtransactiondata.receiverCountry = 'USA'
        accountfundingtransactiondata.receiverAccountNumber = '1234567890'
        accountfundingtransactiondata.accountFundingTransactionType = 'walletTransfer'
        accountfundingtransactiondata.receiverAccountNumberType = 'cardAccount'

        authorization.accountFundingTransactionData = accountfundingtransactiondata

        # Add transaction to container
        transactions.add(authorization)

        # Initial authorization
        authorization2 = fields.authorization()
        authorization2.orderId = '2'
        authorization2.amount = 1001
        authorization2.reportGroup = 'Planets'
        authorization2.orderSource = 'ecommerce'
        authorization2.card = card
        authorization2.billtoaddress = billtoaddress
        authorization2.id = 'thisisid'
        # Add transaction to container
        transactions.add(authorization2)

        # Inital authorization with lodging info
        authorization3 = fields.authorization()
        authorization3.orderId = '2'
        authorization3.amount = 0
        authorization3.reportGroup = 'Planets'
        authorization3.orderSource = 'ecommerce'
        authorization3.card = card
        authorization3.billtoaddress = billtoaddress
        authorization3.id = 'thisisid'
        lodging_info = fields.lodgingInfo()
        lodging_info.roomRate = 1001
        lodging_info.roomTax = 1
        lodging_charge = fields.lodgingCharge()
        lodging_charge.name = "RESTAURANT"
        lodging_info.lodgingCharge = [lodging_charge]
        authorization3.lodgingInfo = lodging_info
        # Add transaction to container
        transactions.add(authorization3)

        # Initial authorization
        sale = fields.sale()
        sale.orderId = '1'
        sale.amount = 10010
        sale.reportGroup = 'Planets'
        sale.orderSource = 'ecommerce'
        sale.card = card
        sale.billtoaddress = billtoaddress
        sale.id = 'thisisid'

        # Create accountFundingTransactionData
        accountfundingtransactiondata = fields.accountFundingTransactionData()
        accountfundingtransactiondata.receiverLastName = 'Smith'
        accountfundingtransactiondata.receiverState = 'CA'
        accountfundingtransactiondata.receiverCountry = 'USA'
        accountfundingtransactiondata.receiverAccountNumber = '12343564'
        accountfundingtransactiondata.receiverAccountNumberType = 'RTNAndBAN'
        accountfundingtransactiondata.accountFundingTransactionType = 'businessDisbursement'

        sale.accountFundingTransactionData = accountfundingtransactiondata
        sale.fraudCheckAction = 'APPROVED_SKIP_FRAUD_CHECK'
        sale.businessIndicator = 'rapidMerchantSettlement'
        sale.orderChannel = 'SMART_TV'


        # Add pinless debit request
        pinless_debit = fields.pinlessDebitRequestType()
        preferred_network = fields.preferredDebitNetworksType()
        preferred_network.debitNetworkName = ['Visa', 'MasterCard']
        pinless_debit.preferredDebitNetworks = preferred_network
        pinless_debit.routingPreference = 'regular'
        sale.pinlessDebitRequest = pinless_debit
        # Add transaction to container
        transactions.add(sale)

        # Initial translate to low value token request
        translateToLow = fields.translateToLowValueTokenRequest()
        translateToLow.orderId = '1'
        translateToLow.token = 'gf5a4f564g6a'
        translateToLow.reportGroup = 'Planets'
        translateToLow.id = 'thisisid'
        # Add transaction to container
        transactions.add(translateToLow)

        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # stream to Vaitiv eCommerce and get object as response
        response = batch.submit(transactions, conf, filename)

        if conf.useEncryption:
            # Using encryption.
            retry = True
            tried = 0
            withEncryptionReponseFilepath = ''
            while retry:
                tried += 1
                try:
                    withEncryptionReponseFilepath = batch._get_file_from_sftp(response, conf, False, 60)
                    retry = False
                except:
                    # sleep 1 minute waiting for batch get processed
                    print("sleep 30 seconds waiting for batch get processed")
                    time.sleep(30)
                if tried > 20:
                    self.fail("Timeout for retrieve batch response")
                    break        

            call(["cat", withEncryptionReponseFilepath])
            ### <<< WITH ENCRYPTION

            with open(withEncryptionReponseFilepath, 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals("Valid Format", obj.message)

        else:
            with open(os.path.join(conf.batch_requests_path, '%s.xml' % filename), 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals(1, obj.numBatchRequests)
                self.assertEquals(11117, obj.batchRequest[0].authAmount)

            self.assertEquals('%s.xml.asc' % filename, response)

    #vvvvv
    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_rfr(self):
        # Initial Transactions container
        transactions = batch.Transactions()
        transactions.sameDayFunding = True

        # Card
        card = fields.cardType()
        card.number = '4457010000000009'
        card.expDate = '0121'
        card.cardValidationNum = '349'
        card.type = 'VI'

        # eCheck
        # echeck = fields.echeck()
        # echeck.accType = 'Checking'
        # echeck.accNum = '4099999992'
        # echeck.routingNum = '011075150'

        # billtoaddress
        billtoaddress = fields.contact()
        billtoaddress.firstName = 'Mike'
        billtoaddress.middleInitial = 'J'
        billtoaddress.lastName = 'Hammer'
        billtoaddress.phone = '999-999-9999'

        # Initial authorization
        authorization = fields.authorization()
        authorization.orderId = '1'
        authorization.amount = 10010
        authorization.reportGroup = 'Planets'
        authorization.orderSource = 'ecommerce'
        authorization.card = card
        authorization.billtoaddress = billtoaddress
        authorization.id = 'thisisid'
        authorization.businessIndicator = 'businessToBusinessTransfer'
        authorization.orderChannel = 'SCAN_AND_GO'
        authorization.fraudCheckAction = 'DECLINED_NEED_FRAUD_CHECK'

        # Create accountFundingTransactionData
        accountfundingtransactiondata = fields.accountFundingTransactionData()
        accountfundingtransactiondata.receiverLastName = 'Stephen'
        accountfundingtransactiondata.receiverState = 'CA'
        accountfundingtransactiondata.receiverCountry = 'USA'
        accountfundingtransactiondata.receiverAccountNumber = '4987335624'
        accountfundingtransactiondata.receiverAccountNumberType = 'walletID'
        accountfundingtransactiondata.accountFundingTransactionType = 'payrollDisbursement'

        authorization.accountFundingTransactionData = accountfundingtransactiondata

        # Add transaction to container
        transactions.add(authorization)

        # Initial authorization
        authorization2 = fields.authorization()
        authorization2.orderId = '2'
        authorization2.amount = 1001
        authorization2.reportGroup = 'Planets'
        authorization2.orderSource = 'ecommerce'
        authorization2.card = card
        authorization2.billtoaddress = billtoaddress
        authorization2.id = 'thisisid'
        # Add transaction to container
        transactions.add(authorization2)

        # Initial authorization
        sale = fields.sale()
        sale.orderId = '1'
        sale.amount = 10010
        sale.reportGroup = 'Planets'
        sale.orderSource = 'ecommerce'
        sale.card = card
        sale.billtoaddress = billtoaddress
        sale.id = 'thisisid'
        sale.accountFundingTransactionData = accountfundingtransactiondata
        sale.fraudCheckAction = 'APPROVED_SKIP_FRAUD_CHECK'
        sale.businessIndicator = 'rapidMerchantSettlement'
        sale.orderChannel = 'SMART_TV'

        # Add transaction to container
        transactions.add(sale)

        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # stream to Vaitiv eCommerce and get object as response
        response_filename = batch.submit(transactions, conf, filename)
        self.assertEquals('%s.xml.asc' % filename, response_filename)

        response = {}


        # Example for RFRRequest
        RFRRequest = fields.RFRRequest()

        retry = True
        tried = 0
        while retry:
            tried += 1
            try:
                response = batch.retrieve(response_filename, conf)
                retry = False
                RFRRequest.cnpSessionId = response['@cnpSessionId']
            except:
                # sleep 1 minute waiting for batch get processed
                print("sleep 30 seconds waiting for batch get processed")
                time.sleep(30)
            if tried > 20:
                self.fail("Timeout for retrieve batch response")
                break

        enhancedData = fields.enhancedData()
        enhancedData.fulfilmentMethodType = 'STANDARD_SHIPPING'
        transactions.enhancedData = enhancedData

        transactions = batch.Transactions()
        transactions.add(RFRRequest)

        # submit batch request
        response_rfr_filename = batch.submit(transactions, conf)

        retry = True
        tried = 0
        while retry:
            tried += 1
            try:
                # retrieve rfr batch request
                response_rfr = batch.retrieve(response_rfr_filename, conf)
                retry = False
                self.assertIn('batchResponse', response_rfr)
                self.assertEquals(response_rfr['batchResponse']['authorizationResponse'][0]['cnpTxnId'],
                                  response['batchResponse']['authorizationResponse'][0]['cnpTxnId'])
            except:
                # sleep 1 minute waiting for batch get processed
                print("sleep 30 seconds waiting for rfr batch get processed")
                time.sleep(30)
            if tried > 20:
                self.fail("Timeout for retrieve rfr batch response")
                break

    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_dict(self):
        txn_dict = {
            'authorization':[
                {
                    'reportGroup': 'Planets',
                    'orderId': '12344',
                    'amount': '100',
                    'orderSource': 'ecommerce',
                    'id': 'thisisid',
                    'accountFundingTransactionData': {
                        'receiverLastName': 'Smith',
                        'receiverState': 'CA',
                        'receiverCountry': 'USA',
                        'receiverAccountNumber': '12343564',
                        'receiverAccountNumberType': 'RTNAndBAN',
                        'accountFundingTransactionType': 'businessDisbursement'
                    },
                    'fraudCheckAction': 'APPROVED_SKIP_FRAUD_CHECK',
                    'businessIndicator': 'rapidMerchantSettlement',
                    'orderChannel': 'SMART_TV',
                    'card': {
                        'expDate': '1210',
                        'number': '4457010000000009',
                        'type': 'VI',
                    }
                },
                {
                    'reportGroup': 'Planets',
                    'orderId': '12345',
                    'amount': '200',
                    'orderSource': 'ecommerce',
                    'id': 'thisisid',
                    'card': {
                        'expDate': '1210',
                        'number': '4457010000000009',
                        'type': 'VI',
                    }
                },
                {
                    'reportGroup': 'Planets',
                    'orderId': '12346',
                    'amount': '300',
                    'orderSource': 'ecommerce',
                    'id': 'thisisid',
                    'card': {
                        'expDate': '1210',
                        'number': '4457010000000009',
                        'type': 'VI',
                    }
                },
                {
                    'reportGroup': 'Planets',
                    'orderId': '12347',
                    'amount': '300',
                    'orderSource': 'ecommerce',
                    'id': 'thisisid',
                    'card': {
                        'expDate': '1210',
                        'number': '4457010000000009',
                        'type': 'VI',
                    },
                    'lodgingInfo': {
                        'roomRate': '1001',
                        'roomTax': '1',
                        'lodgingCharge': [{'name': 'OTHER'}],
                    }
                }
            ],
            'sale': [
                {
                    'reportGroup': 'Planets',
                    'orderId': '12344',
                    'amount': '106',
                    'orderSource': 'ecommerce',
                    'id': 'thisisid',
                    'accountFundingTransactionData': {
                        'receiverLastName': 'Smith',
                        'receiverState': 'CA',
                        'receiverCountry': 'USA',
                        'receiverAccountNumber': '12343564',
                        'receiverAccountNumberType': 'RTNAndBAN',
                        'accountFundingTransactionType': 'businessDisbursement'
                    },
                    'fraudCheckAction': 'APPROVED_SKIP_FRAUD_CHECK',
                    'businessIndicator': 'rapidMerchantSettlement',
                    'orderChannel': 'SMART_TV',
                    'card': {
                        'expDate': '1210',
                        'number': '4457010000000009',
                        'type': 'VI',
                    }
                },
                {
                    'reportGroup': 'Planets',
                    'orderId': '12354',
                    'amount': '106',
                    'orderSource': 'ecommerce',
                    'id': 'thisisid',
                    'card': {
                        'expDate': '1210',
                        'number': '4457010000000009',
                        'type': 'VI',
                    },
                    # 'pinlessDebitRequest': {
                    #     'routingPreference': 'regular',
                    #     'preferredDebitNetworks': {'debitNetworkName': ['visa']}
                    # }
                }
            ],
            #'translateToLowValueTokenRequest': {
            #    'reportGroup': 'Planets',
            #    'orderId': '12344',
            #    'id': 'thisisid',
            #    'token': 'g45a684fw54f'
            #}
        }

        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # stream to Vaitiv eCommerce and get object as response
        response_filename = batch.submit(txn_dict, conf, filename)
        self.assertEquals('%s.xml.asc' % filename, response_filename)

        response = {}


        # Example for RFRRequest
        RFRRequest = fields.RFRRequest()

        retry = True
        tried = 0
        while retry:
            tried += 1
            try:
                response = batch.retrieve(response_filename, conf)
                print("batch.retrieve() ok")
                retry = False
                RFRRequest.cnpSessionId = response['@cnpSessionId']
            except utils.VantivException as ex:
                # sleep 1 minute waiting for batch get processed
                print(ex)
                print("sleep 30 seconds waiting for batch get processed")
                time.sleep(30)
            if tried > 20:
                self.fail("Timeout for retrieve batch response")
                break

        transactions = batch.Transactions()
        transactions.add(RFRRequest)

        # submit batch request
        response_rfr_filename = batch.submit(transactions, conf)

        retry = True
        tried = 0
        while retry:
            tried += 1
            try:
                # retrieve rfr batch request
                response_rfr = batch.retrieve(response_rfr_filename, conf)
                retry = False
                self.assertIn('batchResponse', response_rfr)
                self.assertEquals(response_rfr['batchResponse']['authorizationResponse'][0]['cnpTxnId'],
                                  response['batchResponse']['authorizationResponse'][0]['cnpTxnId'])
            except:
                # sleep 1 minute waiting for batch get processed
                print("sleep 30 seconds waiting for rfr batch get processed")
                time.sleep(30)
            if tried > 20:
                self.fail("Timeout for retrieve rfr batch response")
                break

    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_mix_transaction_recurringtransaction(self):
        txn_dict = {
            'sameDayFunding': 0,
            'authorization':[
                {
                    'reportGroup': 'Planets',
                    'orderId': '12344',
                    'amount': '100',
                    'orderSource': 'ecommerce',
                    'id': 'thisisid',
                    'card': {
                        'expDate': '1210',
                        'number': '4100000000000000',
                        'type': 'VI',
                    }
                },
                {
                    'reportGroup': 'Planets',
                    'orderId': '12345',
                    'amount': '200',
                    'orderSource': 'ecommerce',
                    'id': 'thisisid',
                    'card': {
                        'expDate': '1210',
                        'number': '4100000000000000',
                        'type': 'VI',
                    }
                },
                {
                    'reportGroup': 'Planets',
                    'orderId': '12346',
                    'amount': '300',
                    'orderSource': 'ecommerce',
                    'id': 'thisisid',
                    'card': {
                        'expDate': '1210',
                        'number': '4100000000000000',
                        'type': 'VI',
                    }
                }
            ],
            'sale': {
                'reportGroup': 'Planets',
                'orderId': '12344',
                'amount': '106',
                'orderSource': 'ecommerce',
                'id': 'thisisid',
                'card': {
                    'expDate': '1210',
                    'number': '4100000000000000',
                    'type': 'VI',
                }
            },
            'createPlan': {
                'amount': '106',
                'planCode': '1',
                'name': 'plan name',
                'description': 'plan description',
                'intervalType': 'ANNUAL'
            }
        }

        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # stream to Vaitiv eCommerce and get object as response
        response_filename = batch.submit(txn_dict, conf, filename)
        self.assertEquals('%s.xml.asc' % filename, response_filename)

        response = {}


        # Example for RFRRequest
        RFRRequest = fields.RFRRequest()

        retry = True
        tried = 0
        while retry:
            tried += 1
            try:
                response = batch.retrieve(response_filename, conf)
                retry = False
                RFRRequest.cnpSessionId = response['@cnpSessionId']
            except:
                # sleep 1 minute waiting for batch get processed
                print("sleep 30 seconds waiting for batch get processed")
                time.sleep(30)
            if tried > 20:
                self.fail("Timeout for retrieve batch response")
                break

        transactions = batch.Transactions()
        transactions.sameDayFunding = True
        transactions.add(RFRRequest)

        # submit batch request
        response_rfr_filename = batch.submit(transactions, conf)

        retry = True
        tried = 0
        while retry:
            tried += 1
            try:
                # retrieve rfr batch request
                response_rfr = batch.retrieve(response_rfr_filename, conf)
                retry = False
                self.assertIn('batchResponse', response_rfr)
                self.assertEquals(response_rfr['batchResponse'][0]['authorizationResponse'][0]['cnpTxnId'],
                                  response['batchResponse'][0]['authorizationResponse'][0]['cnpTxnId'])
                self.assertEquals(response_rfr['batchResponse'][1]['createPlanResponse']['cnpTxnId'],
                                  response['batchResponse'][1]['createPlanResponse']['cnpTxnId'])
            except:
                # sleep 1 minute waiting for batch get processed
                print("sleep 30 seconds waiting for rfr batch get processed")
                time.sleep(30)
            if tried > 20:
                self.fail("Timeout for retrieve rfr batch response")
                break

    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_deposit_txn_reversal(self):
        txnBatch = batch.Transactions()
        txnRev = fields.depositTransactionReversal();
        txnRev.reportGroup = 'Planets'
        txnRev.customerId = '987654321'
        txnRev.cnpTxnId = '12345678000'
        txnRev.amount = 106
        txnRev.orderSource = 'ecommerce'
        txnRev.id = 'thisisid'
        txnRev.pin = '123456'

        detailTaxList = list()
        detailTax = fields.detailTax()
        detailTax.taxAmount = 100
        detailTax2 = fields.detailTax()
        detailTax2.taxAmount = 200
        detailTaxList.append(detailTax)
        detailTaxList.append(detailTax2)
        lineItemDataList = list()
        lineItemData = fields.lineItemData()
        lineItemData.itemDescription = 'des'
        lineItemData.itemCategory = 'Chock'
        lineItemData.itemCategory = 'Chock'
        lineItemData.itemSubCategory = 'pen'
        lineItemData.productId = '001'
        lineItemData.productName = 'prod'
        lineItemDataList.append(lineItemData)
        enhancedData = fields.enhancedData()
        enhancedData.detailTax = detailTaxList
        enhancedData.lineItemData = lineItemDataList
        enhancedData.discountCode = '001'
        enhancedData.discountPercent = '10'
        enhancedData.fulfilmentMethodType = 'STANDARD_SHIPPING'

        txnBatch.add(txnRev)

        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # stream to Vaitiv eCommerce and get object as response
        response = batch.submit(txnBatch, conf, filename)

        if conf.useEncryption:
            # Using encryption.
            retry = True
            tried = 0
            withEncryptionReponseFilepath = ''
            while retry:
                tried += 1
                try:
                    withEncryptionReponseFilepath = batch._get_file_from_sftp(response, conf, False, 60)
                    retry = False
                except:
                    # sleep 1 minute waiting for batch get processed
                    print("sleep 30 seconds waiting for batch get processed")
                    time.sleep(30)
                if tried > 20:
                    self.fail("Timeout for retrieve batch response")
                    break

            call(["cat", withEncryptionReponseFilepath])
            ### <<< WITH ENCRYPTION

            with open(withEncryptionReponseFilepath, 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals("Valid Format", obj.message)

        else:
            with open(os.path.join(conf.batch_requests_path, '%s.xml' % filename), 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals(1, obj.numBatchRequests)
                self.assertEquals(106, obj.batchRequest[0].depositTransactionReversalAmount)

            self.assertEquals('%s.xml.asc' % filename, response)

    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_credit_txn_reversal(self):
        txnBatch = batch.Transactions()
        refund_txn_rev = fields.refundTransactionReversal()
        refund_txn_rev.reportGroup = 'Planets'
        refund_txn_rev.customerId = '987654321'
        refund_txn_rev.cnpTxnId = '12345678000'
        refund_txn_rev.amount = 106
        refund_txn_rev.orderSource = 'ecommerce'
        refund_txn_rev.id = 'thisisid'
        refund_txn_rev.pin = '123456'
        txnBatch.add(refund_txn_rev)

        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # stream to Vaitiv eCommerce and get object as response
        response = batch.submit(txnBatch, conf, filename)

        if conf.useEncryption:
            # Using encryption.
            retry = True
            tried = 0
            withEncryptionReponseFilepath = ''
            while retry:
                tried += 1
                try:
                    withEncryptionReponseFilepath = batch._get_file_from_sftp(response, conf, False, 60)
                    retry = False
                except:
                    # sleep 1 minute waiting for batch get processed
                    print("sleep 30 seconds waiting for batch get processed")
                    time.sleep(30)
                if tried > 20:
                    self.fail("Timeout for retrieve batch response")
                    break

            call(["cat", withEncryptionReponseFilepath])
            ### <<< WITH ENCRYPTION

            with open(withEncryptionReponseFilepath, 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals("Valid Format", obj.message)

        else:
            with open(os.path.join(conf.batch_requests_path, '%s.xml' % filename), 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals(1, obj.numBatchRequests)
                self.assertEquals(106, obj.batchRequest[0].refundTransactionReversalAmount)

            self.assertEquals('%s.xml.asc' % filename, response)

    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_auth_sale_v12_30(self):
        txnBatch = batch.Transactions()
        authorization = fields.authorization()
        authorization.id = '1'
        authorization.customerId = 'Cust0403'
        authorization.reportGroup = 'Default Report Group'
        authorization.orderId = '12344401'
        authorization.amount = 106
        authorization.orderSource = 'ecommerce'

        seller_info = fields.sellerInfo()
        seller_info.accountNumber = '4485581000000005'
        seller_info.aggregateOrderCount = '4'
        seller_info.aggregateOrderDollars = '104'
        seller_address = fields.sellerAddress()
        seller_address.sellerStreetaddress = '15 Main Street'
        seller_address.sellerUnit = '100 AB'
        seller_address.sellerPostalcode = '12345'
        seller_address.sellerCity = 'San Jose'
        seller_address.sellerProvincecode = 'MA'
        seller_address.sellerCountrycode = 'US'
        seller_info.sellerAddress = seller_address
        seller_info.createdDate = '2015-11-12T20:33:09'
        seller_info.domain = 'vap'
        seller_info.email = 'bob@example.com'
        seller_info.lastUpdateDate = '2015-11-12T20:33:09'
        seller_info.name = 'bob'
        seller_info.onboardingEmail = 'bob@example.com'
        seller_info.onboardingIpAddress = '75.100.88.78'
        seller_info.parentEntity = 'abc'
        seller_info.phone = '9785510040'
        seller_info.sellerId = '123456789'
        seller_tags = fields.sellerTagsType
        seller_tags.tag = '2'
        seller_info.seller_tags = seller_tags
        seller_info.username = 'bob123'
        authorization.seller_info = seller_info
        card = fields.cardType()
        card.number = '4100000000000000'
        card.expDate = '1210'
        card.type = 'VI'
        authorization.card = card
        authorization.orderChannel = 'MIT'
        authorization.authIndicator = 'Estimated'
        txnBatch.add(authorization)

        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        sale = fields.sale()
        sale.id = 'auth_GP_DI'
        sale.reportGroup = 'DirectWFITxn'
        sale.orderId = 'XGR-1840823423'
        sale.amount = 1100
        sale.orderSource = 'telephone'
        seller_info = fields.sellerInfo()
        seller_info.accountNumber = '6557959585426472'
        seller_info.aggregateOrderCount = '4'
        seller_info.aggregateOrderDollars = '100'
        seller_address = fields.sellerAddress()
        seller_address.sellerStreetaddress = '15 Main Street'
        seller_address.sellerUnit = '100 AB'
        seller_address.sellerPostalcode = '12345'
        seller_address.sellerCity = 'San Jose'
        seller_address.sellerProvincecode = 'MA'
        seller_address.sellerCountrycode = 'US'
        seller_info.sellerAddress = seller_address
        seller_info.createdDate = '2015-11-12T20:33:09'
        seller_info.domain = 'vap'
        seller_info.email = 'bob@example.com'
        seller_info.lastUpdateDate = '2015-11-12T20:33:09'
        seller_info.name = 'bob'
        seller_info.onboardingEmail = 'bob@example.com'
        seller_info.onboardingIpAddress = '75.100.88.78'
        seller_info.parentEntity = 'abc'
        seller_info.phone = '9785510040'
        seller_info.sellerId = '123456789'
        seller_tags = fields.sellerTagsType
        seller_tags.tag = '2'
        seller_info.seller_tags = seller_tags
        seller_info.username = 'bob123'
        sale.seller_info = seller_info
        card = fields.cardType()
        card.number = '4100000000000000'
        card.expDate = '1210'
        card.type = 'VI'
        sale.card = card
        sale.orderChannel = 'MIT'
        txnBatch.add(sale)
        # stream to Vaitiv eCommerce and get object as response
        response = batch.submit(txnBatch, conf, filename)

        if conf.useEncryption:
            # Using encryption.
            retry = True
            tried = 0
            withEncryptionReponseFilepath = ''
            while retry:
                tried += 1
                try:
                    withEncryptionReponseFilepath = batch._get_file_from_sftp(response, conf, False, 60)
                    retry = False
                except:
                    # sleep 1 minute waiting for batch get processed
                    print("sleep 30 seconds waiting for batch get processed")
                    time.sleep(30)
                if tried > 20:
                    self.fail("Timeout for retrieve batch response")
                    break

            call(["cat", withEncryptionReponseFilepath])
            ### <<< WITH ENCRYPTION

            with open(withEncryptionReponseFilepath, 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals("Valid Format", obj.message)

        else:
            with open(os.path.join(conf.batch_requests_path, '%s.xml' % filename), 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals(1, obj.numBatchRequests)
                self.assertEquals(106, obj.batchRequest[0].authAmount)

            self.assertEquals('%s.xml.asc' % filename, response)

    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_capture_force_capture_sale_capture_given_auth_v12_31(self):
        txnBatch = batch.Transactions()
        authorization = fields.authorization()
        authorization.id = '1'
        authorization.customerId = 'Cust0403'
        authorization.reportGroup = 'Default Report Group'
        authorization.orderId = '12344401'
        authorization.amount = 106
        authorization.orderSource = 'ecommerce'
        card = fields.cardType()
        card.number = '4100000000000000'
        card.expDate = '1210'
        card.type = 'VI'
        authorization.card = card
        authorization.orderChannel = 'MIT'
        authorization.authIndicator = 'Estimated'
        txnBatch.add(authorization)

        capture = fields.capture()
        capture.cnpTxnId = 123456000
        capture.orderId = '457754'
        capture.amount = 6000
        capture.id = 'ID001'
        card = fields.cardType()
        card.number = '4100100000000000'
        card.expDate = '1210'
        card.type = 'VI'
        capture.card = card
        capture.foreignRetailerIndicator = 'F'
        txnBatch.add(capture)

        forceCapture = fields.forceCapture()
        forceCapture.reportGroup = 'Default Report Group'
        forceCapture.orderId = '12345'
        forceCapture.amount = 7000
        forceCapture.orderSource = 'ecommerce'
        forceCapture.processingType = 'accountFunding'
        forceCapture.id = '54321'
        forceCapture.businessIndicator = 'consumerBillPayment'
        card = fields.cardType()
        card.number = '4100000000000001'
        card.expDate = '1210'
        card.type = 'VI'
        forceCapture.card = card
        forceCapture.foreignRetailerIndicator = 'F'
        txnBatch.add(forceCapture)

        captureGivenAuth = fields.captureGivenAuth()
        captureGivenAuth.orderId = '77373'
        captureGivenAuth.amount = 2000
        captureGivenAuth.orderSource = 'ecommerce'
        captureGivenAuth.id = 'NewTxnID'
        captureGivenAuth.businessIndicator = 'consumerBillPayment'
        card = fields.cardType()
        card.number = '4100000000000000'
        card.expDate = '1210'
        card.type = 'VI'
        # The type of card is cardType
        captureGivenAuth.card = card
        captureGivenAuth.foreignRetailerIndicator = 'F'
        txnBatch.add(captureGivenAuth)

        sale = fields.sale()
        sale.id = 'auth_GP_DI'
        sale.reportGroup = 'DirectWFITxn'
        sale.orderId = 'XGR-1840823423'
        sale.amount = 1100
        sale.orderSource = 'telephone'
        card = fields.cardType()
        card.number = '4100000000000000'
        card.expDate = '1210'
        card.type = 'VI'
        sale.card = card
        sale.orderChannel = 'MIT'
        sale.foreignRetailerIndicator = 'F'
        txnBatch.add(sale)
        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        # stream to Vaitiv eCommerce and get object as response
        response = batch.submit(txnBatch, conf, filename)

        if conf.useEncryption:
            # Using encryption.
            retry = True
            tried = 0
            withEncryptionReponseFilepath = ''
            while retry:
                tried += 1
                try:
                    withEncryptionReponseFilepath = batch._get_file_from_sftp(response, conf, False, 60)
                    retry = False
                except:
                    # sleep 1 minute waiting for batch get processed
                    print("sleep 30 seconds waiting for batch get processed")
                    time.sleep(30)
                if tried > 20:
                    self.fail("Timeout for retrieve batch response")
                    break

            call(["cat", withEncryptionReponseFilepath])
            ### <<< WITH ENCRYPTION

            with open(withEncryptionReponseFilepath, 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals("Valid Format", obj.message)

        else:
            with open(os.path.join(conf.batch_requests_path, '%s.xml' % filename), 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals(1, obj.numBatchRequests)
                self.assertEquals(106, obj.batchRequest[0].authAmount)
                self.assertEquals(6000, obj.batchRequest[0].captureAmount)
                self.assertEquals(2000, obj.batchRequest[0].captureGivenAuthAmount)
                self.assertEquals(7000, obj.batchRequest[0].forceCaptureAmount)
                self.assertEquals(1100, obj.batchRequest[0].saleAmount)

            self.assertEquals('%s.xml.asc' % filename, response)

    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_capture_force_capture_sale_capture_given_auth_v12_33(self):
        txnBatch = batch.Transactions()
        authorization = fields.authorization()
        authorization.id = '1'
        authorization.customerId = 'Cust0403'
        authorization.reportGroup = 'Default Report Group'
        authorization.orderId = '12344401'
        authorization.amount = 106
        authorization.orderSource = 'ecommerce'
        card = fields.cardType()
        card.number = '4457010000000009'
        card.expDate = '1210'
        card.type = 'VI'
        authorization.card = card
        lineItemDataList = list()
        lineItemData = fields.lineItemData()
        lineItemData.itemDescription = 'des'
        lineItemData.itemCategory = 'Chock'
        lineItemData.shipmentId = 'prod1234'
        sub = fields.subscription()
        sub.subscriptionId = '123'
        sub.nextDeliveryDate = datetime.datetime.now().strftime("%Y-%m-%d")
        sub.periodUnit = 'YEAR'
        sub.numberOfPeriods = '748'
        sub.regularItemPrice = 148
        sub.currentPeriod = '476'
        lineItemData.subscription = sub
        lineItemDataList.append(lineItemData)
        enhancedData = fields.enhancedData()
        enhancedData.lineItemData = lineItemDataList
        authorization.enhancedData = enhancedData
        txnBatch.add(authorization)

        capture = fields.capture()
        capture.cnpTxnId = 123456000
        capture.orderId = '457754'
        capture.amount = 6000
        capture.id = 'ID001'
        card = fields.cardType()
        card.number = '4457010000000009'
        card.expDate = '1210'
        card.type = 'VI'
        capture.card = card
        lineItemDataList = list()
        lineItemData = fields.lineItemData()
        lineItemData.itemDescription = 'des'
        lineItemData.itemCategory = 'Chock'
        lineItemData.shipmentId = 'prod1234'
        sub = fields.subscription()
        sub.subscriptionId = '123'
        sub.nextDeliveryDate = datetime.datetime.now().strftime("%Y-%m-%d")
        sub.periodUnit = 'YEAR'
        sub.numberOfPeriods = '748'
        sub.regularItemPrice = 148
        sub.currentPeriod = '476'
        lineItemData.subscription = sub
        lineItemDataList.append(lineItemData)
        enhancedData = fields.enhancedData()
        enhancedData.lineItemData = lineItemDataList
        capture.enhancedData = enhancedData
        txnBatch.add(capture)

        forceCapture = fields.forceCapture()
        forceCapture.reportGroup = 'Default Report Group'
        forceCapture.orderId = '12345'
        forceCapture.amount = 7000
        forceCapture.orderSource = 'ecommerce'
        forceCapture.processingType = 'accountFunding'
        forceCapture.id = '54321'
        forceCapture.businessIndicator = 'consumerBillPayment'
        card = fields.cardType()
        card.number = '4457010000000009'
        card.expDate = '1210'
        card.type = 'VI'
        forceCapture.card = card
        lineItemDataList = list()
        lineItemData = fields.lineItemData()
        lineItemData.itemDescription = 'des'
        lineItemData.itemCategory = 'Chock'
        lineItemData.shipmentId = 'prod1234'
        sub = fields.subscription()
        sub.subscriptionId = '123'
        sub.nextDeliveryDate = datetime.datetime.now().strftime("%Y-%m-%d")
        sub.periodUnit = 'YEAR'
        sub.numberOfPeriods = '748'
        sub.regularItemPrice = 148
        sub.currentPeriod = '476'
        lineItemData.subscription = sub
        lineItemDataList.append(lineItemData)
        enhancedData = fields.enhancedData()
        enhancedData.lineItemData = lineItemDataList
        forceCapture.enhancedData = enhancedData
        txnBatch.add(forceCapture)

        captureGivenAuth = fields.captureGivenAuth()
        captureGivenAuth.orderId = '77373'
        captureGivenAuth.amount = 2000
        captureGivenAuth.orderSource = 'ecommerce'
        captureGivenAuth.id = 'NewTxnID'
        captureGivenAuth.businessIndicator = 'consumerBillPayment'
        card = fields.cardType()
        card.number = '4457010000000009'
        card.expDate = '1210'
        card.type = 'VI'
        # The type of card is cardType
        captureGivenAuth.card = card
        lineItemDataList = list()
        lineItemData = fields.lineItemData()
        lineItemData.itemDescription = 'des'
        lineItemData.itemCategory = 'Chock'
        lineItemData.shipmentId = 'prod1234'
        sub = fields.subscription()
        sub.subscriptionId = '123'
        sub.nextDeliveryDate = datetime.datetime.now().strftime("%Y-%m-%d")
        sub.periodUnit = 'YEAR'
        sub.numberOfPeriods = '748'
        sub.regularItemPrice = 148
        sub.currentPeriod = '476'
        lineItemData.subscription = sub
        lineItemDataList.append(lineItemData)
        enhancedData = fields.enhancedData()
        enhancedData.lineItemData = lineItemDataList
        captureGivenAuth.enhancedData = enhancedData
        captureGivenAuth.foreignRetailerIndicator = 'F'
        txnBatch.add(captureGivenAuth)

        sale = fields.sale()
        sale.id = 'auth_GP_DI'
        sale.reportGroup = 'DirectWFITxn'
        sale.orderId = 'XGR-1840823423'
        sale.amount = 1100
        sale.orderSource = 'telephone'
        card = fields.cardType()
        card.number = '4457010000000009'
        card.expDate = '1210'
        card.type = 'VI'
        sale.card = card
        sale.orderChannel = 'MIT'
        sale.foreignRetailerIndicator = 'F'
        lineItemDataList = list()
        lineItemData = fields.lineItemData()
        lineItemData.itemDescription = 'des'
        lineItemData.itemCategory = 'Chock'
        lineItemData.shipmentId = 'prod1234'
        sub = fields.subscription()
        sub.subscriptionId = '123'
        sub.nextDeliveryDate = datetime.datetime.now().strftime("%Y-%m-%d")
        sub.periodUnit = 'YEAR'
        sub.numberOfPeriods = '748'
        sub.regularItemPrice = 148
        sub.currentPeriod = '476'
        lineItemData.subscription = sub
        lineItemDataList.append(lineItemData)
        enhancedData = fields.enhancedData()
        enhancedData.lineItemData = lineItemDataList
        sale.enhancedData = enhancedData
        txnBatch.add(sale)
        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        # stream to Vaitiv eCommerce and get object as response
        response = batch.submit(txnBatch, conf, filename)

        if conf.useEncryption:
            # Using encryption.
            retry = True
            tried = 0
            withEncryptionReponseFilepath = ''
            while retry:
                tried += 1
                try:
                    withEncryptionReponseFilepath = batch._get_file_from_sftp(response, conf, False, 60)
                    retry = False
                except:
                    # sleep 1 minute waiting for batch get processed
                    print("sleep 30 seconds waiting for batch get processed")
                    time.sleep(30)
                if tried > 20:
                    self.fail("Timeout for retrieve batch response")
                    break

            call(["cat", withEncryptionReponseFilepath])
            ### <<< WITH ENCRYPTION

            with open(withEncryptionReponseFilepath, 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals("Valid Format", obj.message)

        else:
            with open(os.path.join(conf.batch_requests_path, '%s.xml' % filename), 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEqual(1, obj.numBatchRequests)
                self.assertEqual(106, obj.batchRequest[0].authAmount)
                self.assertEqual(6000, obj.batchRequest[0].captureAmount)
                self.assertEqual(2000, obj.batchRequest[0].captureGivenAuthAmount)
                self.assertEqual(7000, obj.batchRequest[0].forceCaptureAmount)
                self.assertEqual(1100, obj.batchRequest[0].saleAmount)

            self.assertEqual('%s.xml.asc' % filename, response)

    @unittest.skipIf(preliveStatus.lower() == 'down', "prelive not available")
    def test_batch_sub_merchant_credit_debit_vendor_credit_debit_v12_37(self):
        txnBatch = batch.Transactions()
        authorization = fields.authorization()
        authorization.id = '1'
        authorization.customerId = 'Cust0403'
        authorization.reportGroup = 'Default Report Group'
        authorization.orderId = '12344401'
        authorization.amount = 1061512151
        authorization.orderSource = 'ecommerce'
        card = fields.cardType()
        card.number = '4100000000000000'
        card.expDate = '1210'
        card.type = 'VI'
        authorization.card = card
        authorization.orderChannel = 'MIT'
        authorization.authIndicator = 'Estimated'
        authorization.businessIndicator = 'agentCashOut'
        authorization.orderChannel = 'SMART_TV'
        authorization.fraudCheckAction = 'APPROVED_SKIP_FRAUD_CHECK'
        # Create accountFundingTransactionData
        accountfundingtransactiondata = fields.accountFundingTransactionData()
        accountfundingtransactiondata.receiverLastName = 'Smith'
        accountfundingtransactiondata.receiverState = 'AZ'
        accountfundingtransactiondata.receiverCountry = 'USA'
        accountfundingtransactiondata.receiverAccountNumber = '1234567890'
        accountfundingtransactiondata.accountFundingTransactionType = 'walletTransfer'
        accountfundingtransactiondata.receiverAccountNumberType = 'cardAccount'
        authorization.accountFundingTransactionData = accountfundingtransactiondata

        customerInfo = fields.customerInfo()

        customerInfo.accountUserName = 'Jack'
        customerInfo.userAccountNumber = '1234'
        customerInfo.userAccountEmail = 'gmail@gmail.com'
        customerInfo.membershipId = '11111'
        customerInfo.membershipPhone = '123456'
        customerInfo.membershipEmail = 'gmail@gmail.com'
        customerInfo.membershipName = 'fran'
        customerInfo.accountCreatedDate = datetime.datetime.now().strftime("%Y-%m-%d")
        customerInfo.userAccountPhone = '000461223'

        authorization.customerInfo = customerInfo

        detailTaxList = list()
        detailTax = fields.detailTax()
        detailTax.taxAmount = 100
        detailTax2 = fields.detailTax()
        detailTax2.taxAmount = 200
        detailTaxList.append(detailTax)
        detailTaxList.append(detailTax2)
        lineItemDataList = list()
        lineItemData = fields.lineItemData()
        lineItemData.itemDescription = 'des'
        lineItemData.itemCategory = 'Chock'
        lineItemData.itemCategory = 'Chock'
        lineItemData.itemSubCategory = 'pen'
        lineItemData.productId = '001'
        lineItemData.productName = 'prod'
        lineItemDataList.append(lineItemData)
        enhancedData = fields.enhancedData()
        enhancedData.detailTax = detailTaxList
        enhancedData.lineItemData = lineItemDataList
        enhancedData.discountCode = '001'
        enhancedData.discountPercent = '10'
        enhancedData.fulfilmentMethodType = 'STANDARD_SHIPPING'

        authorization.enhancedData = enhancedData

        txnBatch.add(authorization)

        capture = fields.capture()
        capture.cnpTxnId = 123456000
        capture.orderId = '457754'
        capture.amount = 6000
        capture.id = 'ID001'
        card = fields.cardType()
        card.number = '4100100000000000'
        card.expDate = '1210'
        card.type = 'VI'
        capture.card = card
        capture.foreignRetailerIndicator = 'F'
        enhancedData.fulfilmentMethodType = 'EXPEDITED_SHIPPING'
        capture.enhancedData=enhancedData
        txnBatch.add(capture)

        forceCapture = fields.forceCapture()
        forceCapture.reportGroup = 'Default Report Group'
        forceCapture.orderId = '12345'
        forceCapture.amount = 7000
        forceCapture.orderSource = 'ecommerce'
        forceCapture.processingType = 'accountFunding'
        forceCapture.id = '54321'
        forceCapture.businessIndicator = 'businessToBusinessTransfer'
        card = fields.cardType()
        card.number = '4100000000000001'
        card.expDate = '1210'
        card.type = 'VI'
        forceCapture.card = card
        forceCapture.foreignRetailerIndicator = 'F'
        enhancedData.fulfilmentMethodType = 'EXPEDITED_SHIPPING'
        forceCapture.enhancedData = enhancedData
        txnBatch.add(forceCapture)

        captureGivenAuth = fields.captureGivenAuth()
        captureGivenAuth.orderId = '77373'
        captureGivenAuth.amount = 2000
        captureGivenAuth.orderSource = 'ecommerce'
        captureGivenAuth.id = 'NewTxnID'
        captureGivenAuth.businessIndicator = 'governmentNonProfitDisbursement'
        card = fields.cardType()
        card.number = '4100000000000000'
        card.expDate = '1210'
        card.type = 'VI'
        # The type of card is cardType
        captureGivenAuth.card = card
        captureGivenAuth.foreignRetailerIndicator = 'F'
        txnBatch.add(captureGivenAuth)

        sale = fields.sale()
        sale.id = 'auth_GP_DI'
        sale.reportGroup = 'DirectWFITxn'
        sale.orderId = 'XGR-1840823423'
        sale.amount = 1100
        sale.orderSource = 'telephone'
        card = fields.cardType()
        card.number = '4100000000000000'
        card.expDate = '1210'
        card.type = 'VI'
        sale.card = card
        sale.orderChannel = 'SMART_TV'
        sale.foreignRetailerIndicator = 'F'
        sale.businessIndicator = 'rapidMerchantSettlement'
        sale.accountFundingTransactionData = accountfundingtransactiondata
        sale.fraudCheckAction = 'APPROVED_SKIP_FRAUD_CHECK'
        enhancedData.fulfilmentMethodType = 'STANDARD_SHIPPING'
        sale.enhancedData = enhancedData
        txnBatch.add(sale)

        submerchantcredit = fields.submerchantCredit()
        submerchantcredit.id = 'ThisIsID'
        submerchantcredit.reportGroup = 'Default Report Group'
        submerchantcredit.fundingSubmerchantId = "value for fundingSubmerchantId"
        submerchantcredit.submerchantName = "temp1200"
        submerchantcredit.fundsTransferId = "value for fundsTransferId"
        submerchantcredit.amount = 1512
        account_info = fields.echeckTypeCtx()
        account_info.accType = 'Savings'
        account_info.accNum = "1234"
        account_info.routingNum = "12345678"
        submerchantcredit.accountInfo = account_info
        submerchantcredit.customIdentifier = '127'
        txnBatch.add(submerchantcredit)

        submerchantdebit = fields.submerchantDebit()
        submerchantdebit.id = 'ThisIsID'
        submerchantdebit.reportGroup = 'Default Report Group'
        submerchantdebit.fundingSubmerchantId = "value for fundingSubmerchantId"
        submerchantdebit.submerchantName = "temp1200"
        submerchantdebit.fundsTransferId = "value for fundsTransferId"
        submerchantdebit.amount = 1512151212
        submerchantdebit.accountInfo = account_info
        submerchantdebit.customIdentifier = '123'
        txnBatch.add(submerchantdebit)

        vendordebit = fields.vendorDebit()
        vendordebit.id = 'ThisIsID'
        vendordebit.reportGroup = 'Default Report Group'
        vendordebit.fundingSubmerchantId = "value for fundingSubmerchantId"
        vendordebit.submerchantName = "temp1200"
        vendordebit.fundsTransferId = "value for fundsTransferId"
        vendordebit.amount = 1512151212
        vendordebit.accountInfo = account_info
        vendordebit.customIdentifier = '123'
        txnBatch.add(vendordebit)

        vendorcredit = fields.vendorCredit()
        vendorcredit.id = 'ThisIsID'
        vendorcredit.reportGroup = 'Default Report Group'
        vendorcredit.fundingSubmerchantId = "value for fundingSubmerchantId"
        vendorcredit.submerchantName = "temp1200"
        vendorcredit.fundsTransferId = "value for fundsTransferId"
        vendorcredit.amount = 1512151
        vendorcredit.accountInfo = account_info
        vendorcredit.customIdentifier = '123'
        txnBatch.add(vendorcredit)

        filename = 'batch_test_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        # stream to Vaitiv eCommerce and get object as response
        response = batch.submit(txnBatch, conf, filename)

        if conf.useEncryption:
            # Using encryption.
            retry = True
            tried = 0
            withEncryptionReponseFilepath = ''
            while retry:
                tried += 1
                try:
                    withEncryptionReponseFilepath = batch._get_file_from_sftp(response, conf, False, 60)
                    retry = False
                except:
                    # sleep 1 minute waiting for batch get processed
                    print("sleep 30 seconds waiting for batch get processed")
                    time.sleep(30)
                if tried > 20:
                    self.fail("Timeout for retrieve batch response")
                    break

            call(["cat", withEncryptionReponseFilepath])
            ### <<< WITH ENCRYPTION

            with open(withEncryptionReponseFilepath, 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals("Valid Format", obj.message)

        else:
            with open(os.path.join(conf.batch_requests_path, '%s.xml' % filename), 'r') as xml_file:
                obj = fields.CreateFromDocument(xml_file.read())
                self.assertEquals(1, obj.numBatchRequests)
                self.assertEquals(1061512151, obj.batchRequest[0].authAmount)
                self.assertEquals(6000, obj.batchRequest[0].captureAmount)
                self.assertEquals(2000, obj.batchRequest[0].captureGivenAuthAmount)
                self.assertEquals(7000, obj.batchRequest[0].forceCaptureAmount)
                self.assertEquals(1100, obj.batchRequest[0].saleAmount)

            self.assertEquals('%s.xml.asc' % filename, response)


if __name__ == '__main__':
    unittest.main()
