SHADES = " .:-=+*#%@"

for row in range(-12, 13):
    line = ""
    for column in range(-39, 40):
        c = complex(column / 26 - 0.5, row / 10)
        z = 0j
        count = 0
        while abs(z) <= 2 and count < 27:
            z = z * z + c
            count += 1
        line += SHADES[count // 3]
    print(line)
