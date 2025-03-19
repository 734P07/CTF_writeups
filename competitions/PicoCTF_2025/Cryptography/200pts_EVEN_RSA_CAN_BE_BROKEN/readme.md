# EVEN RSA CAN BE BROKEN??? - Easy
## Description
This service provides you an encrypted flag. Can you decrypt it with just N & e?
## Solution
Challenge cho ta N, e và c trong một hệ RSA.  
Để ý thấy N chia hết cho 2. Ta gán `q = 2` và `p = N/2`. Từ p và q tính được `phi` và khóa bí mật `d`. Sau đó dùng khóa bí mật để giải mã từ `c`
## Flag
```
picoCTF{tw0_1$_pr!m33486c703}
```