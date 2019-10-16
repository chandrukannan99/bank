from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import math

hash = "SHA-256"

def new_keys(keysize):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private


def import_key(externKey):
    return RSA.importKey(externKey)


def get_public_key(priv_key):
    return priv_key.publickey()


def encrypt(message, pub_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)


def decrypt(ciphertext, priv_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)


def sign(message, priv_key, hashAlg="SHA-256"):
    global hash
    hash = hashAlg
    signer = PKCS1_v1_5.new(priv_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.sign(digest)


def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.verify(digest, signature)


def one_line_format(pem_key):
    to_remove_strs = [
        '-----BEGIN PUBLIC KEY-----',
        '-----END PUBLIC KEY-----',
        '-----BEGIN RSA PRIVATE KEY-----',
        '-----END RSA PRIVATE KEY-----',
        '\n',
    ]

    for to_remove in to_remove_strs:
        pem_key = pem_key.replace(to_remove, '')

    return pem_key


def pem_format(one_line_key):
    pem = ''

    for i in range(int(math.ceil(len(one_line_key) / 64))):
        pem += one_line_key[i * 64: (i + 1) * 64] + '\n'

    if len(one_line_key) > 500:
        return '-----BEGIN RSA PRIVATE KEY-----\n' + pem + '-----END RSA PRIVATE KEY-----'

    else:
        return '-----BEGIN PUBLIC KEY-----\n' + pem + '-----END PUBLIC KEY-----'
