import "pe"
import "math"

rule example_rule {
    strings:
        $name = "elcome to the YaraRules0x100 cha"
    condition: 
        (math.entropy(0, filesize) >= 6.2 and $name) or // pe.imports không tìm được những api thật sự trong packed file
        (math.entropy(0, filesize) < 6.2 and 
            pe.imports("kernel32.dll", "GetProcAddress") and
            pe.imports("kernel32.dll", "CreateThread") and
            pe.imports("kernel32.dll", "CreateProcessA") and
            pe.imports("kernel32.dll", "GetExitCodeProcess") and
            pe.imports("advapi32.dll", "OpenProcessToken") and
            pe.imports("advapi32.dll", "AdjustTokenPrivileges"))
}

// picoCTF{yara_rul35_r0ckzzz_0222db39}