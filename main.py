import math
import random
import sys
import time

import pygame
from perlin_noise import PerlinNoise
from pygame.locals import *

grass_offset_x = 0
grass_offset_y = 0

pygame.init()
DEBUG = False
screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE, 32)
font = pygame.font.Font("fonts/Pixel.ttf", 35)
fontbig = pygame.font.Font("fonts/Pixel.ttf", 50)
fontsmall = pygame.font.Font("fonts/Pixel.ttf", 20)
clock = pygame.time.Clock()
onsound = pygame.mixer.Sound("sounds/on.wav")
offsound = pygame.mixer.Sound("sounds/off.wav")
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
purpimgs = dict(
    rest=pygame.transform.scale_by(
        pygame.image.load("images/purpguyrest.png"), SCALE_FACTOR
    ),
    d1=pygame.transform.scale_by(pygame.image.load("images/pgd1.png"), SCALE_FACTOR),
    d2=pygame.transform.scale_by(pygame.image.load("images/pgd2.png"), SCALE_FACTOR),
)
punch = pygame.mixer.Sound("sounds/punch.ogg")
punch.set_volume(0.4)
keybinds = {
    "up": K_w,
    "down": K_s,
    "left": K_a,
    "right": K_d,
    "sprint": K_LSHIFT,
    "kill": K_k,
    "pause": K_ESCAPE,
}


class Tile:
    """ """
    def __init__(self, x, y, img):
        self.x = x * 64
        self.y = y * 64
        self.img = img

    def draw(self):
        """ """
        if (
            -64 < self.x - offsetx < screen.get_width()
            and -64 < self.y + offsety < screen.get_height()
        ):
            screen.blit(self.img, (self.x - offsetx, self.y + offsety))


class Barrier(Tile):
    """ """
    def __init__(self, x, y):
        super().__init__(x, y, imgs[1])


