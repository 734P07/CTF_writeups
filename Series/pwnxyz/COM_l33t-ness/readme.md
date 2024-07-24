# Pwnable.xyz l33t-ness
## Analysis
Challenge muốn ta vượt qua 3 vòng thử thách để lấy flag
```
undefined8 main(void)
{
  char check;
  
  setup();
  puts("The l33t-ness level.");
  check = round_1();
  if (check != '\0') {
    check = round_2();
    if (check != '\0') {
      check = round_3();
      if (check != '\0') {
        win();
      }
    }
  }
  return 0;
```
## Solution
Round 1: Nhập 2 số x, y sao cho x-y=1337, điều kiện 0 <= x, y < 1337
+ Nhập x = 1336 thỏa mãn điều kiện
+ Nhập y = 4294967295 = 0xffffffff để khi qua hàm atoi() chuyển thành số nguyên bù 2 có dấu là -1
```
undefined8 round_1(void)
{
  int numX;
  int numY;
  char *pcVar1;
  undefined8 check;
  long in_FS_OFFSET;
  char x [16];
  char y [24];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("=== 1eet ===");
  memset(x,0,0x20);
  printf("x: ");
  read(0,x,0x10);
  printf("y: ");
  read(0,y,0x10);
  pcVar1 = strchr(x,L'-');
  if (pcVar1 == (char *)0x0) {
    pcVar1 = strchr(y,L'-');
    if (pcVar1 == (char *)0x0) {
      numX = atoi(x);
      numY = atoi(y);
      if ((numX < 1337) && (numY < 1337)) {
        if (numX - numY == 1337) {
          check = 1;
        }
        else {
          check = 0;
        }
      }
      else {
        check = 0;
      }
      goto end;
    }
  }
  check = 0;
end:
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return check;

```
Round 2: Nhập 2 số x, y để x*y=1337 sao cho x >= 2, y >= 1338 
+ Sử dụng lỗi tràn số: khi x và y kiểu int nhưng x*y vượt quá INT_MAX, kết quả cuối cùng chỉ lấy 4 bytes cuối
+ 1337 = 0x539 => lấy x\*y = 0x100000539 = 9 * 477218737
```
undefined8 round_2(void)
{
  undefined8 check;
  long in_FS_OFFSET;
  int x;
  int y;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("=== t00leet ===");
  x = 0;
  y = 0;
  __isoc99_scanf("%d %d",&x,&y);
  if (((x < 2) || (y < 1338)) || (y * x != 1337)) {
    check = 0;
  }
  else {
    check = 1;
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return check;
}
```
Round 3: Nhập dãy không giảm gồm 5 số sao cho tổng dãy bằng tích dãy -> nhập toàn số 0
```
undefined8 round_3(void)

{
  long lVar1;
  undefined8 check;
  long in_FS_OFFSET;
  int i;
  int x [5];
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  puts("=== 3leet ===");
  x[0] = 0;
  x[1] = 0;
  x[2] = 0;
  x[3] = 0;
  x[4] = 0;
  __isoc99_scanf("%d %d %d %d %d",x,x + 1,x + 2,x + 3,x + 4);
  i = 1;
  do {
    if (4 < i) {
      if (x[4] + x[0] + x[1] + x[2] + x[3] == x[4] * x[0] * x[1] * x[2] * x[3]) {
        check = 1;
      }
      else {
        check = 0;
      }
return:
      if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return check;
    }
    if (x[i] < x[i + -1]) {
      check = 0;
      goto return;
    }
    i = i + 1;
  } while( true );
}
```
```
└─$ nc svc.pwnable.xyz 30008
The l33t-ness level.
=== 1eet ===
x: 1336
y: 4294967295
=== t00leet ===
9
477218737
=== 3leet ===
0
0
0
0
0
FLAG{1eet_t00leet_3leet_4z}
```
## Flag
```
FLAG{1eet_t00leet_3leet_4z}
```