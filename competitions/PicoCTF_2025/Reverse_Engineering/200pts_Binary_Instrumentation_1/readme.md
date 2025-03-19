# Binary Instrumentation 1 - Medium
## Description
I have been learning to use the Windows API to do cool stuff! Can you wake up my program to get the flag?
## Solution
Sử dụng DIE với file pe được cho thấy nó đã bị pack  
Có gợi ý `wake up my program` -> dùng frida-trace xem chương trình có thực thi hàm `Sleep` hay không:
```
frida-trace -i "Sleep" .\bininst1.exe
```
Sử dụng kĩ thuật hook để thay đổi tham số của hàm sleep về 0:
```
└─$ frida .\bininst1.exe -l .\hook.js
Spawned `.\bininst1.exe`. Resuming main thread!
[Local::bininst1.exe ]-> Hi, I have the flag for you just right here!
I'll just take a quick nap before I print it out for you, should only take me a decade or so!
zzzzzzzz....
Ok, I'm Up! The flag is: cGljb0NURnt3NGtlX20zX3VwX3cxdGhfZnIxZGFfZjI3YWNjMzh9
```
## Flag
```
picoCTF{w4ke_m3_up_w1th_fr1da_f27acc38}
```