import sys
import pygame
from pygame.locals import *
from perlin_noise import PerlinNoise
import time
import random
import math

pygame.init()

screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE, 32)
font = pygame.font.Font("fonts/Pixel.ttf", 35)
clock = pygame.time.Clock()
SCALE_FACTOR = 4
imgs = [
    pygame.transform.scale_by(pygame.image.load("images/w.png"), SCALE_FACTOR),
    pygame.transform.scale_by(pygame.image.load("images/barrier.png"), SCALE_FACTOR),
    pygame.transform.scale_by(pygame.image.load("images/barrier2.png"), SCALE_FACTOR),
]
red = pygame.surface.Surface((64, 64))
red.fill((255, 0, 0))
grassimgs = dict(
    g=pygame.transform.scale_by(pygame.image.load("images/g.png"), SCALE_FACTOR),
    gd=pygame.transform.scale_by(pygame.image.load("images/gd.png"), SCALE_FACTOR),
    gu=pygame.transform.scale_by(pygame.image.load("images/gu.png"), SCALE_FACTOR),
    gl=pygame.transform.scale_by(pygame.image.load("images/gl.png"), SCALE_FACTOR),
    gr=pygame.transform.scale_by(pygame.image.load("images/gr.png"), SCALE_FACTOR),
    gur=pygame.transform.scale_by(pygame.image.load("images/gur.png"), SCALE_FACTOR),
    gul=pygame.transform.scale_by(pygame.image.load("images/gul.png"), SCALE_FACTOR),
    gdr=pygame.transform.scale_by(pygame.image.load("images/gdr.png"), SCALE_FACTOR),
    gdl=pygame.transform.scale_by(pygame.image.load("images/gdl.png"), SCALE_FACTOR),
    dgul=pygame.transform.scale_by(pygame.image.load("images/dgul.png"), SCALE_FACTOR),
    dgur=pygame.transform.scale_by(pygame.image.load("images/dgur.png"), SCALE_FACTOR),
    dgdl=pygame.transform.scale_by(pygame.image.load("images/dgdl.png"), SCALE_FACTOR),
    dgdr=pygame.transform.scale_by(pygame.image.load("images/dgdr.png"), SCALE_FACTOR),
    gudl=pygame.transform.scale_by(pygame.image.load("images/gudl.png"), SCALE_FACTOR),
    gudr=pygame.transform.scale_by(pygame.image.load("images/gudr.png"), SCALE_FACTOR),
    gulr=pygame.transform.scale_by(pygame.image.load("images/gulr.png"), SCALE_FACTOR),
    gdlr=pygame.transform.scale_by(pygame.image.load("images/gdlr.png"), SCALE_FACTOR),
    t=red,
)
waterimgs = dict(
    t=red,
    w=pygame.transform.scale_by(pygame.image.load("images/w.png"), SCALE_FACTOR),
    wu=pygame.transform.scale_by(pygame.image.load("images/wu.png"), SCALE_FACTOR),
    wd=pygame.transform.scale_by(pygame.image.load("images/wd.png"), SCALE_FACTOR),
    wl=pygame.transform.scale_by(pygame.image.load("images/wl.png"), SCALE_FACTOR),
    wr=pygame.transform.scale_by(pygame.image.load("images/wr.png"), SCALE_FACTOR),
    wul=pygame.transform.scale_by(pygame.image.load("images/wul.png"), SCALE_FACTOR),
    wur=pygame.transform.scale_by(pygame.image.load("images/wur.png"), SCALE_FACTOR),
    wdl=pygame.transform.scale_by(pygame.image.load("images/wdl.png"), SCALE_FACTOR),
    wdr=pygame.transform.scale_by(pygame.image.load("images/wdr.png"), SCALE_FACTOR),
    wudl=pygame.transform.scale_by(pygame.image.load("images/wudl.png"), SCALE_FACTOR),
    wudr=pygame.transform.scale_by(pygame.image.load("images/wudr.png"), SCALE_FACTOR),
    wulr=pygame.transform.scale_by(pygame.image.load("images/wulr.png"), SCALE_FACTOR),
    wdlr=pygame.transform.scale_by(pygame.image.load("images/wdlr.png"), SCALE_FACTOR),
)
hbimgs = dict(
    hb1=pygame.transform.scale_by(pygame.image.load("images/hb1.png"), SCALE_FACTOR),
    hb2=pygame.transform.scale_by(pygame.image.load("images/hb2.png"), SCALE_FACTOR),
    hb3=pygame.transform.scale_by(pygame.image.load("images/hb3.png"), SCALE_FACTOR),
)
healthimgs = dict(
    h1=pygame.transform.scale_by(pygame.image.load("images/heart.png"), SCALE_FACTOR),
    h2=pygame.transform.scale_by(pygame.image.load("images/heart2.png"), SCALE_FACTOR),
    h3=pygame.transform.scale_by(pygame.image.load("images/heart3.png"), SCALE_FACTOR),
    fh1=pygame.transform.scale_by(pygame.image.load("images/fheart.png"), SCALE_FACTOR),
    fh2=pygame.transform.scale_by(
        pygame.image.load("images/fheart2.png"), SCALE_FACTOR
    ),
    fh3=pygame.transform.scale_by(
        pygame.image.load("images/fheart3.png"), SCALE_FACTOR
    ),
)
punch = pygame.mixer.Sound("sounds/punch.ogg")


