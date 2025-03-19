# Binary Instrumentation 2 - Medium
## Description
I've been learning more Windows API functions to do my bidding. Hmm... I swear this program was supposed to create a file and write the flag directly to the file. Can you try and intercept the file writing function to see what went wrong?
## Solution
Challenge nói rõ sẽ tạo và ghi file nên ta sử dụng frida-trace các api `CreateFileA`, `WriteFile`  
Xem args (tham số) của CreateFileA thấy được dev đã quên thay tên file vào template `<Insert path here>`, dẫn đến lỗi  
Sau khi thay tham số thứ nhất của CreateFileA thành `./flag` thì chương trình hoạt động bình thường
```
└─$ frida .\bininst2.exe -l .\hook.js

Spawning `.\bininst2.exe`...
Spawned `.\bininst2.exe`. Resuming main thread!
[Local::bininst2.exe ]-> File path: <Insert path here>

File path replaced: ./flag
Result: 0x288
Content: cGljb0NURntmcjFkYV9mMHJfYjFuX2luNXRydW0zbnQ0dGlvbiFfYjIxYWVmMzl9
Result: 0x1
Process terminated
```
## Flag
```
picoCTF{fr1da_f0r_b1n_in5trum3nt4tion!_b21aef39}
```