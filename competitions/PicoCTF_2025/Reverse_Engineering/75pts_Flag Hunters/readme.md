# Flag Hunters - Easy
## Description
Lyrics jump from verses to the refrain kind of like a subroutine call. There's a hidden refrain this program doesn't print by default. Can you get it to print it? There might be something in it for you.
## Solution
Challenge cho ta source code trong file [lyric-reader.py](./lyric-reader.py). Code khá dài nhưng ta chỉ tập trung vài điểm chính.  
Cách hoạt động của hàm `reader`:  
    + In ra lời bài hát bắt đầu từ `[VERSE1]`  
    + Khi tới dòng `CROWD (Singalong here!);`, yêu cầu nhập input  
    + Khi gặp dòng có dạng `RETURN X`, nhảy đến dòng thứ X trong bài hát  
Flag nằm ở phần đầu của bài hát, nhưng sẽ không in ra theo mặc định.  
Mặt khác, chương trình coi dòng đầu tiên ở sau dấu `;` là lệnh  
Như vậy ta chỉ cần nhập payload `;RETURN 0` để chương trình nhảy về câu hát đầu tiên, từ đó in ra flag.
## Flag
```
picoCTF{70637h3r_f0r3v3r_ac197d12}
```