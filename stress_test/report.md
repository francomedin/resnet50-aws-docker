Report:
Computer caracateristics:
- Intel(R) Core(TM) i5-2450M CPU @ 2.50GHz   2.50 GHz
- Ram 6,00 GB
First Round:
- Number of users: 100 
- Spawn Rate: 3
- time: 10 minutes
- Weigth: index(1) ; predict(3) 
- Not Scaled
--------Results: 
--Get:
Requests: 396
Fails: 0
rps : 0.7
-- Post:
Requests: 1203
Fails: 117
rps : 2.0

Second Round:
- Number of users: 100 
- Spawn Rate: 3
- time: 10 minutes
- Weigth: index(1) ; predict(3) 
- Scaled: --scale model=3

--------Results: 
--Get:
Requests: 603
Fails: 0
rps : 1.0
-- Post:
Requests: 1620
Fails: 73
rps : 2.7

Conclusion: Although I scaled docker using the same computer/resources. The performance improved when I scaled the model three times.
