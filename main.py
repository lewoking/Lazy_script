import pyautogui as pg
import time

pg.FAILSAFE = True
# pg.PAUSE = 0.5

width, height = pg.size()

x, y = pg.position()  # 手动定位点

# or 以图定位
# p = pg.locateOnScreen('find.png')
# x,y= pg.center(find)

f = pg.locateOnScreen('yes.png')
px, py = pg.center(f)  # 自动定位点

pg.click(x, y)

pg.click(px, py + 60)

pg.click(px, py + 230)

try:
    time.sleep(1)  # 等待提示框弹出时间
#  pg.locateOnScreen('sucess.png')  # 自动识别成功提示框
except expression as identifier:

    pass
else:
    pg.typewrite(['enter'])

pg.click(x, y + 30)
pg.click(x, y + 30)

pg.click(px, py + 100)

pg.click(px, py + 230)

try:
    time.sleep(1)
#    pg.locateOnScreen('sucess.png')
except expression as identifier:
    pass
else:
    pg.typewrite(['enter'])

pg.click(x, y + 60)
pg.click(x, y + 60)

pg.click(px, py + 140)

pg.click(px, py + 230)

try:
    time.sleep(1)
#    pg.locateOnScreen('sucess.png')
except expression as identifier:
    pass
else:
    pg.typewrite(['enter'])
