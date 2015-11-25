import hashlib
import base64
from Crypto import Random
from Crypto.Cipher import AES
import sys

class AESCipher(object):
    def __init__(self,key,blocksize):
        self.key=hashlib.sha256(key.encode()).digest()
        self.blocksize=int(blocksize)

    def encrypt(self,PT):
        PT=self._pad(PT)
        IV=Random.new().read(AES.block_size)
        cipher=AES.new(self.key,AES.MODE_CBC,IV)
        CT=base64.b64encode(IV+cipher.encrypt(PT))
        return CT

    def decrypt(self,CT):
        enc=base64.b64decode(CT)
        IV=enc[:16]#the first 16 are IV
        cipher=AES.new(self.key,AES.MODE_CBC,IV)
        return self._unpadd(cipher.decrypt(enc[AES.block_size:])).decode("utf-8")

    def _pad(self,s):
        return s+chr(self.blocksize-len(s)%self.blocksize)*(self.blocksize-len(s)%self.blocksize)

    def _unpadd(self,s):
        return s[:-ord(s[len(s)-1:])]
