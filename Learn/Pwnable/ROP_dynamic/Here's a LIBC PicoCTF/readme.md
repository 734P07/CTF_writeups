# Here's a LIBC PicoCTF

Challenge cho chúng ta file binary và file libc. Sử dụng pwninit để liên kết chúng lại:
```
$  sudo pwninit
bin: ./vuln
libc: ./libc.so.6

fetching linker
https://launchpad.net/ubuntu/+archive/primary/+files//libc6_2.27-3ubuntu1.2_amd64.deb
setting ./ld-2.27.so executable
copying ./vuln to ./vuln_patched
running patchelf on ./vuln_patched
writing solve.py stub
```

File và checksec:
```
$  file vuln
vuln: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=e5dba3e6ed29e457cd104accb279e127285eecd0, not stripped
$  checksec vuln
[*] '/home/tornad/ctf/vuln'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    RUNPATH:  b'./'
```
Dịch ngược trong ghidra thấy hàm do_stuff dính lỗi buffer overflow:
```
void do_stuff(void)

{
  char cVar1;
  undefined local_89;
  char buf [112];
  undefined8 local_18;
  ulong local_10;
  
  local_18 = 0;
  __isoc99_scanf("%[^\n]",buf);
  __isoc99_scanf(&DAT_0040093a,&local_89);
  for (local_10 = 0; local_10 < 100; local_10 = local_10 + 1) {
    cVar1 = convert_case((int)local_88[local_10],local_10);
    local_88[local_10] = cVar1;
  }
  puts(local_88);
  return;
}
```
Kịch bản khai thác: Sử dụng hàm puts trong libc leak địa chỉ hàm system("/bin/sh") và lấy được shell  
Tính padding:
```
gef➤  ni
abcd
0x0000000000400703 in do_stuff ()
[ Legend: Modified register | Code | Heap | Stack | String ]
──────────────────────────────────────────────────────────────────────────────────────registers ────
$rax   : 0x1
$rbx   : 0x0
$rcx   : 0x00007ffff7dcfa00  →  0x00000000fbad2288
$rdx   : 0x00007ffff7dd18d0  →  0x0000000000000000
$rsp   : 0x00007fffffffddc0  →  0x00007ffff7dd07e3  →  0xdd18c0000000000a ("\n"?)
$rbp   : 0x00007fffffffde50  →  0x00007fffffffdf00  →  0x00000000004008b0  →  <__libc_csu_init+0> push r15
$rsi   : 0x1
$rdi   : 0x0
$rip   : 0x0000000000400703  →  <do_stuff+43> lea rax, [rbp-0x81]
$r8    : 0x0
$r9    : 0x0
$r10   : 0x0
$r11   : 0x0000000000400939  →   add BYTE PTR [rip+0x63], ah        # 0x4009a2
$r12   : 0x1b
$r13   : 0x0
$r14   : 0x1b
$r15   : 0x0
$eflags: [zero carry parity adjust sign trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00
─────────────────────────────────────────────────────────────────────────────────────────────stack ────
0x00007fffffffddc0│+0x0000: 0x00007ffff7dd07e3  →  0xdd18c0000000000a ("\n"?)    ← $rsp
0x00007fffffffddc8│+0x0008: 0x00007ffff7a70fc1  →  <__GI__IO_do_write+177> mov rbp, rax
0x00007fffffffddd0│+0x0010: 0x00007f0064636261 ("abcd"?)
0x00007fffffffddd8│+0x0018: 0x00007ffff7dd0760  →  0x00000000fbad2887
0x00007fffffffdde0│+0x0020: 0x000000000000000a ("\n"?)
0x00007fffffffdde8│+0x0028: 0x00007fffffffde60  →  "WeLcOmE To mY EcHo sErVeR!"
0x00007fffffffddf0│+0x0030: 0x00007ffff7dcc2a0  →  0x0000000000000000
0x00007fffffffddf8│+0x0038: 0x000000000000001b
──────────────────────────────────────────────────────────────────────────────────────code:x86:64 ────
     0x4006f2 <do_stuff+26>    lea    rdi, [rip+0x23b]        # 0x400934
     0x4006f9 <do_stuff+33>    mov    eax, 0x0
     0x4006fe <do_stuff+38>    call   0x400580 <__isoc99_scanf@plt>
 →   0x400703 <do_stuff+43>    lea    rax, [rbp-0x81]
     0x40070a <do_stuff+50>    mov    rsi, rax
     0x40070d <do_stuff+53>    lea    rdi, [rip+0x226]        # 0x40093a
     0x400714 <do_stuff+60>    mov    eax, 0x0
     0x400719 <do_stuff+65>    call   0x400580 <__isoc99_scanf@plt>
     0x40071e <do_stuff+70>    mov    QWORD PTR [rbp-0x8], 0x0
───────────────────────────────────────────────────────────────────────────────────────────threads ────
[#0] Id 1, Name: "vuln_patched", stopped 0x400703 in do_stuff (), reason: SINGLE STEP
─────────────────────────────────────────────────────────────────────────────────────────────trace ────
[#0] 0x400703 → do_stuff()
[#1] 0x4008a0 → main()
───────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  i frame
Stack level 0, frame at 0x7fffffffde60:
 rip = 0x400703 in do_stuff; saved rip = 0x4008a0
 called by frame at 0x7fffffffdf10
 Arglist at 0x7fffffffde50, args:
 Locals at 0x7fffffffde50, Previous frame's sp is 0x7fffffffde60
 Saved registers:
  rbp at 0x7fffffffde50, rip at 0x7fffffffde58
```
Padding = 0x7fffffffde58 - 0x00007fffffffddd0 = 136  
Code khai thác:
