# Bitlocker-2 - Medium
## Description
Jacky has learnt about the importance of strong passwords and made sure to encrypt the BitLocker drive with a very long and complex password. We managed to capture the RAM while this drive was opened however. See if you can break through the encryption!
## Solution
Phần 2 cơ bản giống phần 1, có khác là Jacky đã dùng mật khẩu mạnh hơn nên bruteforce hash sẽ không còn hiệu quả. Ngoài ra chall có cung cấp thêm 1 file `RAM dump`.  
Để giải mã một disk bị mã hóa bằng bitlocker có nhiều cách: user password, vmk hoặc fvek...  
Hãy đọc thêm [bài viết này](https://noinitrd.github.io/Memory-Dump-UEFI/) nói về phương pháp lấy fvek (full volume encryption keys) từ ram dump.  
Sử dụng `volatility 2` phiên bản mới nhất biết được profile của ram dump là Win10x64_19041  
Tải plugin [bitlocker](https://github.com/breppo/Volatility-BitLocker) có hỗ trợ win 10 để giải bài này.  
Extract fvek file từ ram dump:
```
python2.7 vol.py -f memdump.mem bitlocker --profile Win10x64_19041 --dislocker .
```
Có tất cả 4 file fvek. Sử dùng dislocker để giải mã và mount thử với từng file:
```
sudo dislocker -V bitlocker-2.dd -k ./0x9e8879926a50-Dislocker.fvek -- /mnt/bitlocker/
sudo mount -t ntfs-3g -r -o loop /mnt/bitlocker/dislocker-file /mnt/decrypted/
```
## Flag
```
picoCTF{B1tl0ck3r_dr1v3_d3crypt3d_9029ae5b}
```