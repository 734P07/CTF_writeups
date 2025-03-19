# perplexed - Medium
## Solution
Challenge chỉ cho ta một binary có chức năng kiểm tra password mà user nhập vào.  
Decompile xem hàm `check` bằng IDA:
```
__int64 __fastcall check(const char *a1)
{
  __int64 v2; // rbx
  __int64 v3; // [rsp+10h] [rbp-50h]
  _QWORD v4[3]; // [rsp+18h] [rbp-48h]
  int v5; // [rsp+34h] [rbp-2Ch]
  int v6; // [rsp+38h] [rbp-28h]
  int v7; // [rsp+3Ch] [rbp-24h]
  int j; // [rsp+40h] [rbp-20h]
  unsigned int i; // [rsp+44h] [rbp-1Ch]
  int v10; // [rsp+48h] [rbp-18h]
  int v11; // [rsp+4Ch] [rbp-14h]

  if ( strlen(a1) != 27 )
    return 1LL;
  v3 = 0x617B2375F81EA7E1LL;
  v4[0] = 0xD269DF5B5AFC9DB9LL;
  *(_QWORD *)((char *)v4 + 7) = 0xF467EDF4ED1BFED2LL;
  v11 = 0;
  v10 = 0;
  v7 = 0;
  for ( i = 0; i <= 0x16; ++i )
  {
    for ( j = 0; j <= 7; ++j )
    {
      if ( !v10 )
        v10 = 1;
      v6 = 1 << (7 - j);
      v5 = 1 << (7 - v10);
      if ( (v6 & *((char *)&v4[-1] + (int)i)) > 0 != (v5 & a1[v11]) > 0 )
        return 1LL;
      if ( ++v10 == 8 )
      {
        v10 = 0;
        ++v11;
      }
      v2 = v11;
      if ( v2 == strlen(a1) )
        return 0LL;
    }
  }
  return 0LL;
}
```
Hàm `check` thực hiện các công việc sau:  
    + Nếu độ dài input không phải là 27 thì thoát chương trình  
    + So lần lượt từng khoảng 7 bits của giá trị đã được hardcoded với từng kí tự trong input của user.  
Dump giá trị được hardcoded đó ra, chia từng khoảng 7 bits và chuyển sang dạng text là sẽ có flag.  
[Script giải mã](./sol.py)
## Flag
```
picoCTF{0n3_bi7_4t_a_7im3}
```