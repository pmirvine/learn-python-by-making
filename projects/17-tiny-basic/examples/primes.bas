10 REM The primes below a limit, by trial division
20 LIMIT = 20000
30 COUNT = 0
40 FOR N = 2 TO LIMIT
50   D = 2
60   PRIME = -1
70   REPEAT
80     IF N MOD D = 0 AND D < N THEN PRIME = 0
90     D = D + 1
100   UNTIL D * D > N OR PRIME = 0
110   IF PRIME THEN COUNT = COUNT + 1
120 NEXT N
130 PRINT COUNT; " primes below "; LIMIT
