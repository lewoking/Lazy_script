import pyautogui as pg

pg.FAILSAFE = True
# pg.PAUSE = 0.5

width, height = pg.size()

x, y = pg.position()

# or 以图定位
# p = pg.locateOnScreen('find.png')
# x,y= pg.center(find)

f = pg.locateOnScreen('findp.png')
px, py = pg.center(f)

pg.click(x, y)

pg.click(px, py)

pg.click(px, py + 202)

try:
    pg.locateOnScreen('sucess.png')
except expression as identifier:

    pass
else:
    pg.typewrite(['enter'])

pg.click(x, y + 18)
pg.click(x, y + 18)


pg.click(px, py + 47)

pg.click(px, py + 202)

try:
    pg.locateOnScreen('sucess.png')
except expression as identifier:
    pass
else:
    pg.typewrite(['enter'])

pg.click(x, y + 47)
pg.click(x, y + 47)


pg.click(px, py + 85)

pg.click(px, py + 202)

try:
    pg.locateOnScreen('sucess.png')
except expression as identifier:
    pass
else:
    pg.typewrite(['enter'])
