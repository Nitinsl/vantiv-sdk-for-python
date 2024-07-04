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

from vantivsdk.utils import VantivException

package_root = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.insert(0, package_root)

import pyxb

from vantivsdk import *

conf = utils.Configuration()


class TestFundingInstruction(unittest.TestCase):
    def test_payFacCredit_000(self):
        txn_dict = {
            'payFacCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000
            }
        }

        response = online.request(txn_dict, conf, sameDayFunding=True)
        self.assertEquals('000', response['payFacCreditResponse']['response'])

    def test_payFacDebit_000(self):
        txn_dict = {
            'payFacDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['payFacDebitResponse']['response'])

    def test_submerchantCredit_000(self):
        txn_dict = {
            'submerchantCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
                'customIdentifier': 'customIdentifie'
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['submerchantCreditResponse']['response'])

    def test_submerchantDebit_000(self):
        txn_dict = {
            'submerchantDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
                'customIdentifier': 'customIdentifie'
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['submerchantDebitResponse']['response'])

    def test_vendorCredit_000(self):
        txn_dict = {
            'vendorCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'vendorName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['vendorCreditResponse']['response'])

    def test_vendorCredit_000_fundingCustomerId(self):
        txn_dict = {
            'vendorCredit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': 'fundingCustomerId',
                'vendorName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['vendorCreditResponse']['response'])

    def test_vendorDebit_000(self):
        txn_dict = {
            'vendorDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'vendorName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['vendorDebitResponse']['response'])

    def test_vendorDebit_000_fundingCustomerId(self):
        txn_dict = {
            'vendorDebit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': 'fundingCustomerId',
                'vendorName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['vendorDebitResponse']['response'])

    def test_physicalCheckCredit_000(self):
        txn_dict = {
            'physicalCheckCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002000,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['physicalCheckCreditResponse']['response'])

    def test_physicalCheckDebit_000(self):
        txn_dict = {
            'physicalCheckDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002000,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['physicalCheckDebitResponse']['response'])

    def test_reserveCredit_000(self):
        txn_dict = {
            'reserveCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['reserveCreditResponse']['response'])

    def test_reserveDebit_000(self):
        txn_dict = {
            'reserveDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010000
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['reserveDebitResponse']['response'])

    def test_fundingInstructionVoid_000(self):
        txn_dict = {
            'fundingInstructionVoid': {
                'id': 'OnlinePC2',
                'cnpTxnId': '900010002000',
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['fundingInstructionVoidResponse']['response'])

    def test_fastAccessFunding_000(self):
        txn_dict = {
            'fastAccessFunding': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'submerhc',
                'fundsTransferId': '1234567891111111',
                'amount': 90000000,
                'card': {
                    'type': 'VI',
                    'number': '4100000000000000',
                    'expDate': '1210'
                }
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['fastAccessFundingResponse']['response'])

    def test_fastAccessFunding_with_cardholderAddress(self):
        txn_dict = {
            'fastAccessFunding': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'submerhc',
                'fundsTransferId': '1234567891111111',
                'amount': 90000000,

                'card': {
                    'type': 'VI',
                    'number': '4100000000000000',
                    'expDate': '1210'
                },
                'cardholderAddress': {
                    'addressLine1': '37 Main Street',
                    'addressLine2': '',
                    'addressLine3': '',
                    'city': 'Augusta',
                    'state': 'Wisconsin',
                    'zip': '28209',
                    'country': 'USA'
                }
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['fastAccessFundingResponse']['response'])

    def test_payFacCredit_940(self):
        txn_dict = {
            'payFacCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 90001940
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['payFacCreditResponse']['response'])

    def test_payFacDebit_940(self):
        txn_dict = {
            'payFacDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 90001940
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['payFacDebitResponse']['response'])

    def test_submerchantCredit_940(self):
        txn_dict = {
            'submerchantCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 90001940,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
                'customIdentifier': 'customIdentifie'
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['submerchantCreditResponse']['response'])

    def test_submerchantDebit_940(self):
        txn_dict = {
            'submerchantDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012940,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
                'customIdentifier': 'customIdentifie'
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['submerchantDebitResponse']['response'])

    def test_vendorCredit_940(self):
        txn_dict = {
            'vendorCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'vendorName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012940,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['vendorCreditResponse']['response'])

    def test_vendorDebit_940(self):
        txn_dict = {
            'vendorDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'vendorName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012940,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['vendorDebitResponse']['response'])

    def test_physicalCheckCredit_940(self):
        txn_dict = {
            'physicalCheckCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002940,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['physicalCheckCreditResponse']['response'])

    def test_physicalCheckDebit_940(self):
        txn_dict = {
            'physicalCheckDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002940,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['physicalCheckDebitResponse']['response'])

    def test_reserveCredit_940(self):
        txn_dict = {
            'reserveCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012940,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['reserveCreditResponse']['response'])

    def test_reserveDebit_940(self):
        txn_dict = {
            'reserveDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012940,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['reserveDebitResponse']['response'])

    def test_fundingInstructionVoid_940(self):
        txn_dict = {
            'fundingInstructionVoid': {
                'id': 'OnlinePC2',
                'cnpTxnId': '900010002940',
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['fundingInstructionVoidResponse']['response'])

    def test_fastAccessFunding_940(self):
        txn_dict = {
            'fastAccessFunding': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'submerch',
                'fundsTransferId': '1234567891111111',
                'amount': 90000940,
                'card': {
                    'type': 'VI',
                    'number': '4100000000000000',
                    'expDate': '1210'
                }
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('940', response['fastAccessFundingResponse']['response'])

    def test_payFacCredit_941(self):
        txn_dict = {
            'payFacCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012941
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['payFacCreditResponse']['response'])

    def test_payFacDebit_941(self):
        txn_dict = {
            'payFacDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012941
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['payFacDebitResponse']['response'])

    def test_submerchantCredit_941(self):
        txn_dict = {
            'submerchantCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012941,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
                'customIdentifier': 'customIdentifie'
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['submerchantCreditResponse']['response'])

    def test_submerchantDebit_941(self):
        txn_dict = {
            'submerchantDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012941,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
                'customIdentifier': 'customIdentifie'
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['submerchantDebitResponse']['response'])

    def test_vendorCredit_941(self):
        txn_dict = {
            'vendorCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'vendorName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012941,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['vendorCreditResponse']['response'])

    def test_vendorDebit_941(self):
        txn_dict = {
            'vendorDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'vendorName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012941,
                'accountInfo': {
                    'accType': 'Checking',
                    'accNum': '123456789012',
                    'routingNum': '123456789'
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['vendorDebitResponse']['response'])

    def test_physicalCheckCredit_941(self):
        txn_dict = {
            'physicalCheckCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002941,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['physicalCheckCreditResponse']['response'])

    def test_physicalCheckDebit_941(self):
        txn_dict = {
            'physicalCheckDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002941,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['physicalCheckDebitResponse']['response'])

    def test_reserveCredit_941(self):
        txn_dict = {
            'reserveCredit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012941,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['reserveCreditResponse']['response'])

    def test_reserveDebit_941(self):
        txn_dict = {
            'reserveDebit': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900012941,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['reserveDebitResponse']['response'])

    def test_fundingInstructionVoid_941(self):
        txn_dict = {
            'fundingInstructionVoid': {
                'id': 'OnlinePC2',
                'cnpTxnId': '900010002941',
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['fundingInstructionVoidResponse']['response'])

    def test_fastAccessFunding_941(self):
        txn_dict = {
            'fastAccessFunding': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'submerchantName': 'submerch',
                'fundsTransferId': '1234567891111111',
                'amount': 90000941,
                'card': {
                    'type': 'VI',
                    'number': '4100000000000000',
                    'expDate': '1210'
                }
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('941', response['fastAccessFundingResponse']['response'])

    def test_fundingInstructionVoid_360(self):
        txn_dict = {
            'fundingInstructionVoid': {
                'id': 'OnlinePC2',
                'cnpTxnId': '900010002360',
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('360', response['fundingInstructionVoidResponse']['response'])

    def test_fundingInstructionVoid_362(self):
        txn_dict = {
            'fundingInstructionVoid': {
                'id': 'OnlinePC2',
                'cnpTxnId': '900010002362',
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('362', response['fundingInstructionVoidResponse']['response'])

    def test_customerDebit_000(self):
        txn_dict = {
            'customerDebit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': 'fundingCustomerId',
                'customerName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['customerDebitResponse']['response'])

    def test_customerCredit_000(self):
        txn_dict = {
            'customerCredit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': 'fundingCustomerId',
                'customerName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['customerCreditResponse']['response'])

    def test_payoutOrgDebit_000(self):
        txn_dict = {
            'payoutOrgDebit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002000,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['payoutOrgDebitResponse']['response'])

    def test_payoutOrgCredit_000(self):
        txn_dict = {
            'payoutOrgCredit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': 'fundingSubmerchantId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002000,
            }
        }

        response = online.request(txn_dict, conf)
        self.assertEquals('000', response['payoutOrgCreditResponse']['response'])

    def test_fastAccessFunding_mixedName(self):
        self.skipTest("Sandbox does not check for mixed names. Production does check.")

        txn_dict = {
            'fastAccessFunding': {
                'id': 'OnlinePC2',
                'fundingSubmerchantId': 'fundingSubmerchantId',
                'customerName': 'submerhc',
                'fundsTransferId': '1234567891111111',
                'amount': 90000000,
                'card': {
                    'type': 'VI',
                    'number': '4100000000000000',
                    'expDate': '1210'
                }
            }
        }

        with self.assertRaises(VantivException) as context:
            online.request(txn_dict, conf)

    def test_customerDebit_nullCustomerNameException(self):
        txn_dict = {
            'customerDebit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': 'fundingCustomerId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        with self.assertRaises(VantivException) as context:
            online.request(txn_dict, conf)

    def test_customerDebit_negativeAmountException(self):
        self.skipTest("Sandbox does not check for negative amounts. Production does check.")

        txn_dict = {
            'customerDebit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': 'fundingCustomerId',
                'customerName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': -900010002000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        with self.assertRaises(VantivException) as context:
            online.request(txn_dict, conf)

    def test_customerDebit_idTooLongException(self):
        txn_dict = {
            'customerDebit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': '123456789012345678901234567890123456789012345678901234567890',
                'customerName': 'Jon Snow',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002000,
                'accountInfo': {
                    'accNum': '123456789012',
                    'routingNum': '123456789',
                    'accType': 'Checking',
                },
            }
        }

        with self.assertRaises(VantivException) as context:
            online.request(txn_dict, conf)

    def test_customerCredit_nullCustomerNameException(self):
        txn_dict = {
            'customerCredit': {
                'id': 'OnlinePC2',
                'fundingCustomerId': 'fundingCustomerId',
                'fundsTransferId': 'fundsTransferId',
                'amount': 900010002000,
                'accountInfo': {
                    'accType': 'Checking',
                    'accNum': '123456789012',
                    'routingNum': '123456789'
                },
            }
        }

        with self.assertRaises(VantivException) as context:
            online.request(txn_dict, conf)

if __name__ == '__main__':
    unittest.main()
