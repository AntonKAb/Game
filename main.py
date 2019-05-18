from livewires import games, colour
import pygame
import random

games.init(screen_width=1024, screen_height=512, fps=60)


class Hero(games.Sprite):

    points = 0
    sound = games.load_sound('sounds/game_over.wav')
    scr = games.load_image('img/hero_11.png')
    reloading = 0
    pause = 70

    def __init__(self, dx):
        super(Hero, self).__init__(image=Hero.scr,
                                   x=games.screen.width / 2,
                                   bottom=games.screen.height - 90, dx=dx)
        self.dx = dx

        self.score = games.Text(value=Hero.points,
                                size=32,
                                color=colour.black,
                                top=5,
                                right=games.screen.width - 12)
        self.score_letter = games.Text(value='Score: ',
                                       size=32, color=colour.black,
                                       top=5, right=games.screen.width - 20)
        games.screen.add(self.score)
        games.screen.add(self.score_letter)

        self.health = games.Text(value=1,
                                 size=32,
                                 color=colour.black,
                                 top=30, right=games.screen.width - 12)
        self.health_letter = games.Text(value='Health: ', size=32, color=colour.black,
                                        top=30, right=games.screen.width - 20)
        games.screen.add(self.health)
        games.screen.add(self.health_letter)

    def update(self):
        if self.reloading > 0:
            self.reloading -= 1
        if games.keyboard.is_pressed(games.K_a):
            self.dx = -1
        if games.keyboard.is_pressed(games.K_d):
            self.dx = 1

        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width

        if games.keyboard.is_pressed(games.K_1) and self.reloading == 0:
            knife = Knife(self.x)
            games.screen.add(knife)
            self.reloading = Hero.pause
            if self.left < 0:
                knife.destroy()

        if games.keyboard.is_pressed(games.K_SPACE) and self.reloading == 0:
            one_shoot = Bullet(self.x)
            games.screen.add(one_shoot)
            self.reloading = Hero.pause
            if self.right > games.screen.width:
                one_shoot.destroy()
            if self.left < 0:
                one_shoot.destroy()

        for _ in self.overlapping_sprites:
            if not games.keyboard.is_pressed(games.K_SPACE) and not games.keyboard.is_pressed(games.K_1):
                for sprite in self.overlapping_sprites:
                    sprite.destroy()
                    self.health.value -= 1
            if games.keyboard.is_pressed(games.K_SPACE) or games.keyboard.is_pressed(games.K_1):
                    self.score.value += 1
        if self.health.value == 0:
            self.endgame()
        if self.health.value <= 0:
            self.endgame()


    def check_score(self):
        if self.overlapping_sprites:
            self.score += 1


    @staticmethod
    def endgame():
        end = games.Message(value='DEATH', size=86, color=colour.red, x=games.screen.width / 2,
                            y=games.screen.height / 3, lifetime=2 * games.screen.fps, after_death=games.screen.quit)

        games.screen.add(end)
        Hero.sound.play()


class Ghost(games.Sprite):
    left_border = random.choice([-50, -70])
    right_border = random.choice([games.screen.width + 20, games.screen.width])
    run = 1
    img = {'type_one': games.load_image('img/ghost_1.png'),
           'type_two': games.load_image('img/ghost_2.png'),
           'type_three': games.load_image('img/ghost_2.png'),
           'type_four': games.load_image('img/ghost_2.png')}

    def __init__(self):
        super(Ghost, self).__init__(image=Ghost.img[random.choice(['type_one', 'type_two',
                                                                   'type_three', 'type_four'])],
                                    x=random.choice([self.left_border, self.right_border]),
                                    bottom=games.screen.height - 90, dx=0)

    def update(self):
        if self.x == self.left_border:
            self.dx = 1
        if self.x == self.right_border:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.dx = -1


class Bullet(games.Sprite):
    image = games.load_image('img/bullet.png')
    sound = games.load_sound('sounds/gun.wav')
    speed = 15

    def __init__(self, x):
        super(Bullet, self).__init__(image=Bullet.image, x=x + 80, dx=Bullet.speed, bottom=games.screen.height - 90)
        Bullet.sound.play()

    def update(self):
            for _ in self.overlapping_sprites:
                if not games.keyboard.is_pressed(games.K_SPACE):
                    for sprite in self.overlapping_sprites:
                        sprite.destroy()
                    Hero.points += 1


class Knife(games.Sprite):
    image = games.load_image('img/knife.png')
    speed = 4

    def __init__(self, x):
        super(Knife, self).__init__(image=Knife.image, x=x - 89, dx=Knife.speed * -1, bottom=games.screen.height - 140)

    def update(self):
        for _ in self.overlapping_sprites:
            if not games.keyboard.is_pressed(games.K_1):
                for sprite in self.overlapping_sprites:
                    sprite.destroy()
                Hero.points += 1


class Move_Right(games.Animation):
    images = []

    def __init__(self, x):
        for i in range(1, 6):
            Move_Right.images.append('animation/move_r' + str(i) + '.png')
        super(Move_Right, self).__init__(images=Move_Right.images, x=x, repeat_interval=10,
                                         n_repeats=1, bottom=games.screen.height - 90)


class Ghost_Death:
    images = []

    def __init__(self, x):
        for i in range(1, 8):
            Ghost_Death.images.append('animation/ghost_dead' + str(i) + '.png')
        super(Ghost_Death, self).__init__(images=Ghost_Death.images, x=x,
                                          repeat_interval=15, n_repeats=1, bottom=games.screen.height - 90)


class Start:

    def __init__(self):

        games.music.load('music/fon.wav')
        games.music.play(-1)

        self.hero = Hero(dx=0)
        games.screen.add(self.hero)

    def begin(self):
        wall_image = games.load_image('img/wall_1.jpg', transparent=False)
        games.screen.background = wall_image


def main():
    play_game = Start()
    play_game.begin()

    all_en = []

    enemy = [Ghost() for _ in range(3)]
    for obj in enemy:
        all_en.append(obj)
    for el in all_en:
        games.screen.add(el)

    games.mouse.is_visible = False
    games.screen.mainloop()


if __name__ == '__main__':
    main()
