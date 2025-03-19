# Rust fixme 1/2/3 - Easy
## Description
1. Have you heard of Rust? Fix the syntax errors in this Rust file to print the flag!  
2. The Rust saga continues? I ask you, can I borrow that, pleeeeeaaaasseeeee?  
3. Have you heard of Rust? Fix the syntax errors in this Rust file to print the flag!
## Solution
Các phần của Rust fixme đều có những lỗi syntax trong code, ta chỉ cần sửa cho đúng là sẽ ra flag:  
1. Tải rust và cargo. Thêm `;`, sửa lại format string và keyword `return`
2. Sửa tham số `String` thành `&mut String` thì function mới có thể chỉnh sửa trực tiếp được.
3. Bỏ comment `unsafe`. Unsafe dùng để bỏ qua các đảm bảo an toàn của Rust, đổi lại ta sẽ có quyền kiểm soát bộ nhớ tốt hơn.
## Flag
```
1. picoCTF{4r3_y0u_4_ru$t4c30n_n0w?}
2. picoCTF{4r3_y0u_h4v1n5_fun_y31?}
3. picoCTF{n0w_y0uv3_f1x3d_1h3m_411}
```