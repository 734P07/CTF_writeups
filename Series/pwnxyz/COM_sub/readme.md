# Pwnable.xyz Sub
## Analysis
Ch&#432;&#417;ng tr&#236;nh mu&#7889;n ta nh&#7853;p 2 s&#7889; nh&#7887; h&#417;n 0x1337 sau &#273;&#243; t&#237;nh hi&#7879;u, n&#7871;u k&#7871;t qu&#7843; l&#224; 0x1337 th&#236; in ra flag
```
undefined8 FUN_00100850(void)
{
  long in_FS_OFFSET;
  int local_18;
  int local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  FUN_00100a3e();
  local_18 = 0;
  local_14 = 0;
  __printf_chk(1,"1337 input: ");
  __isoc99_scanf("%u %u",&local_18,&local_14);
  if ((local_18 < 0x1337) && (local_14 < 0x1337)) {
    if (local_18 - local_14 == 0x1337) {
      system("cat /flag");
    }
  }
  else {
    puts("Sowwy");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
M&#7863;c d&#249; h&#224;m scanf() d&#249;ng &#273;&#7883;nh d&#7841;ng %u nh&#432;ng ta v&#7851;n c&#243; th&#7875; nh&#7853;p s&#7889; &#226;m
## Solution
```
└─$ nc svc.pwnable.xyz 30001
1337 input: 4918 -1
FLAG{sub_neg_==_add}
```
## Flag
```
FLAG{sub_neg_==_add}
```