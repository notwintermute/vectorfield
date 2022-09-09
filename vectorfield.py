import math
import pygame
import numpy as np

sqSide = 20
noSq = 25

sqRes = noSq * sqSide
resX = sqRes
resY = sqRes
tp = [resX/2, resY/2]
triang = 0
n = noSq


ballList = []
class Ball:
    def __init__(self, xp, yp, xv, yv):
        self.xp = xp
        self.yp = yp
        self.xv = xv
        self.yv = yv


def norm(x, y):
    if x == 0 and y == 0:
        return 1
    return math.sqrt(x**2+y**2)


def findAng(inp):
    nm = norm(inp[0],inp[1])
    m = 1
    if inp[1] < 0:
        m = -1
    return math.acos(inp[0]/nm)*m


def texp(x,a,b):
    return math.exp(-b*(x-a)**2)


def colcur(x):
    p = 0.6
    s = 0.6
    w = 8
    B = 80
    blue = int(texp(x, p, w)*(255-B)+B)
    green = int(texp(x, p+s, w)*(255-B)+B)
    red = int(texp(x, p+2*s, w)*(255-B)+B)
    return red, blue, green


def diffFun(x,y):
    dx = -y-x
    dy = x-y
    nrm = norm(dx, dy)
    return dx/nrm, dy/nrm


def rot(inp, ang, piv):
    s = [inp[0]-piv[0], inp[1]-piv[1]]
    rx = math.cos(ang)*s[0]-math.sin(ang)*s[1]
    ry = math.cos(ang)*s[1]+math.sin(ang)*s[0]
    rx += piv[0]
    ry += piv[1]
    return rx, ry


def stc(inp):
    sx = inp[0]-resX/2
    sy = -(inp[1]-resY/2)
    return sx, sy


def cts(inp):
    sx = inp[0]+resX/2
    sy = (resY/2)-inp[1]
    return sx, sy

grid = []
for x in range(n):
    grid.append([])
    for y in range(n):
        grid[x].append(diffFun(x-(n-1)/2,(n-1)/2-y))

pygame.init()
# initialize surface and start the main loop
surface = pygame.display.set_mode((resX, resY))
pygame.display.set_caption('vectorfield')
running = True
# --------------------------------------- Main Loop ---------------------------------------
while running:
    mouse = pygame.mouse.get_pos()  # puts the mouse position into a 2d tuple
    mouseSq = [math.floor(mouse[0]/sqSide), math.floor(mouse[1]/sqSide)]
    # ------------------------------------- input handling -------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        # ------------------------------------ mouse click actions ------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            ballList.append(Ball(mouse[0], mouse[1], 0, 0))
            print(grid[mouseSq[0]][mouseSq[1]])
        if event.type == pygame.MOUSEBUTTONUP:  # releasing the hold
            pass
        # ------------------------------------ key press actions ------------------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                tp[1] -= 1
            if event.key == pygame.K_s:
                tp[1] += 1
            if event.key == pygame.K_a:
                tp[0] -= 1
            if event.key == pygame.K_d:
                tp[0] += 1
            if event.key == pygame.K_q:
                triang += 2*math.pi/36
            if event.key == pygame.K_e:
                triang -= 2*math.pi/36

    # ---------------------------------------- Updating Parameters ----------------------------------------

    # ---------------------------------------- Rendering ----------------------------------------
    surface.fill((0,0,0))
    pygame.draw.line(surface, (255, 255, 255), (resX/2, 0), (resX/2,resY))
    pygame.draw.line(surface, (255, 255, 255), (0, resY / 2), (resX, resY/2))
    for i, ball in enumerate(ballList):
        try:
            sp = [math.floor(ball.xp / sqSide), math.floor(ball.yp / sqSide)]
            ball.xv = grid[sp[0]][sp[1]][0]
            ball.yv = grid[sp[0]][sp[1]][1]
            ball.xp += ball.xv
            ball.yp -= ball.yv
            pygame.draw.circle(surface, (255, 255, 255), (ball.xp, ball.yp), 2)
        except IndexError:
            ballList.pop(i)

    s = sqSide/2.5
    ang = math.pi/3
    for i in range(noSq):
        for j in range(noSq):
            p = grid[i][j]
            a = findAng(p)+3*math.pi/2
            tx, ty = stc([i*sqSide+(sqSide/2), j*sqSide+(sqSide/2)])
            triP = ([tx-s/4, ty-s/(2*math.sqrt(3))], [tx + s/4, ty-s/(2*math.sqrt(3))], [tx, ty + s/math.sqrt(3)])
            tripoints = []
            for x in triP:
                tripoints.append((cts(rot(x, a, [tx, ty]))))
            pygame.draw.polygon(surface, (colcur(1.8 * a/(2*math.pi))), tripoints, 1)

    pygame.display.flip()