class Grass(Tile):
    """ """
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
    """ """
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
    """ """
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
        self.username = "Filler Username"
        self.deathmessage = ""
        self.deathtypes = {
            "hunger": "{} starved to death",
            "normal": "{} died",
            "slain": "{} was slain by {}",
        }
        self.dx = 0
        self.dy = 0
        self.rect = pygame.Rect(
            self.x - self.img.get_width() * 2,
            self.y - self.img.get_height() * 2,
            self.img.get_width() * 4,
            self.img.get_height() * 4,
        )

    def draw(self):
        """ """
        if DEBUG:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                self.rect,
            )
        self.rect = pygame.Rect(
            self.x - self.img.get_width() / 2,
            self.y + self.img.get_height() / 2,
            self.img.get_width(),
            self.img.get_height(),
        )
        if self.hunger <= 0:
            self.hunger = 0
            if self.lhd < time.time():
                self.damage(5, "hunger")
                self.lhd = time.time() + 1
        if self.dir == "down" and not self.moving:
            self.img = self.imgs["down"]
        elif self.dir == "down" and self.moving:
            if time.time() % 0.4 < 0.2 and not game_paused:
                self.img = self.imgs["down1"]
            else:
                self.img = self.imgs["down2"]
        elif self.dir == "left" and not self.moving:
            self.img = self.imgs["left"]
        elif self.dir == "left" and self.moving:
            if time.time() % 0.4 < 0.2 and not game_paused:
                self.img = self.imgs["left"]
            else:
                self.img = self.imgs["pl1"]
        elif self.dir == "right" and not self.moving:
            self.img = self.imgs["right"]
        elif self.dir == "right" and self.moving:
            if time.time() % 0.4 < 0.2 and not game_paused:
                self.img = self.imgs["right"]
            else:
                self.img = self.imgs["pr1"]
        elif self.dir == "up" and not self.moving:
            self.img = self.imgs["up"]
        elif self.dir == "up" and self.moving:
            if time.time() % 0.4 < 0.2 and not game_paused:
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

    def damage(self, amount, damagetype="normal", secondary=""):
        """

        :param amount:
        :param damagetype:  (Default value = "normal")
        :param secondary:  (Default value = "")

        """
        if self.health > 0 and self.ldt < time.time() and not game_paused:
            punch.play()
            self.health -= amount
            self.ldt = time.time() + 0.4
            self.deathmessage = self.deathtypes[damagetype].format(
                self.username, secondary
            )
            return True
        else:
            return False

    def move(self):
        """ """
        if not game_paused:
            self.x += self.dx
            self.y += self.dy
        if self.dx > 0:
            self.dx -= dt_adjusted(1)
        elif self.dx < 0:
            self.dx += dt_adjusted(1)
        if self.dy > 0:
            self.dy -= dt_adjusted(1)
        elif self.dy < 0:
            self.dy += dt_adjusted(1)
        if 1 > self.dx > -1:
            self.dx = 0
        if 1 > self.dy > -1:
            self.dy = 0
        if self.health <= 0:
            self.dead = True
            self.hunger = 0
            self.moving = False
            self.dir = ""
            self.img = pygame.transform.scale_by(
                pygame.image.load("images/pd.png"), SCALE_FACTOR
            )
        if self.x < 0:
            self.x = 0
        if self.y > 0:
            self.y = 0
        if not self.dead and not game_paused:
            if keys[keybinds["kill"]]:
                self.damage(100)
            if keys[keybinds["sprint"]] and self.hunger > 0:
                if self.moving:
                    self.hunger -= dt_adjusted(0.1)
                if self.speed < 3.5:
                    self.speed += 0.1
            else:
                if self.speed > 2:
                    self.speed -= 0.1
                elif self.speed < 1.8:
                    self.speed += 0.1
            self.moving = False
            if self.ldt > time.time():
                self.speed = 1.25
            if keys[keybinds["up"]]:
                if keys[keybinds["left"]] or keys[keybinds["right"]]:
                    self.y += dt_adjusted(1.5) * self.speed
                else:
                    self.y += dt_adjusted(3) * self.speed
                self.moving = True
                self.dir = "up"
            if keys[keybinds["down"]]:
                self.dir = "down"
                if keys[keybinds["left"]] or keys[keybinds["right"]]:
                    self.y -= dt_adjusted(1.5) * self.speed
                else:
                    self.y -= dt_adjusted(3) * self.speed
                self.moving = True
            if keys[keybinds["left"]]:
                self.dir = "left"
                if keys[keybinds["up"]] or keys[keybinds["down"]]:
                    self.x -= dt_adjusted(1.5) * self.speed
                else:
                    self.x -= dt_adjusted(3) * self.speed
                self.moving = True
            if keys[keybinds["right"]]:
                self.dir = "right"
                if keys[keybinds["up"]] or keys[keybinds["down"]]:
                    self.x += dt_adjusted(1.5) * self.speed
                else:
                    self.x += dt_adjusted(3) * self.speed
                self.moving = True

    def respawn(self):
        """ """
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
    """ """
    def __init__(self, x, y, text, margins=10):
        self.x = x
        self.y = y
        self.text = font.render(text, False, (255, 255, 255))
        self.margins = margins
        self.rect = pygame.FRect(
            self.x - self.text.get_width() / 2 - self.margins / 2,
            self.y - self.text.get_height() / 2 - self.margins / 2,
            self.text.get_width() + self.margins,
            self.text.get_height() + self.margins,
        )
        self.surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.active = True
        self.pressed = False
        self.activated = False

    def draw(self):
        """ """
        if (
            not self.pressed
            and self.rect.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
            and self.active
            and not self.activated
        ):
            onsound.play()
        if self.pressed and (
            not pygame.mouse.get_pressed()[0]
            or not self.rect.collidepoint(pygame.mouse.get_pos())
        ):
            offsound.play()
            self.pressed = False
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.activated = True
        elif self.activated:
            self.activated = False
        if self.active:
            if (
                self.rect.collidepoint(pygame.mouse.get_pos())
                and pygame.mouse.get_pressed()[0]
            ):
                self.pressed = True
                pygame.draw.rect(
                    self.surf,
                    (255, 255, 255, 200),
                    (0, 0, self.rect.width, self.rect.height),
                )
            elif self.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(
                    self.surf,
                    (255, 255, 255, 100),
                    (0, 0, self.rect.width, self.rect.height),
                )
            else:
                pygame.draw.rect(
                    self.surf,
                    (255, 255, 255, 0),
                    (0, 0, self.rect.width, self.rect.height),
                )
            self.surf.blit(
                self.text,
                (
                    self.rect.width / 2 - self.text.get_width() / 2,
                    self.rect.height / 2 - self.text.get_height() / 2,
                ),
            )
            screen.blit(self.surf, (self.rect.x, self.rect.y))

    def setpos(self, x, y):
        """

        :param x:
        :param y:

        """
        self.x = x
        self.y = y
        self.rect = pygame.Rect(
            self.x - self.text.get_width() / 2 - self.margins / 2,
            self.y - self.text.get_height() / 2 - self.margins / 2,
            self.text.get_width() + self.margins,
            self.text.get_height() + self.margins,
        )

    def update_rect(self):
        """ """
        self.rect = pygame.FRect(
            self.x - self.text.get_width() / 2 - self.margins / 2,
            self.y - self.text.get_height() / 2 - self.margins / 2,
            self.text.get_width() + self.margins,
            self.text.get_height() + self.margins,
        )
        self.surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)


