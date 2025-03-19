#!/usr/bin/python3
from pwn import *
import random
import time

def get_random(length, seed):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed(seed)  # seeding with current time 
    s = ""
    for i in range(length):
        s += random.choice(alphabet)
    return s

t1 = int(time.time() * 1000)
con = remote("verbal-sleep.picoctf.net", 49550)
con.recv(1)
t2 = int(time.time() * 1000)

log.success(f"RTT: {t2-t1}")

for _ in range(50):
    seed = random.randint(t1,t2)
    con.sendlineafter(b"your guess for the token (or exit):", get_random(20, seed))
    res = con.recvline()
    if (b"Congratulations" in res):
        log.success(res)
        break

con.interactive()

# picoCTF{UseSecure#$_Random@j3n3r@T0rs82488c9a}
