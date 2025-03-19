# Ph4nt0m 1ntrud3r - Easy
## Description
A digital ghost has breached my defenses, and my sensitive data has been stolen! 😱💻 Your mission is to uncover how this phantom intruder infiltrated my system and retrieve the hidden flag.  
To solve this challenge, you'll need to analyze the provided PCAP file and track down the attack method. The attacker has cleverly concealed his moves in well timely manner. Dive into the network traffic, apply the right filters and show off your forensic prowess and unmask the digital intruder!
## Solution
Challenge cho ta một file pcap, mở bằng wireshark thấy những gói tin tcp rất không bình thường  
Sử dụng tool strings:
```
└─$ strings myNetworkTraffic.pcap 
X5w4OZo=:
H7DUfjk=:
ob0o5i0=:
y50ZdmI=:
y1vZtpY=:
hBFmx3U=:
b0gkDEE=:
fQ==:
cGljb0NURg==:
8WXUPlw=:
KWH98Vc=:
kpRM1Ck=:
ZTEwZTgzOQ==:
6dmdW8U=:
XzM0c3lfdA==:
FNoN3tc=:
bnRfdGg0dA==:
LJzhGLY=:
tXcY/Ew=:
YmhfNHJfOA==:
ezF0X3c0cw==:
FUiWx28=
```
Các mã bas64 có padding 2 dấu bằng là các phần của flag.
## Flag
```
picoCTF{1t_w4snt_th4t_34sy_tbh_4r_8e10e839}
```