class Enemy:
    """ """
    def __init__(self, imgs, x, y):
        self.imgs = imgs
        self.img = self.imgs["rest"]
        self.x = x
        self.y = y
        self.rect = pygame.Rect(
            self.x + self.img.get_width() / 2,
            self.y + self.img.get_height() / 2,
            self.img.get_width(),
            self.img.get_height(),
        )
        self.resting = True
        self.discoverdead = False

    def draw(self):
        """ """
        distance = math.dist((self.x, self.y), (player.x, player.y))
        if (
            -64 < self.x - offsetx < screen.get_width()
            and -64 < self.y + offsety < screen.get_height()
        ):
            if self.resting:
                img = self.imgs["rest"]
            elif time.time() % 0.4 < 0.2:
                img = self.imgs["d1"]
            else:
                img = self.imgs["d2"]
            screen.blit(
                img,
                (
                    self.x - offsetx - self.img.get_width() / 2,
                    self.y + offsety - self.img.get_height() / 2,
                ),
            )
            if DEBUG:
                screen.blit(
                    font.render(
                        str(round(distance)),
                        False,
                        (255, 255, 255),
                    ),
                    (
                        self.x - offsetx - self.img.get_width() / 2,
                        self.y + offsety - self.img.get_height() / 2,
                    ),
                )
        if DEBUG:
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                self.rect,
            )

    def update_rect(self):
        """ """
        self.rect = pygame.Rect(
            self.x - self.img.get_width() / 2,
            -(self.y - self.img.get_height() / 2),
            self.img.get_width(),
            self.img.get_height(),
        )

    def move(self):
        """ """
        x = round(self.x)
        y = round(self.y)
        if not player.dead:
            self.discoverdead = False
        distance = math.dist((self.x, self.y), (player.x, player.y))
        if distance < 400:
            if not self.discoverdead:
                if self.x < round(player.x) and abs(self.x - player.x) > 1:
                    for _ in range(3):
                        self.x += dt_adjusted(1)
                        self.rect = pygame.Rect(
                            self.x - self.img.get_width() / 2,
                            -(self.y - self.img.get_height() / 2),
                            self.img.get_width(),
                            self.img.get_height(),
                        )
                        for enemy in enemys:
                            if enemy != self and self.rect.colliderect(enemy.rect):
                                self.x -= dt_adjusted(0.5)
                                enemy.x += dt_adjusted(0.5)
                                break
                        if self.x > round(player.x):
                            break
                elif self.x > round(player.x) and abs(self.x - player.x) > 1:
                    for _ in range(3):
                        self.x -= dt_adjusted(1)
                        self.rect = pygame.Rect(
                            self.x - self.img.get_width() / 2,
                            -(self.y - self.img.get_height() / 2),
                            self.img.get_width(),
                            self.img.get_height(),
                        )
                        for enemy in enemys:
                            if enemy != self and self.rect.colliderect(enemy.rect):
                                self.x += dt_adjusted(0.5)
                                enemy.x -= dt_adjusted(0.5)
                                break
                        if self.x < round(player.x):
                            break
                if -self.y < round(player.y) and abs(-self.y - player.y) > 1:
                    for _ in range(3):
                        self.y -= dt_adjusted(1)
                        self.rect = pygame.Rect(
                            self.x - self.img.get_width() / 2,
                            -(self.y - self.img.get_height() / 2),
                            self.img.get_width(),
                            self.img.get_height(),
                        )
                        for enemy in enemys:
                            if enemy != self and self.rect.colliderect(enemy.rect):
                                self.y += dt_adjusted(0.5)
                                enemy.y -= dt_adjusted(0.5)
                                break
                        if -self.y < round(player.y):
                            break
                elif -self.y > round(player.y) and abs(-self.y - player.y) > 1:
                    for _ in range(3):
                        self.y += dt_adjusted(1)
                        self.rect = pygame.Rect(
                            self.x - self.img.get_width() / 2,
                            -(self.y - self.img.get_height() / 2),
                            self.img.get_width(),
                            self.img.get_height(),
                        )
                        for enemy in enemys:
                            if enemy != self and self.rect.colliderect(enemy.rect):
                                self.y -= dt_adjusted(0.5)
                                enemy.y += dt_adjusted(0.5)
                                break
                        if -self.y > round(player.y):
                            break
            else:
                if self.x < round(player.x) and abs(self.x - player.x) > 1:
                    for _ in range(3):
                        self.x -= dt_adjusted(1)
                        self.rect = pygame.Rect(
                            self.x - self.img.get_width() / 2,
                            -(self.y - self.img.get_height() / 2),
                            self.img.get_width(),
                            self.img.get_height(),
                        )
                        for enemy in enemys:
                            if enemy != self and self.rect.colliderect(enemy.rect):
                                self.x += dt_adjusted(1)
                                break
                        if self.x > round(player.x):
                            break
                elif self.x > round(player.x) and abs(self.x - player.x) > 1:
                    for _ in range(3):
                        self.x += dt_adjusted(1)
                        self.rect = pygame.Rect(
                            self.x - self.img.get_width() / 2,
                            -(self.y - self.img.get_height() / 2),
                            self.img.get_width(),
                            self.img.get_height(),
                        )
                        for enemy in enemys:
                            if enemy != self and self.rect.colliderect(enemy.rect):
                                self.x -= dt_adjusted(1)
                                break
                        if self.x < round(player.x):
                            break
                if -self.y < round(player.y) and abs(-self.y - player.y) > 1:
                    for _ in range(3):
                        self.y += dt_adjusted(1)
                        self.rect = pygame.Rect(
                            self.x - self.img.get_width() / 2,
                            -(self.y - self.img.get_height() / 2),
                            self.img.get_width(),
                            self.img.get_height(),
                        )
                        for enemy in enemys:
                            if enemy != self and self.rect.colliderect(enemy.rect):
                                self.y -= dt_adjusted(1)
                                break
                        if -self.y < round(player.y):
                            break
                elif -self.y > round(player.y) and abs(-self.y - player.y) > 1:
                    for _ in range(3):
                        self.y -= dt_adjusted(1)
                        self.rect = pygame.Rect(
                            self.x - self.img.get_width() / 2,
                            -(self.y - self.img.get_height() / 2),
                            self.img.get_width(),
                            self.img.get_height(),
                        )
                        for enemy in enemys:
                            if enemy != self and self.rect.colliderect(enemy.rect):
                                self.y += dt_adjusted(1)
                                break
                        if -self.y > round(player.y):
                            break
        self.x = round(self.x)
        self.y = round(self.y)
        if self.rect.colliderect(player.rect):
            if player.dead:
                self.discoverdead = True
            if player.damage(20, "slain", "a zombie"):
                dx = player.x - self.x
                dy = player.y + self.y
                distance = math.sqrt(dx**2 + dy**2)
                dx /= distance
                dy /= distance

                player.dx += dx * 10
                player.dy += dy * 10

        for enemy in enemys:
            if enemy != self and self.rect.colliderect(enemy.rect):
                if self.x < enemy.x:
                    self.x -= dt_adjusted(1)
                elif self.x > enemy.x:
                    self.x += dt_adjusted(1)
                if self.y < enemy.y:
                    self.y -= dt_adjusted(1)
                elif self.y > enemy.y:
                    self.y += dt_adjusted(1)
                self.x = round(self.x)
                self.y = round(self.y)
                self.rect = pygame.Rect(
                    self.x - self.img.get_width() / 2,
                    -(self.y - self.img.get_height() / 2),
                    self.img.get_width(),
                    self.img.get_height(),
                )
        if x == self.x and y == self.y:
            self.resting = True
        else:
            self.resting = False


