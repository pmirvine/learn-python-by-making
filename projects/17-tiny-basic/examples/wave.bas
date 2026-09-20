10 REM A wave, down the screen
20 FOR A = 0 TO 12.6 STEP 0.3
30   PRINT STRING$(INT(20 + 18 * SIN(A)), " "); "*"
40 NEXT
