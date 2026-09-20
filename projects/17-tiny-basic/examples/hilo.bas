10 REM Hi-Lo
20 SECRET = RND(100)
30 TRIES = 0
40 PRINT "I'm thinking of a number from 1 to 100."
50 REPEAT
60   INPUT "Your guess? ", GUESS
70   TRIES = TRIES + 1
80   IF GUESS < SECRET THEN PRINT "Too low."
90   IF GUESS > SECRET THEN PRINT "Too high."
100 UNTIL GUESS = SECRET
110 PRINT "Got it, in "; TRIES; " tries."
