import os
import sys
import unittest
from calendar import Calendar
from enum import auto

package_root = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.insert(0, package_root)

import pyxb

from vantivsdk import *
import datetime

conf = utils.Configuration()

class TestEncryptionKeyRequest(unittest.TestCase):

    def test_simple_encryption_key_request(self):

        transaction = fields.encryptionKeyRequest("PREVIOUS")

        response = online.request(transaction, conf)
        self.assertEqual('10000', response['encryptionKeyResponse']['encryptionKeySequence'])


if __name__ == '__main__':
    unittest.main()