game_paused = True


def dt_adjusted(value):
    """

    :param value:

    """
    if clock.get_fps() == 0 or (game_paused and menu != "Start"):
        return 0
    return value / clock.get_fps() * 60


def create_tiles(noise, player, imgs, grassimgs, waterimgs, hbimgs):
    """

    :param noise:
    :param player:
    :param imgs:
    :param grassimgs:
    :param waterimgs:
    :param hbimgs:

    """
    tilemap = []
    tiles = []
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
    return tilemap, tiles


SEED = 1
if not SEED:
    seed = random.randint(-1125899906842624, 1125899906842624)
noise = PerlinNoise(octaves=1, seed=SEED)
player = Player()
tilemap, tiles = create_tiles(noise, player, imgs, grassimgs, waterimgs, hbimgs)

offsetx = 0
offsety = 0
menu = "Start"
quitb = Button(screen.get_width() / 2, screen.get_height() / 2 - 80, "Quit")
rsb = Button(screen.get_width() / 2, screen.get_height() / 2 + 75, "Restart")
resumeb = Button(screen.get_width() / 2, screen.get_height() / 2 + 75, "Resume")
debugb = Button(
    screen.get_width() / 2, screen.get_height() / 2 - 160, "Debug Mode (OFF)"
)
# Create a new game button
newgameb = Button(screen.get_width() / 2, screen.get_height() / 2 - 120, "New Game")
enemys = []
for i in range(10):
    enemys.append(Enemy(purpimgs, i * 100, 50))
