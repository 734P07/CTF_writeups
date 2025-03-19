# YaraRules0x100 - Medium
## Description
Dear Threat Intelligence Analyst,  
Quick heads up - we stumbled upon a shady executable file on one of our employee's Windows PCs. Good news: the employee didn't take the bait and flagged it to our InfoSec crew.  
Seems like this file sneaked past our Intrusion Detection Systems, indicating a fresh threat with no matching signatures in our database.  
Can you dive into this file and whip up some YARA rules? We need to make sure we catch this thing if it pops up again.  
Thanks a bunch!
## Analysis
Challenge muốn ta viết yararule phát hiện các biến thể của một file exe nghi là mã độc. Đồng thời rule phải vượt qua 64 testcase cho trước mà không bị âm tính giả hoặc dương tính giả.  
Dùng tool DIE biết được file được pack bằng UPX. Sử dụng string `"elcome to the YaraRules0x100 cha"` để phát hiện biến thể này.  
Với biến thể unpacked, ta sẽ xem file có import api nào chỉ có thể được sử dụng bởi các mã độc hay không.  
Ngoài ra, ta sẽ phân loại biến thể packed và unpacked bằng entropy.
## Solution
```
import "pe"
import "math"

rule example_rule {
    strings:
        $name = "elcome to the YaraRules0x100 cha"
    condition: 
        (math.entropy(0, filesize) >= 6.2 and $name) or
        (math.entropy(0, filesize) < 6.2 and 
            pe.imports("kernel32.dll", "GetProcAddress") and
            pe.imports("kernel32.dll", "CreateThread") and
            pe.imports("kernel32.dll", "CreateProcessA") and
            pe.imports("kernel32.dll", "GetExitCodeProcess") and
            pe.imports("advapi32.dll", "OpenProcessToken") and
            pe.imports("advapi32.dll", "AdjustTokenPrivileges"))
}
```
## Flag
```
picoCTF{yara_rul35_r0ckzzz_0222db39}
```