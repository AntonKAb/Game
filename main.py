from livewires import games, colour
import pygame
import random

games.init(screen_width=1024, screen_height=512, fps=60)


class Hero(games.Sprite):
    first = 1
    second = 2

    dir = 1
    image = [0, 0]
    image[0] = games.load_image('img/hero_11.png')
    image[1] = pygame.transform.flip(image[0], 1, 0)
    sound = games.load_sound('sounds/game_over.wav')

    reloading = 0
    pause = 70

    def __init__(self, dx):
        super(Hero, self).__init__(image=Hero.image[0],
                                   x=games.screen.width / 2,
                                   bottom=games.screen.height - 90, dx=dx)
        self.dx = dx

        self.score = games.Text(value=0,
                                size=32,
                                color=colour.black,
                                top=5,
                                right=games.screen.width - 12)
        self.score_letter = games.Text(value='Score: ',
                                       size=32, color=colour.black,
                                       top=5, right=games.screen.width - 20)
        games.screen.add(self.score)
        games.screen.add(self.score_letter)

        self.health = games.Text(value=2,
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
        if games.keyboard.is_pressed(games.K_q):
            Hero.dir = -1
        if games.keyboard.is_pressed(games.K_e):
            Hero.dir = 1

        if games.keyboard.is_pressed(games.K_a):
            self.dx = -1
        if games.keyboard.is_pressed(games.K_d):
            self.dx = 1

        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width

        if games.keyboard.is_pressed(games.K_SPACE) and self.reloading == 0:
            one_shoot = Bullet(self.x)
            games.screen.add(one_shoot)
            self.reloading = Hero.pause
            if self.right > games.screen.width:
                one_shoot.destroy()
            if self.left < 0:
                one_shoot.destroy()
        for _ in self.overlapping_sprites:
            if not games.keyboard.is_pressed(games.K_SPACE):
                for sprite in self.overlapping_sprites:
                    sprite.destroy()
                    self.health.value -= 1
        if self.health.value == 0:
            self.endgame()
        if self.health.value <= 0:
            self.endgame()
        self.next_direction()

    def next_direction(self):
        if Hero.dir == -1:
            self.image = Hero.image[1]
        else:
            self.image = Hero.image[0]
    #     self.direction *= -1
    #     depend = {-1: 1, 1: 0}
    #     self.image = Hero.image[depend[self.direction]]


    @staticmethod
    def endgame():
        end = games.Message(value='DEATH', size=86, color=colour.red, x=games.screen.width / 2,
                            y=games.screen.height / 3, lifetime=2 * games.screen.fps, after_death=games.screen.quit)

        games.screen.add(end)
        Hero.sound.play()


class Ghost(games.Sprite):
    left_border = -50
    right_border = games.screen.width
    run = 1
    img = {'type_one': games.load_image('img/ghost_1.png'), 'type_two': games.load_image('img/ghost_2.png')}

    def __init__(self):
        super(Ghost, self).__init__(image=Ghost.img[random.choice(['type_one', 'type_two'])],
                                    x=random.choice([self.left_border, self.right_border]),
                                    bottom=games.screen.height - 90, dx=0)

    def death(self):
        self.destroy()

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
        if Hero.dir == 1:
            self.dx = 15
            for _ in self.overlapping_sprites:
                if not games.keyboard.is_pressed(games.K_SPACE):
                    for sprite in self.overlapping_sprites:
                        sprite.destroy()
        else:
            self.dx = -15
            self.x *= -1
            for _ in self.overlapping_sprites:
                if not games.keyboard.is_pressed(games.K_SPACE):
                    for sprite in self.overlapping_sprites:
                        sprite.destroy()


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
    _list = []

    def __init__(self):

        games.music.load('music/fon.wav')
        games.music.play(-1)

        self.hero = Hero(dx=0)
        games.screen.add(self.hero)

    def begin(self):
        wall_image = games.load_image('img/wall_1.jpg', transparent=False)
        games.screen.background = wall_image

    def new_ghost(self):
        ghost = Ghost()
        games.screen.add(ghost)


def main():
    play_game = Start()
    play_game.begin()

    for _ in range(1, 2):
        play_game.new_ghost()

    ghost = Ghost()
    games.screen.add(ghost)

    games.mouse.is_visible = False
    games.screen.mainloop()


if __name__ == '__main__':
    main()
