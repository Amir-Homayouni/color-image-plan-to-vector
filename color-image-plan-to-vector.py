import rhinoscriptsyntax as rs

r = [[0 for i in range(y)] for j in range(x)]
g = [[0 for i in range(y)] for j in range(x)]
b = [[0 for i in range(y)] for j in range(x)]
col = [[-1 for i in range(y)] for j in range(x)]
for i in range(x):
    for j in range(y):
        r[i][j] = datar[j * x + i]
        g[i][j] = datag[j * x + i]
        b[i][j] = datab[j * x + i]

for i in range(x):
    for j in range(y):
        for k in range(cn):
            if abs(r[i][j]-cr[k])+abs(g[i][j]-cg[k])+abs(b[i][j]-cb[k]) <= col_tel:
                col[i][j] = k
c = -1
circles = []
for i in range(x):
    for j in range(y):
        if col[i][j] == c:
            circles.append(rs.AddCircle([i,j,0], 0.5))
xlines = [0]
ylines = [0]
temp = []
for i in range(x - 1):
    dif = 0
    for j in range(y):
        if col[i][j] != col[i + 1][j]:
            dif = dif + 1
    if dif > line_det_tel * y:
        if len(temp) == 0:
            temp.append(i)
        else:
            if temp[-1] == i - 1:
                temp.append(i)
            else:
                sum = 0
                for k in temp:
                    sum = sum + k
                ave = int(sum / len(temp))
                xlines.append(ave)
                temp = []
    else:
        if len(temp) > 0:
            if temp[-1] == i - 1:
                sum = 0
                for k in temp:
                    sum = sum + k
                ave = int(sum / len(temp))
                xlines.append(ave)
                temp = []
temp = []
for j in range(y - 1):
    dif = 0
    for i in range(x):
        if col[i][j] != col[i][j + 1]:
            dif = dif + 1
    if dif > line_det_tel * y:
        if len(temp) == 0:
            temp.append(j)
        else:
            if temp[-1] == j - 1:
                temp.append(j)
            else:
                sum = 0
                for k in temp:
                    sum = sum + k
                ave = int(sum / len(temp))
                ylines.append(ave)
                temp = []
    else:
        if len(temp) > 0:
            if temp[-1] == j - 1:
                sum = 0
                for k in temp:
                    sum = sum + k
                ave = int(sum / len(temp))
                ylines.append(ave)
                temp = []

lines = []
xlines.append(x - 1)
ylines.append(y - 1)
for i in xlines:
    lines.append(rs.AddLine([i + 0.5,0,0], [i + 0.5,y,0]))
for j in ylines:
    lines.append(rs.AddLine([0,j + 0.5,0], [x,j + 0.5,0]))

cc = [[-1 for i in range(len(ylines) - 1)] for j in range(len(xlines) - 1)]
sx = [[-1 for i in range(len(ylines) - 1)] for j in range(len(xlines) - 1)]
sy = [[-1 for i in range(len(ylines) - 1)] for j in range(len(xlines) - 1)]

for i in range(len(xlines) - 1):
    for j in range(len(ylines) - 1):
        x1 = xlines[i]
        x2 = xlines[i + 1]
        y1 = ylines[j]
        y2 = ylines[j + 1]
        sx[i][j] = x2 - x1
        sy[i][j] = y2 - y1
        counter = [0 for k in range(-1, cn)]
        for k in range(x1 + 1, x2):
            for l in range(y1 + 1, y2):
                counter[col[k][l]] = counter[col[k][l]] + 1
        max = 0
        for k in range(-1, cn):
            if counter[k] > max:
                max = counter[k]
                cc[i][j] = k
xn = len(xlines) - 1
yn = len(ylines) - 1
print cn, xn, yn
print cc
print sx
print sy
external = []
internal = []
for i in range(1, xn):
    x1 = xlines[i]
    for j in range(yn - 1):
        y1 = ylines[j]
        y2 = ylines[j + 1]
        if cc[i - 1][j] != cc[i][j]:
            if (cc[i - 1][j] == -1) or (cc[i][j] == -1):
                external.append(rs.AddLine([x1,y1,0],[x1,y2,0]))
            else:
                internal.append(rs.AddLine([x1,y1,0],[x1,y2,0]))
for j in range(1, yn):
    y1 = ylines[j]
    for i in range(xn - 1):
        x1 = xlines[i]
        x2 = xlines[i + 1]
        if cc[i][j - 1] != cc[i][j]:
            if (cc[i][j - 1] == -1) or (cc[i][j] == -1):
                external.append(rs.AddLine([x1,y1,0],[x2,y1,0]))
            else:
                internal.append(rs.AddLine([x1,y1,0],[x2,y1,0]))

rectangles = []
for k in range(cn):
    startx = xn
    starty = yn
    endx = 0
    endy = 0
    for i in range(xn):
        for j in range(yn):
            if cc[i][j] == k:
                if i < startx:
                    startx = i
                if i > endx:
                    endx = i
                if j < starty:
                    starty = j
                if j > endy:
                    endy = j
    lx = 0
    ly = 0
    sizex = 0
    sizey = 0
    for i in range(startx):
        lx = lx + sx[i][0]
    for j in range(starty):
        ly = ly + sy[0][j]
    for i in range(startx, endx + 1):
        sizex = sizex + sx[i][0]
    for j in range(starty, endy + 1):
        sizey = sizey + sy[0][j]
    pl = rs.PlaneFromNormal([lx, ly, 0], [0, 0, 1])
    rectangles.append(rs.AddRectangle(pl, sizex, sizey))
