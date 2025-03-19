#!/usr/bin/python3
from pwn import *
from Crypto.Cipher import ChaCha20_Poly1305
from cryptomath import divceil

from sympy import GF, Poly
from sympy.abc import r

con = remote("activist-birds.picoctf.net", 62900)

goal = b"But it's only secure if used correctly!"

messages = [
    b"Did you know that ChaCha20-Poly1305 is an authenticated encryption algorithm?",
    b"That means it protects both the confidentiality and integrity of data!"
]

## Chacha20
def encrypt(message, key, nonce):
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    return ciphertext + tag + nonce

def decrypt(message_enc, key, nonce):
    ciphertext = message_enc[:-28]
    tag = message_enc[-28:-12]
    nonce = message_enc[-12:]
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

## Poly1305
P = 0x3fffffffffffffffffffffffffffffffb # 2^130-5

def le_bytes_to_num(data):
    """Convert a number from little endian byte format"""
    ret = 0
    for i in range(len(data) - 1, -1, -1):
        ret <<= 8
        ret += data[i]
    return ret

def num_to_16_le_bytes(num):
    """Convert number to 16 bytes in little endian format"""
    ret = [0]*16
    for i, _ in enumerate(ret):
        ret[i] = num & 0xff
        num >>= 8
    return bytearray(ret)

def create_tag(data, r, s, coef: list):
    """Calculate authentication tag for data"""
    acc = 0
    for i in range(0, divceil(len(data), 16)):
        n = le_bytes_to_num(data[i*16:(i+1)*16] + b'\x01')
        coef.append(n)
        acc += n
        acc = (r * acc) % P
    global tmp
    tmp = acc
    acc += s
    return num_to_16_le_bytes(acc)

def find_s(data, r):
    """Calculate authentication tag for data"""
    acc = 0
    for i in range(0, divceil(len(data), 16)):
        n = le_bytes_to_num(data[i*16:(i+1)*16] + b'\x01')
        acc += n
        acc = (r * acc) % P
    return 

con.recvuntil(b"Plaintext (hex): ")
plain1 = bytes.fromhex(con.recv(77*2).decode())
con.recvuntil(b"Ciphertext (hex): ")
enc_message1 = bytes.fromhex(con.recv(105*2).decode())

con.recvuntil(b"Plaintext (hex): ")
plain2 = bytes.fromhex(con.recv(70*2).decode())
con.recvuntil(b"Ciphertext (hex): ")
enc_message2 = bytes.fromhex(con.recv(98*2).decode())

# nonce là 12 bytes cuối cipher
nonce = enc_message1[-12:]
tag1 = enc_message1[-28:-12]
tag2 = enc_message2[-28:-12]
# key_stream(key, nonce) là cipher ^ plain
cipher1 = enc_message1[:-28]
cipher2 = enc_message2[:-28]
key_stream = xor(cipher1, plain1)

log.success("Nonce: " + nonce.hex())
log.success("Tag 1: " + tag1.hex())
log.success("Tag 2: " + tag2.hex())
log.success("Key stream: " + key_stream.hex())

### Stage 1: tính cipher chacha20
goal_cipher = xor(key_stream, goal)[:len(goal)]
log.success("Goal_cipher: " + goal_cipher.hex())

### Stage 2: tính mac tag
#### Stage 2.1: lấy thông tin
tag1_num = le_bytes_to_num(tag1)
tag2_num = le_bytes_to_num(tag2)
log.success("Tag 1 to num: " + hex(tag1_num))
log.success("Tag 2 to num: " + hex(tag2_num))
log.success("Tag1 - tag2: " + hex(tag1_num - tag2_num))

a = [] # hệ số đa thức 1
b = [] # hệ số đa thức 2
create_tag(cipher1, 0, 0, a)
create_tag(cipher2, 0, 0, b)

#### Stage 2.2: giải đa thức tìm r
print("Đang tìm r...")
f = Poly((a[0]-b[0])*r**5 + (a[1]-b[1])*r**4 + (a[2]-b[2])*r**3 + (a[3]-b[3])*r**2 + (a[4]-b[4])*r, r, modulus=P)
roots = f.ground_roots()
print(list(roots.keys()))
create_tag(messages[0], list(roots.keys())[-1], 0, [])
s1 = tag1_num - tmp
print(hex(tmp))

# payload = encrypt(goal.encode(), key_stream, nonce)
# con.sendafter(b"s your message?", payload.hex())
# log.success(decrypt(plain1, key_stream, nonce))

con.interactive()
