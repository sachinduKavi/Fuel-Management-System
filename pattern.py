row_count = 1
count = 1
for i in range(3, 0, -1):
    star = ''
    for s in range(i, 0, -1):
        star += ' '
    var = ''
    for t in range(row_count):
        var += str(count)
        count += 1
    row_count += 2
    print(star + var)
