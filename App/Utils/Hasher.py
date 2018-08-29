import hashlib
import uuid
import Crypto
import ast
import base64
import rsa
from pathlib import Path


class Hasher:
    '''This is class is responsible for
    hashing string encoding string to make secure'''

    def __init__(self):
        key_file = Path("Secrets/key.pem")
        if key_file.is_file():
            self.pubkey, self.privkey = self.import_keys()
        else:
            self.pubkey, self.privkey = rsa.newkeys(512)
            self.export_keys()

    def generate_salted_hash(self, input_str):
        salt = uuid.uuid4().hex
        return hashlib.sha256(
            salt.encode() + input_str.encode()).hexdigest() + ':' + salt

    def generate_asym_encryption(self, input_str):
        input_str = input_str.encode('utf8')
        return rsa.encrypt(input_str, self.pubkey).hex()

    def decyrpt_asym_encycryption(self, encrypted_str):
        decrypted_str = rsa.decrypt(bytes.fromhex(encrypted_str), privkey)
        return decrypted_str.decode('utf8')

    def export_keys(self):
        with open("Secrets/pubkey.pem", "wb") as prv_file:
            prv_file.write(self.pubkey.exportKey())
        with open("Secrets/privkey.pem", "wb") as prv_file:
            prv_file.write(self.privkey.exportKey())

    def import_keys(self):
        with open("Secrets/pubkey.pem", "rb") as prv_file:
            pubkey = rsa.importKey(prv_file.read())
        with open("Secrets/privkey.pem", "rb") as prv_file:
            privkey = rsa.importKey(prv_file.read())
        return pubkey, privkey