quitb.active = False
resumeb.active = False
debugb.active = False
newgameb.active = False
pygame.key.set_repeat(200, 25)
deadsurf = pygame.Surface((screen.get_width(), screen.get_height())).convert_alpha()
deadsurf.fill((255, 0, 0, 100))
pausesurf = pygame.Surface((screen.get_width(), screen.get_height())).convert_alpha()
pausesurf.fill((0, 0, 0, 100))
while True:
    screen.fill((0, 0, 25))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            deadsurf = pygame.Surface(
                (screen.get_width(), screen.get_height())
            ).convert_alpha()
            deadsurf.fill((255, 0, 0, 100))
            pausesurf = pygame.Surface(
                (screen.get_width(), screen.get_height())
            ).convert_alpha()
            pausesurf.fill((0, 0, 0, 100))
    if quitb.activated:
        pygame.quit()
        sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_q]:
        pygame.quit()
        sys.exit()
    if menu == "Start":
        grass_offset_x += dt_adjusted(0.5)
        grass_offset_y += dt_adjusted(0.5)
        if grass_offset_x >= grassimgs["g"].get_width():
            grass_offset_x = 0
        if grass_offset_y >= grassimgs["g"].get_height():
            grass_offset_y = 0
        # Draw a matrix of the image "grassimgs["g"]"
        for i in range(
            -grassimgs["g"].get_width(), screen.get_width(), grassimgs["g"].get_width()
        ):
            for j in range(
                -grassimgs["g"].get_height(),
                screen.get_height(),
                grassimgs["g"].get_height(),
            ):
                screen.blit(grassimgs["g"], (i + grass_offset_x, j + grass_offset_y))
        quitb.active = True
        newgameb.active = True
        quitb.setpos(screen.get_width() / 2, screen.get_height() / 2 + 105)
        quitb.update_rect()
        quitb.draw()
        # Draw the new game button
        newgameb.setpos(screen.get_width() / 2, screen.get_height() / 2 + 51)
        newgameb.draw()
        # Check if the new game button is activated
        if newgameb.activated:
            menu = "Game"
        if keys[K_p]:
            menu = "Game"
        # Draw the title "Topdown"
        title_surface = fontbig.render("TOPDOWN", False, (255, 255, 255))
        screen.blit(
            title_surface,
            (
                screen.get_width() / 2 - title_surface.get_width() / 2,
                screen.get_height() / 2 - title_surface.get_height() / 2,
            ),
        )

    elif menu == "Game":
        if keys[K_p] and not player.dead:
            game_paused = True
        for tile in tiles:
            tile.draw()
        player.draw()
        player.move()
        for enemy in enemys:
            enemy.draw()
            enemy.move()
        offsetx = int(player.x) - screen.get_width() / 2
        offsety = int(player.y) + screen.get_height() / 2
        if player.dead:
            quitb.active = True
            rsb.active = True
            screen.blit(deadsurf, (0, 0))
            txt = fontbig.render(player.deathmessage, False, (255, 255, 255))
            screen.blit(
                txt,
                (
                    screen.get_width() / 2 - txt.get_width() / 2,
                    screen.get_height() / 2 - 100,
                ),
            )
            quitb.setpos(screen.get_width() / 2, screen.get_height() / 2 + 100)
            quitb.draw()
            rsb.setpos(screen.get_width() / 2, screen.get_height() / 2 + 154)
            rsb.draw()
            if rsb.activated:
                player.respawn()
        if game_paused:
            quitb.active = True
            resumeb.active = True
            debugb.active = True
            screen.blit(pausesurf, (0, 0))
            quitb.setpos(screen.get_width() / 2, screen.get_height() / 2 + 100)
            quitb.draw()
            resumeb.setpos(screen.get_width() / 2, screen.get_height() / 2 + 154)
            resumeb.draw()
            debugb.setpos(screen.get_width() / 2, screen.get_height() / 2 + 208)
            debugb.draw()
            txt = fontbig.render("Paused", False, (255, 255, 255))
            screen.blit(
                txt,
                (
                    screen.get_width() / 2 - txt.get_width() / 2,
                    screen.get_height() / 2 - txt.get_height() / 2,
                ),
            )
            if resumeb.activated:
                game_paused = False
            if debugb.activated:
                if DEBUG:
                    debugb.text.fill((0, 0, 0, 0))
                    debugb.text = font.render(
                        "Debug Mode (OFF)", False, (255, 255, 255)
                    )
                    debugb.update_rect()
                    DEBUG = False
                else:
                    debugb.text.fill((0, 0, 0, 0))
                    debugb.text = font.render("Debug Mode (ON)", False, (255, 255, 255))
                    debugb.update_rect()
                    DEBUG = True
    clock.tick()
    screen.blit(font.render(str(int(clock.get_fps())), False, (255, 255, 255)), (0, 0))

    pygame.display.flip()
