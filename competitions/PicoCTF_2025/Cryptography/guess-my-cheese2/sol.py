from hashlib import sha256

with open('./cheese_list.txt', 'r') as f1, open('./out4.txt', 'w') as f2:
    for line in f1:
        for i in range(0x20, 0x7e+1):
            for j in range(0x20, 0x7e+1):
                for k in range(0x20, 0x7e+1):
                    # print(salt)
                    f2.write(sha256(line.strip().encode() + bytes.fromhex(hex(i)[2:].rjust(2, '0')) + bytes.fromhex(hex(j)[2:].rjust(2, '0')) + bytes.fromhex(hex(k)[2:].rjust(2, '0'))).hexdigest() + "\n")