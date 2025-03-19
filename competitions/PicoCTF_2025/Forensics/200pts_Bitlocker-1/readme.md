# Bitlocker-1 - Medium
## Description
Jacky is not very knowledgable about the best security passwords and used a simple password to encrypt their BitLocker drive. See if you can break through the encryption!
## Solution
Challenge cho ta một file diskdump được mã hóa bằng bitlocker. Với thông tin đã biết là mật khẩu được sử dụng rất yếu thì bài này chỉ cần crack hash là đã xong.  
Lấy hash của password sử dụng tool `bitlocker2john`
```
bitlocker2john -i bitlocker-1.dd > bitlocker_hash.txt
```
Dùng hashcat bruteforce được mật khẩu là `jacqueline` (sử dụng mode 22100 cho bitlocker)
```
hashcat -m 22100 userpw_hash.txt rockyou.txt --force
```
Dùng `dislocker` mở khóa bằng mật khẩu của user đã tìm
```
sudo dislocker -V bitlocker-1.dd -u"jacqueline" -- /mnt/bitlocker/
```
Mount dislocker file với một directory bất kỳ (lưu ý ntfs)
```
sudo mount -t ntfs-3g -r -o loop /mnt/bitlocker/dislocker-file /mnt/decrypted/
```
Truy cập vào và lấy flag
## Flag
```
picoCTF{us3_b3tt3r_p4ssw0rd5_pl5!_3242adb1}
```