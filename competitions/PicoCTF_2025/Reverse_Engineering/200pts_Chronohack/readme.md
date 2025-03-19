# Chronohack - Medium
## Description
Can you guess the exact token and unlock the hidden flag?  
Our school relies on tokens to authenticate students. Unfortunately, someone leaked an important file for token generation. Guess the token to get the flag.
## Solution
Challenge cho file [source code](./token_generator.py) có chức năng kiểm tra xem input của người dùng có khớp với token được generate random hay không. User được đoán tối đa 50 lần.  
Seed được sử dụng cho hàm random là giá trị thời gian thực. Tức là ta chỉ cần làm thế nào đồng bộ local với remote là được.  
Vấn đề là làm thế nào để lấy chính xác giá trị thời gian ở thời điểm server set seed cho hàm random?  
Dựa theo bài viết [này](https://captain-woof.medium.com/picoctf-seed-spring-walkthrough-going-toe-to-toe-with-time-4ed35e16889b), nếu ta gửi request cho server tại thời điểm t<sub>1</sub> = 0, request đó sẽ không thể đến server ngay lập tức mà sẽ luôn đến nơi vào thời điểm t<sub>1.5</sub> > t<sub>1</sub>, sau đó response của server sẽ được gửi tới client vào thời điểm t<sub>2</sub>. Vì vậy giá trị thời gian được sử dụng làm seed có thể là bất cứ giá trị `x` nào với t<sub>1</sub> < x < t<sub>2</sub>.  
Từ lập luận trên, ta sẽ chạy [mã khai thác](./exp.py) vài lần, với mỗi lần sẽ ghi lại t1 và t2 tương ứng rồi random seed x trong khoảng đó.  
Việc còn lại là hi vọng sẽ có một lần khai thác thành công.
## Flag
```
picoCTF{UseSecure#$_Random@j3n3r@T0rs82488c9a}
```