class Tile:
    def __init__(self, x, y, img):
        self.x = x * 64
        self.y = y * 64
        self.img = img

    def draw(self):
        screen.blit(self.img, (self.x - offsetx, self.y + offsety))


class Barrier(Tile):
    def __init__(self, x, y):
        super().__init__(x, y, imgs[1])

    def draw(self):
        if time.time() % 0.75 < 0.375:
            self.img = imgs[1]
        else:
            self.img = imgs[2]
        screen.blit(self.img, (self.x - offsetx, self.y + offsety))


class Grass(Tile):
    def __init__(
        self, x, y, up, down, left, right, test, upleft, upright, downleft, downright
    ):
        super().__init__(x, y, grassimgs["g"])
        self.up = up
        self.right = right
        self.left = left
        self.down = down
        self.upleft = upleft
        self.upright = upright
        self.downleft = downleft
        self.downright = downright
        self.test = test
        if self.test:
            self.img = grassimgs["t"]

        elif self.up and self.right and self.left:
            self.img = grassimgs["gulr"]
        elif self.up and self.right and self.down:
            self.img = grassimgs["gudr"]
        elif self.up and self.left and self.down:
            self.img = grassimgs["gudl"]
        elif self.down and self.right and self.left:
            self.img = grassimgs["gdlr"]
        elif self.up and self.right:
            self.img = grassimgs["gur"]
        elif self.up and self.left:
            self.img = grassimgs["gul"]
        elif self.down and self.right:
            self.img = grassimgs["gdr"]
        elif self.down and self.left:
            self.img = grassimgs["gdl"]
        elif self.down:
            self.img = grassimgs["gd"]
        elif self.up:
            self.img = grassimgs["gu"]
        elif self.left:
            self.img = grassimgs["gl"]
        elif self.right:
            self.img = grassimgs["gr"]
        elif self.upright:
            self.img = grassimgs["dgur"]
        elif self.upleft:
            self.img = grassimgs["dgul"]
        elif self.downright:
            self.img = grassimgs["dgdr"]
        elif self.downleft:
            self.img = grassimgs["dgdl"]


