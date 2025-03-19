# Event-Viewing - Medium
## Description
One of the employees at your company has their computer infected by malware! Turns out every time they try to switch on the computer, it shuts down right after they log in. The story given by the employee is as follows:  
1. They installed software using an installer they downloaded online  
2. They ran the installed software but it seemed to do nothing  
3. Now every time they bootup and login to their computer, a black command prompt screen quickly opens and closes and their computer shuts down instantly.  

See if you can find evidence for the each of these events and retrieve the flag (split into 3 pieces) from the correct logs!
## Solution
Mở file event log mà chall đã cho trong Event Viewer, tìm 3 phần của flag tương ứng với mô tả của đề bài.  
1. Họ đã cài một phần mềm sử dụng installer mà họ đã tải từ trước đó. Ta sẽ tìm các log có id 11707, 1033 (liên quan đến **MsiInstaller**).  
Tìm được 1 mã base64 `cGljb0NURntFdjNudF92aTN3djNyXw==` -> `picoCTF{Ev3nt_vi3wv3r_` trong 1 log có id 1033
2. Họ chạy thử phần mềm vừa được tải nhưng không có gì xảy ra.  
Tìm các log có id 4688, 1 (tạo process).  
Ngoài ra phần mềm có thể tác động đến các registry `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` hoặc `HKLM\Software\Microsoft\Windows\CurrentVersion\Run` để tự chạy mỗi lần mở máy (id 4657).  
Tìm được 1 mã base64 `MXNfYV9wcjN0dHlfdXMzZnVsXw==` -> `1s_a_pr3tty_us3ful_` trong 1 log có id 4657
3. Có một cmd hiện lên và tự động tắt máy mỗi khi họ login vào máy.  
Kiểm tra các log id 1074, 6006, 6008 (shutdown)  
Tìm được 1 mã base64 `dDAwbF84MWJhM2ZlOX0=` -> `t00l_81ba3fe9}` trong 1 log có id 1074
## Flag
```
picoCTF{Ev3nt_vi3wv3r_1s_a_pr3tty_us3ful_t00l_81ba3fe9}
```