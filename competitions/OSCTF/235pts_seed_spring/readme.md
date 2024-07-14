# seed sPRING
## Analysis
Chương trình muốn ta đoán đúng số random 30 lần
```
undefined4 main(void) {
  uint local_20;
  uint local_1c;
  uint local_18;
  int local_14;
  undefined *local_10;
  
  local_10 = &stack0x00000004;
  welcome()
  puts("Welcome! The game is easy: you jump on a sPRiNG.");
  puts("How high will you fly?");
  puts("");
  fflush(_stdout);
  local_18 = time((time_t *)0x0);
  srand(local_18);
  local_14 = 1;
  while( true ) {
    if (0x1e < local_14) {
      puts("Congratulation! You\'ve won! Here is your flag:\n");
      get_flag();
      fflush(_stdout);
      return 0;
    }
    printf("LEVEL (%d/30)\n",local_14);
    puts("");
    local_1c = rand();
    local_1c = local_1c & 0xf;
    printf("Guess the height: ");
    fflush(_stdout);
    __isoc99_scanf(&DAT_00010c9a,&local_20);
    fflush(_stdin);
    if (local_1c != local_20) break;
    local_14 = local_14 + 1;
  }
  puts("WRONG! Sorry, better luck next time!");
  fflush(_stdout);
                    /* WARNING: Subroutine does not return */
  exit(-1);
}
```
## Solution
Do seed được sử dụng dựa trên thời gian thực, ta chỉ cần viết 1 chương trình tương tự
```
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
 
int main(){
    int r;
    srand(time(0));
    for(int i = 0; i < 30; ++i){
        r = rand() & 0xf;
        printf("%d\n", r);
    }    
}
```
```
└─$ ./exp | nc 34.125.199.248 2534
```
## Flag
```
OSCTF{th1s_w4snt_phys1cs_lm4o}
```