class Water(Tile):
    def __init__(self, x, y, up, down, left, right, test):
        super().__init__(x, y, imgs[0])
        self.up = up
        self.right = right
        self.left = left
        self.down = down
        self.test = test

        if self.test:
            self.img = waterimgs["t"]
        elif self.up and self.right and self.left:
            self.img = waterimgs["wulr"]
        elif self.up and self.right and self.down:
            self.img = waterimgs["wudr"]
        elif self.up and self.left and self.down:
            self.img = waterimgs["wudl"]
        elif self.down and self.right and self.left:
            self.img = waterimgs["wdlr"]
        elif self.up and self.right:
            self.img = waterimgs["wur"]
        elif self.up and self.left:
            self.img = waterimgs["wul"]
        elif self.down and self.right:
            self.img = waterimgs["wdr"]
        elif self.down and self.left:
            self.img = waterimgs["wdl"]
        elif self.down:
            self.img = waterimgs["wd"]
        elif self.up:
            self.img = waterimgs["wu"]
        elif self.left:
            self.img = waterimgs["wl"]
        elif self.right:
            self.img = waterimgs["wr"]


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 1.5
        self.img = pygame.transform.scale_by(
            pygame.image.load("images/player.png"), SCALE_FACTOR
        )
        self.hunger = 100
        self.health = 100
        self.lhd = 0
        self.imgs = dict(
            down=pygame.transform.scale_by(
                pygame.image.load("images/player.png"), SCALE_FACTOR
            ),
            left=pygame.transform.scale_by(
                pygame.image.load("images/pl.png"), SCALE_FACTOR
            ),
            right=pygame.transform.scale_by(
                pygame.image.load("images/pr.png"), SCALE_FACTOR
            ),
            down1=pygame.transform.scale_by(
                pygame.image.load("images/pd1.png"), SCALE_FACTOR
            ),
            down2=pygame.transform.scale_by(
                pygame.image.load("images/pd2.png"), SCALE_FACTOR
            ),
            pl1=pygame.transform.scale_by(
                pygame.image.load("images/pl1.png"), SCALE_FACTOR
            ),
            pr1=pygame.transform.scale_by(
                pygame.image.load("images/pr1.png"), SCALE_FACTOR
            ),
            up=pygame.transform.scale_by(
                pygame.image.load("images/pu.png"), SCALE_FACTOR
            ),
            u1=pygame.transform.scale_by(
                pygame.image.load("images/pu1.png"), SCALE_FACTOR
            ),
            u2=pygame.transform.scale_by(
                pygame.image.load("images/pu2.png"), SCALE_FACTOR
            ),
        )
        self.dir = "down"
        self.moving = False
        self.ldt = 0
        self.dead = False
        self.username = "( USERNAME )"
        self.deathmessage = ""
        self.deathtypes = {
            "hunger": "{} starved to death".format(self.username),
            "normal": "{} died".format(self.username),
        }

    def draw(self):
        if self.hunger <= 0:
            self.hunger = 0
            if self.lhd < time.time():
                self.damage(5, "hunger")
                self.lhd = time.time() + 1
        if self.dir == "down" and not self.moving:
            self.img = self.imgs["down"]
        elif self.dir == "down" and self.moving:
            if time.time() % 0.4 < 0.2:
                self.img = self.imgs["down1"]
            else:
                self.img = self.imgs["down2"]
        elif self.dir == "left" and not self.moving:
            self.img = self.imgs["left"]
        elif self.dir == "left" and self.moving:
            if time.time() % 0.4 < 0.2:
                self.img = self.imgs["left"]
            else:
                self.img = self.imgs["pl1"]
        elif self.dir == "right" and not self.moving:
            self.img = self.imgs["right"]
        elif self.dir == "right" and self.moving:
            if time.time() % 0.4 < 0.2:
                self.img = self.imgs["right"]
            else:
                self.img = self.imgs["pr1"]
        elif self.dir == "up" and not self.moving:
            self.img = self.imgs["up"]
        elif self.dir == "up" and self.moving:
            if time.time() % 0.4 < 0.2:
                self.img = self.imgs["u1"]
            else:
                self.img = self.imgs["u2"]
        screen.blit(
            self.img,
            (
                screen.get_width() / 2 - self.img.get_width() / 2,
                screen.get_height() / 2 - self.img.get_height() / 2,
            ),
        )
        displayhunger = self.hunger - 5
        if displayhunger > 15:
            for i in range(10):
                if displayhunger > i * 10:
                    screen.blit(hbimgs["hb1"], (i * 32, 0))
                elif displayhunger > (i - 1 * 10) + 5 and displayhunger > (i * 10) - 5:
                    screen.blit(hbimgs["hb3"], (i * 32, 0))
                else:
                    screen.blit(hbimgs["hb2"], (i * 32, 0))
        else:
            for i in range(10):
                offset = math.sin(time.time() * 25 + i * 10) * 5
                if displayhunger > i * 10:
                    screen.blit(hbimgs["hb1"], (i * 32, offset))
                elif displayhunger > (i - 1 * 10) + 5 and displayhunger > (i * 10) - 5:
                    screen.blit(hbimgs["hb3"], (i * 32, offset))
                else:
                    screen.blit(hbimgs["hb2"], (i * 32, offset))
        displayhealth = self.health - 5
        if self.health <= 20:
            if self.ldt < time.time() and not self.dead:
                for i in range(10):
                    offset = math.sin(time.time() * 25 + i * 10) * 5
                    if displayhealth > (i * 10):
                        screen.blit(
                            healthimgs["h1"],
                            (i * 32 + screen.get_width() - 325, offset),
                        )
                    elif (
                        displayhealth > (i - 1 * 10) + 5
                        and displayhealth > (i * 10) - 5
                    ):
                        screen.blit(
                            healthimgs["h2"],
                            (i * 32 + screen.get_width() - 325, offset),
                        )
                    else:
                        screen.blit(
                            healthimgs["h3"],
                            (i * 32 + screen.get_width() - 325, offset),
                        )
            else:
                for i in range(10):
                    offset = math.sin(time.time() * 25 + i * 10) * 5
                    if displayhealth > (i * 10):
                        screen.blit(
                            healthimgs["fh1"],
                            (i * 32 + screen.get_width() - 325, offset),
                        )
                    elif (
                        displayhealth > (i - 1 * 10) + 5
                        and displayhealth > (i * 10) - 5
                    ):
                        screen.blit(
                            healthimgs["fh2"],
                            (i * 32 + screen.get_width() - 325, offset),
                        )
                    else:
                        screen.blit(
                            healthimgs["fh3"],
                            (i * 32 + screen.get_width() - 325, offset),
                        )
        else:
            if self.ldt < time.time() and not self.dead:
                for i in range(10):
                    if displayhealth > (i * 10):
                        screen.blit(
                            healthimgs["h1"], (i * 32 + screen.get_width() - 325, 0)
                        )
                    elif (
                        displayhealth > (i - 1 * 10) + 5
                        and displayhealth > (i * 10) - 5
                    ):
                        screen.blit(
                            healthimgs["h2"], (i * 32 + screen.get_width() - 325, 0)
                        )
                    else:
                        screen.blit(
                            healthimgs["h3"], (i * 32 + screen.get_width() - 325, 0)
                        )
            else:
                for i in range(10):
                    if displayhealth > (i * 10):
                        screen.blit(
                            healthimgs["fh1"], (i * 32 + screen.get_width() - 325, 0)
                        )
                    elif (
                        displayhealth > (i - 1 * 10) + 5
                        and displayhealth > (i * 10) - 5
                    ):
                        screen.blit(
                            healthimgs["fh2"], (i * 32 + screen.get_width() - 325, 0)
                        )
                    else:
                        screen.blit(
                            healthimgs["fh3"], (i * 32 + screen.get_width() - 325, 0)
                        )

    def damage(self, amount, damagetype="normal"):
        if self.health > 0:
            punch.play()
            self.health -= amount
            self.ldt = time.time() + 0.2
            self.deathmessage = self.deathtypes[damagetype]

    def move(self):
        if self.health <= 0:
            self.dead = True
            self.hunger = 0
            self.moving = False
            self.dir = ""
            self.img = pygame.transform.scale_by(
                pygame.image.load("images/pd.png"), SCALE_FACTOR
            )
        if not self.dead:
            if keys[K_k]:
                self.damage(100)
            if keys[K_LSHIFT] and self.hunger > 0:
                if self.moving:
                    self.hunger -= 0.05
                if self.speed < 5:
                    self.speed += 0.1

            else:
                if self.speed > 2.5:
                    self.speed -= 0.1
                elif self.speed < 2.3:
                    self.speed += 0.1
            self.moving = False
            if self.ldt > time.time():
                self.speed = 1.25
            if keys[pygame.K_w]:
                if keys[K_a] or keys[K_d]:
                    self.y += 1.5 * self.speed
                else:
                    self.y += 3 * self.speed
                self.moving = True
                self.dir = "up"
            if keys[pygame.K_s]:
                self.dir = "down"
                if keys[K_a] or keys[K_d]:
                    self.y -= 1.5 * self.speed
                else:
                    self.y -= 3 * self.speed
                self.moving = True
            if keys[pygame.K_a]:
                self.dir = "left"
                if keys[K_w] or keys[K_s]:
                    self.x -= 1.5 * self.speed
                else:
                    self.x -= 3 * self.speed
                self.moving = True
            if keys[pygame.K_d]:
                self.dir = "right"
                if keys[K_w] or keys[K_s]:
                    self.x += 1.5 * self.speed
                else:
                    self.x += 3 * self.speed
                self.moving = True

    def respawn(self):
        self.health = 100
        self.hunger = 100
        self.dead = False
        self.moving = False
        self.dir = "down"
        self.x = 0
        self.y = 0
        self.ldt = time.time()
        self.deathmessage = ""


