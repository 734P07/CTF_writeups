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
