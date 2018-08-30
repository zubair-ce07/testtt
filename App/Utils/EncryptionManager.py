import hashlib
import uuid
import Crypto
import ast
import rsa
from pathlib import Path


class EncryptionManager:
    '''This is class is responsible for
    encryption & decryptions'''

    def __init__(self):
        key_file = Path("Secrets/pubkey.pem")
        if key_file.is_file():
            self.pubkey, self.privkey = self.import_keys()
        else:
            self.pubkey, self.privkey = rsa.newkeys(512)
            self.export_keys()

    def generate_salted_hash(self, input_str):
        salt = uuid.uuid4().hex
        return hashlib.sha256(
            salt.encode() + input_str.encode()).hexdigest() + ':' + salt

    def match_salted_hash(self, salted_hash, word):
        hash_str, salt = salted_hash.split(':')
        return hash_str == hashlib.sha256(
            salt.encode() + word.encode()).hexdigest()

    def generate_asym_encryption(self, input_str):
        input_str = input_str.encode('utf8')
        return rsa.encrypt(input_str, self.pubkey).hex()

    def decyrpt_asym_encycryption(self, encrypted_str):
        decrypted_str = rsa.decrypt(bytes.fromhex(encrypted_str), self.privkey)
        return decrypted_str.decode('utf8')

    def export_keys(self):
        with open("Secrets/pubkey.pem", "w") as pub_file:
            pub_file.write(self.pubkey.save_pkcs1(
                format='PEM').decode('ascii'))
        with open("Secrets/privkey.pem", "w") as prv_file:
            prv_file.write(self.privkey.save_pkcs1(
                format='PEM').decode('ascii'))

    def import_keys(self):
        with open("Secrets/pubkey.pem", "rb") as pub_file:
            pubkey = rsa.PublicKey.load_pkcs1(pub_file.read())
        with open("Secrets/privkey.pem", "rb") as prv_file:
            privkey = rsa.PrivateKey.load_pkcs1(prv_file.read())
        return pubkey, privkey
