#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

con = process()
#gdb.attach(con, gdbscript = "start")

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

#con = remote("jupiter.challenges.picoctf.org", 18263)

exit_add = 0xac8
elf.asm(exit_add, "call 0xa21")
ins = elf.read(exit_add, 5)
print(int(ins, 16))

# con.interactive()
