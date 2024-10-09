import subprocess
from subprocess import call
from subprocess import check_output
from subprocess import CalledProcessError

import os

from . import (utils)

class PgpHelper(object):

  # Encrypt a file.
  def encryptFile(self, recipient, toBeEncryptedFilepath, outputFilepath):
    # Call gpg command line to encrypt the file.
    try:
      check_output(["gpg",
      "--batch",
      "--yes",
      "--always-trust",
      "--no-secmem-warning",
      "--armor",
      "--trust-model", "always",
      "--output", outputFilepath,
      "--recipient", recipient,
      "--encrypt", toBeEncryptedFilepath])
      # Check for error code.
      print("\"%s\" has been encrypted to \"%s\"." % (toBeEncryptedFilepath, outputFilepath))
    except CalledProcessError as err:
      raise utils.VantivException("Encrypting the file has failed!\n%s" % err.output)


  # Handle gpg encryption when the output filename is the same as the input filename.
  def encryptFileSameName(self, recipient, toBeEncryptedFilepath):
    try:
      temp = 'pgp.vantiv'
      self.encryptFile(recipient, toBeEncryptedFilepath, temp)
      writer = open(toBeEncryptedFilepath, 'wb')
      reader = open(temp, 'rb')
      writer.write(reader.read())
      writer.close()
      reader.close()
      os.remove(temp)
    except CalledProcessError as err:
      raise utils.VantivException("Encrypting the file to the output with the same name has failed!\n%s" % err.output)


  # Decrypt an encrypted file.
  def decryptFile(self, passphrase, encryptedFilepath, outputFilepath):
    # Call gpg command line to decrypt the file.
    try:
      check_output(["gpg",
      "--batch",
      "--yes",
      "--no-secmem-warning",
      "--no-mdc-warning",
      "--output", outputFilepath,
      "--passphrase", passphrase,
      "--decrypt", encryptedFilepath])
      # Check for error code.
      print("\"%s\" has been decrypted to \"%s\"." % (encryptedFilepath, outputFilepath))
    except CalledProcessError as err:
      raise utils.VantivException("Decrypting the file has failed!\n%s" % err.output)


  # Add Vantiv public key into merchants' keyrings.
  def importVantivPublicKey(self, publicKeyFilePath):
    # Call gpg command line to import public key.
    try:
      check_output(["gpg",
      "--import", publicKeyFilePath])
      #Check for error code.
      print("Successfully added Vantiv public key!")
    except CalledProcessError as err:
      raise utils.VantivException("Adding Vantiv public key has failed with error code is %s.\n" % err.output)

  def encryptPayload(toBeEncryptedString, path):
    # Convert the object to a JSON string
    try:
      # Call gpg command line to encrypt the string
      process = subprocess.Popen([
        "gpg",
        "--batch",
        "--yes",
        "--always-trust",
        "--no-secmem-warning",
        "--armor",
        "--trust-model", "always",
        "--recipient-file", path,
        "--encrypt"
      ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

      # Pass the string to be encrypted to the gpg process
      encrypted_string, err = process.communicate(input=toBeEncryptedString.encode())

      if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, process.args, output=err)

      return encrypted_string.decode()
    except subprocess.CalledProcessError as err:
      raise utils.VantivException(
        "Encrypting the payload has failed. Please check the Encryption key or key path, is correct!\n%s" % err.output)
