# Quantum Scrambler - Medium
## Description
We invented a new cypher that uses "quantum entanglement" to encode the flag. Do you have what it takes to decode it?
## Solution
Bài này nếu reverse thì sẽ khá khó hiểu. Cách đơn giản hơn là cho một vài plaintext đã biết đi qua hàm `scramble`, từ đó tìm ra quy luật và viết [script](./sol.py) giải mã.  
VD:  
    + scramble([[1], [2]]) = [[1], [2]]  
    + scramble([[1], [2], [3]]) = [[1, 2], [3, []]]  
    + scramble([[1], [2], [3], [4]]) = [[1, 2], [3, []], [4]]  
    + scramble([[1], [2], [3], [4], [5]]) = [[1, 2], [3, [], 4], [5, [[1, 2]]]]  
## Flag
```
picoCTF{python_is_weirde2a45ca5}
```