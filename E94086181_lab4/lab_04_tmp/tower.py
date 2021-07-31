import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """

        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        #計算敵人和塔之距離,如果小於攻擊範圍即可以攻擊
        x1,y1=enemy.get_pos()
        x2,y2=self.center
        distance=math.sqrt((x1-x2)**2+(y1-y2)**2)
        if distance<self.radius:
            return True
        else:
            return False


    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        #先畫一個畫布,再把透明的圓畫在上面,最後把畫布新增到螢幕上
        x, y = self.center
        # create semi-transparent surface
        transparent_surface = pygame.Surface((self.radius*2,self.radius*2), pygame.SRCALPHA)
        transparency = 150  # define transparency: 0~255, 0 is fully transparent
        # draw the rectangle on the transparent surface
        pygame.draw.circle(transparent_surface, (192, 192, 192, transparency), (self.radius,self.radius), self.radius)
        win.blit(transparent_surface, (x - self.radius, y - self.radius))


        pass


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        #當self.cd_count未達到self.cd_max_count時(代表塔攻擊還在冷卻),回傳False(冷卻中),反之,回傳True(已可以攻擊)
        if self.cd_count<self.cd_max_count:
            self.cd_count += 1
            return False
        else:
            self.cd_count=0
            return True


    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        #如果塔攻擊已冷卻,且敵人位於塔的攻擊範圍,則敵人會被塔攻擊(會被扣血)
        is_cool_down=self.is_cool_down()
        if is_cool_down==True:
            for emeny in enemy_group.get():
                if self.range_circle.collide(emeny):
                    emeny.get_hurt(self.damage)
                    return

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        #如果滑鼠點擊的範圍是塔,則代表塔被點擊
        if self.rect.x<x<self.rect.x+70 and self.rect.y<y<self.rect.y+70:
            return True
        else:
            return False



    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