class Button:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = font.render(text, False, (255, 255, 255))
        self.rect = pygame.Rect(
            self.x - self.text.get_width() / 2 + 5,
            self.y - self.text.get_height() / 2 + 5,
            self.text.get_width() + 15,
            self.text.get_height() + 15,
        )
        self.active = True
        self.pressed = False

    def draw(self):
        self.pressed = False
        if self.active:
            if (
                self.rect.collidepoint(pygame.mouse.get_pos())
                and pygame.mouse.get_pressed()[0]
            ):
                self.pressed = True
                pygame.draw.rect(screen, (140, 140, 220), self.rect)
            elif self.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (120, 120, 120), self.rect)
            else:
                pygame.draw.rect(screen, (80, 80, 80), self.rect)
            screen.blit(
                self.text,
                (
                    self.x - self.text.get_width() / 2 + 5,
                    self.y - self.text.get_height() / 2 + 5,
                ),
            )

    def setpos(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(
            self.x - self.text.get_width() / 2,
            self.y - self.text.get_height() / 2,
            self.text.get_width(),
            self.text.get_height(),
        )


tilemap = []
tiles = []
noise = PerlinNoise(octaves=1, seed=random.randint(-1125899906842624, 1125899906842624))
player = Player()
for i in range(100):
    tilemap.append([])
    for j in range(100):
        if noise((i / 10, j / 10)) > -0.1:
            tilemap[i].append("Grass")
        else:
            tilemap[i].append("Water")
for i in range(len(tilemap[0])):
    tilemap[0][i] = "Grass"
for i in range(len(tilemap[99])):
    tilemap[99][i] = "Grass"
for i in range(len(tilemap)):
    tilemap[i][0] = "Grass"
    tilemap[i][99] = "Grass"
for i in range(99):
    for j in range(99):
        if tilemap[i][j] == "Grass":
            sides = [False, False, False, False, False, False, False, False, False]
            ntw = False
            if tilemap[i][j + 1] == "Water":
                sides[1] = True
                ntw = True
            if tilemap[i - 1][j] == "Water":
                sides[2] = True
                ntw = True
            if tilemap[i + 1][j] == "Water":
                sides[3] = True
                ntw = True
            if tilemap[i][j - 1] == "Water":
                sides[0] = True
                ntw = True
            if tilemap[i + 1][j + 1] == "Water" and not ntw:
                sides[8] = True
            if tilemap[i - 1][j + 1] == "Water" and not ntw:
                sides[7] = True
            if tilemap[i + 1][j - 1] == "Water" and not ntw:
                sides[6] = True
            if tilemap[i - 1][j - 1] == "Water" and not ntw:
                sides[5] = True
            tilemap[i][j] = Grass(i, j, *sides)
for i in range(99):
    for j in range(99):
        if tilemap[i][j] == "Water":
            sides = [False, False, False, False, False]
            ntw = False
            if type(tilemap[i][j + 1]) == Grass:
                sides[1] = True
                ntw = True
            if type(tilemap[i - 1][j]) == Grass:
                sides[2] = True
                ntw = True
            if type(tilemap[i + 1][j]) == Grass:
                sides[3] = True
                ntw = True
            if type(tilemap[i][j - 1]) == Grass:
                sides[0] = True
                ntw = True
            tilemap[i][j] = Water(i, j, *sides)
for i in range(100):
    for j in range(100):
        if tilemap[i][j] == "Water":
            tilemap[i][j] = Tile(i, j, imgs[0])
        if tilemap[i][j] == "Grass":
            tilemap[i][j] = Tile(i, j, imgs[0])
for i in range(len(tilemap[0])):
    tilemap[0][i] = Barrier(tilemap[0][i].x / 64, tilemap[0][i].y / 64)
for i in range(len(tilemap[99])):
    tilemap[99][i] = Barrier(tilemap[99][i].x / 64, tilemap[99][i].y / 64)
for i in range(len(tilemap)):
    tilemap[i][0] = Barrier(tilemap[i][0].x / 64, tilemap[i][0].y / 64)
    tilemap[i][99] = Barrier(tilemap[i][99].x / 64, tilemap[i][99].y / 64)
for i in tilemap:
    for j in i:
        tiles.append(j)

offsetx = 0
offsety = 0
menu = "Start"
quitb = Button(screen.get_width() / 2 - 75, screen.get_height() / 2 - 75, "Quit")
rsb = Button(screen.get_width() / 2 - 75, screen.get_height() / 2 + 75, "Restart")
quitb.active = False
while True:
    screen.fill((0, 0, 25))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_q]:
        pygame.quit()
        sys.exit()
    for tile in tiles:
        tile.draw()
    player.draw()
    player.move()
    offsetx = int(player.x) - screen.get_width() / 2
    offsety = int(player.y) + screen.get_height() / 2
    if player.dead:
        quitb.active = True
        rsb.active = True
        deadsurf = pygame.Surface(
            (screen.get_width(), screen.get_height())
        ).convert_alpha()
        deadsurf.fill((255, 0, 0, 100))
        screen.blit(deadsurf, (0, 0))
        txt = font.render(player.deathmessage, False, (255, 255, 255))
        screen.blit(
            txt,
            (
                screen.get_width() / 2 - txt.get_width() / 2,
                screen.get_height() / 2 - 100,
            ),
        )
        quitb.setpos(screen.get_width() / 2, screen.get_height() / 2 + 100)
        quitb.draw()
        rsb.setpos(screen.get_width() / 2, screen.get_height() / 2 + 150)
        rsb.draw()
        if quitb.pressed:
            pygame.quit()
            sys.exit()
        if rsb.pressed:
            player.respawn()
    clock.tick(60)

    pygame.display.flip()
