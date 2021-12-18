from func import *

#Hàm hiển thị
def display(font_size, status, font_color, X1, X2, Y1, relative = False, posxInpt = 0, posyInpt = 0):
    status = str(status)
    font = pygame.font.SysFont('consolas', font_size)
    surface = font.render(status, True, font_color)
    size = surface.get_size()
    if relative:
        posx = posxInpt
        posy = posyInpt
    else:
        posx = (X1 - size[0]) / 2 + X2
        posy = Y1 - size[1] / 2
    SCREEN.blit(surface, (posx, posy))
    return [posx, posy]

def displayBack(name_file, scaleX, scaleY, posx, posy):
    image = pygame.image.load('image/' + str(name_file))
    image = pygame.transform.scale(image, (scaleX, scaleY))

    # surface_back = pygame.surface.Surface((scaleX, scaleY), flags=0)
    # SCREEN.blit(surface_back, (posx, posy))
    SCREEN.blit(image, (posx, posy))
    return [posx, posy]

def displayImage(name_file, scaleX, scaleY, posx, posy):
    image = pygame.image.load('image/icon/' + str(name_file))
    image = pygame.transform.scale(image, (scaleX, scaleY))

    # surface_back = pygame.surface.Surface((scaleX, scaleY), flags=0)
    # SCREEN.blit(surface_back, (posx, posy))
    SCREEN.blit(image, (posx, posy))
    return [posx, posy]

#Các hàm xử lý số liệu
def changeTime(realtime):
    second_after_process = int(realtime)
    minute = int(second_after_process / 60)
    second = second_after_process - minute * 60
    if minute < 10:
        if second < 10:
            time = '0' + str(minute) + ':' + '0' + str(second)
        else:
            time = '0' + str(minute) + ':' + str(second)
    else:
        if second < 10:
            time = str(minute) + ':' + '0' + str(second)
        else:
            time = str(minute) + ':' + str(second)
    return time

def pos_mouse(pos):
    icon_position = [
        [45, 95, 500, 550, 'choose_song_next'],
        [115, 165, 500, 550, 'prep'],
        [175, 225, 500, 550, 'run_pause'],
        [235, 285, 500, 550, 'next'],
        [305, 355, 500, 550, 'like'],
        [70, WINDOWWIDTH - 70, 445, 455, 'change_start_point_music'],
        [355, 369, 120, 340, 'change_volumn'],
        [25, 75, 20, 70, 'file'],
        [125, 175, 20, 70, 'search'],
        [225, 275, 20, 70, 'play'],
        [325, 375, 20, 70, 'setting'],
    ]

    for i in icon_position:
        if pos[0] >= i[0] and pos[0] <= i[1] and pos[1] >= i[2] and pos[1] <= i[3]:
            return icon_position.index(i)

def takequeue():
    list = []
    for name in glob.glob('music/*.mp3'):
        list.append(name)
    return list

def playMusic(number):
    list = []
    for name in glob.glob('music/*.mp3'):
        list.append(name)
    mixer.init()
    mixer.music.load(str(list[number]))
    song = MP3(str(list[number]))
    songLength = song.info.length
    mixer.music.play()
    return songLength

#Các class đặc trưng
class Disc():
    def __init__(self):
        self.angle = 0

    def update(self, run_pause, speed):
        if run_pause == -1:
            self.angle += speed * 8

    def draw(self):
        disc = pygame.image.load('image/discS.png')
        disc = pygame.transform.smoothscale(disc, (250, 250))
        rotate_image = pygame.transform.rotate(disc, self.angle)
        rect = rotate_image.get_rect()
        pos_disc = (((WINDOWWIDTH - rect.width) / 2), ((WINDOWHEIGHT - rect.height) / 2 - 70))
        SCREEN.blit(rotate_image, pos_disc)

class Volume():
    def __init__(self):
        self.volume = 1
        self.display = 130
        self.icon = 'max.png'

    def draw(self):
        pygame.draw.line(SCREEN, WHITE, (362, 130), (362, self.display), 3)
        pygame.draw.line(SCREEN, BLACK, (362, self.display), (362, 330), 3)
        pygame.draw.circle(SCREEN, BLACK, (362, self.display), 5)  # Hình tròn

    def update(self, point):
        ratio = int((point - 130) / 200 * 10) / 10
        self.volume = 1 - ratio
        if self.volume <= 0.05:
            self.volume = 0
        elif self.volume >= 0.95:
            self.volume = 1
        self.display = 130 + ratio * 200
        mixer.music.set_volume(self.volume)

    def out(self):
        return self.volume

class Song():
    def __init__(self, number):
        self.number = number
        self.list = takequeue()
        self.song = MP3(str(self.list[number]))
        self.length = self.song.info.length
        self.realtime = 70
        self.point = 70
        self.time = 0
        self.store = 0
        self.min_value = 1000

    def draw(self, time, check):
        display(20, str(self.list[self.number][6:]), WHITE, WINDOWWIDTH, 0, 400)
        display(15, str(changeTime(self.length)), WHITE, 70, WINDOWWIDTH - 70, 450)
        self.realtime = (time / (self.length * 1000)) * (WINDOWWIDTH - 140) + self.point
        if self.realtime <= WINDOWWIDTH - 70:
            if check:
                self.store = self.time + time / 1000
            else:
                pass
            display(15, str(changeTime(self.store)), WHITE, 70, 0, 450)
            pygame.draw.line(SCREEN, RED, (70, 450), (self.realtime, 450), 3)
            pygame.draw.line(SCREEN, WHITE, (self.realtime, 450), (WINDOWWIDTH - 70, 450), 3)
            pygame.draw.circle(SCREEN, RED, (self.realtime, 450), 5)  # Hình tròn
        else:
            self.realtime = WINDOWWIDTH - 70
            display(15, str(changeTime(self.length)), WHITE, 70, 0, 450)
            pygame.draw.line(SCREEN, RED, (70, 450), (self.realtime, 450), 3)
            pygame.draw.line(SCREEN, WHITE, (self.realtime, 450), (WINDOWWIDTH - 70, 450), 3)
            pygame.draw.circle(SCREEN, RED, (self.realtime, 450), 5)  # Hình tròn

        if self.min_value > int((self.length - self.store) * 100):
            self.min_value = int((self.length - self.store) * 100)
        elif self.min_value == int((self.length - self.store) * 100):
            self.min_value = 0

    def update(self, point):
        if int((point - 70) / (WINDOWWIDTH - 140)) < 1:
            self.point = point
            self.time = (self.point - 70) / (WINDOWWIDTH - 140) * self.length
            mixer.music.set_pos(self.time)
        else:
            pass

    def out(self):
        if self.min_value == 0:
            print('ok')
            return True
        else:
            return False

class Icon():
    def __init__(self):
        self.how_to_change = 'continue.png'
        self.run = 'pause.png'

    def draw(self, run_pause):
        if run_pause == -1:
            self.run = 'pause.png'
        else:
            self.run = 'run.png'

        displayImage(self.how_to_change, 50, 50, 45, 500)
        displayImage('prep.png', 50, 50, 115, 500)
        displayImage(self.run, 50, 50, 175, 500)
        displayImage('next.png', 50, 50, 235, 500)
        displayImage('like.png', 50, 50, 305, 500)

    def update(self, change_queue):
        if change_queue == 0:
            self.how_to_change = 'continue.png'
        elif change_queue == 1:
            self.how_to_change = 'random.png'
        elif change_queue == 2:
            self.how_to_change = 'replay-all.png'
        elif change_queue == 3:
            self.how_to_change = 'replay-one.png'

class Page():
    def __init__(self):
        self.file = 'file.png'
        self.search = 'search.png'
        self.play = 'play_c.png'
        self.setting = 'setting.png'
        self.file_c = 1
        self.search_c = 1
        self.play_c = -1
        self.setting_c = 1

    def draw(self):
        if self.file_c == 1:
            self.file = 'file.png'
        else:
            self.file = 'file_c.png'

        if self.search_c == 1:
            self.search = 'search.png'
        else:
            self.search = 'search_c.png'

        if self.play_c == 1:
            self.play = 'play.png'
        else:
            self.play = 'play_c.png'

        if self.setting_c == 1:
            self.setting = 'setting.png'
        else:
            self.setting = 'setting_c.png'

        displayImage(self.file, 50, 50, 25, 20)
        displayImage(self.search, 50, 50, 125, 20)
        displayImage(self.play, 50, 50, 225, 20)
        displayImage(self.setting, 50, 50, 325, 20)

    def update(self, status):
        if status == 0:
            self.file_c *= -1
            self.search_c = 1
            self.play_c = 1
            self.setting_c = 1
        if status == 1:
            self.search_c *= -1
            self.file_c = 1
            self.play_c = 1
            self.setting_c = 1
        if status == 2:
            self.play_c *= -1
            self.file_c = 1
            self.search_c = 1
            self.setting_c = 1
        if status == 3:
            self.setting_c *= -1
            self.file_c = 1
            self.search_c = 1
            self.play_c = 1

#Hàm chạy

disc = Disc()
volume = Volume()
song = Song(number=0)
icon = Icon()
page = Page()

def play_screen():

    number = 0
    playMusic(number)
    song.__init__(number)

    mute_volumn = -1
    run_pause = -1
    change_queue = 0
    start_realtime = 0
    unpause_realtime = 0
    pause_realtime = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                status = pos_mouse(pos)

                # Các trạng thái chuyển bài
                if status == 0:
                    if change_queue == 3:
                        change_queue = 0
                    else:
                        change_queue += 1
                    icon.update(change_queue)
                if status == 1:
                    number -= 1
                    song.__init__(number)
                    start_realtime = pygame.time.get_ticks()
                    playMusic(number)
                if status == 3:
                    if number == len(takequeue()) - 1:
                        number = 0
                    else:
                        number += 1
                    song.__init__(number)
                    start_realtime = pygame.time.get_ticks()
                    playMusic(number)

                # Các trạng thái ảnh hưởng đến bài hát
                if status == 2:# Trạng thái của nút pause/run
                    run_pause *= -1
                    if run_pause == -1:
                        unpause_realtime = pygame.time.get_ticks()
                    else:
                        pause_realtime = pygame.time.get_ticks()
                if status == 5:# Trạng thái bài hát
                    start_realtime = pygame.time.get_ticks()
                    song.update(pos[0])

                # Các trạng thái ảnh hưởng đến âm lượng
                if status == 6:# Trạng thái điều khiển thanh âm lượng
                    volume.update(pos[1])

                # Chuyển trang
                if status == 7:
                    page.update(0)
                if status == 8:
                    page.update(1)
                if status == 9:
                    page.update(2)
                if status == 10:
                    page.update(3)


            if event.type == MOUSEBUTTONUP:
                status = -1

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    run_pause *= -1
                    if run_pause == -1:
                        unpause_realtime = pygame.time.get_ticks()
                    else:
                        pause_realtime = pygame.time.get_ticks()
                if event.key == K_m:
                    mute_volumn *= -1
                    if mute_volumn == -1:
                        volume.update(330)
                    else:
                        volume.update(230)

        if song.out():
            if change_queue == 0:
                number += 1
                if number > len(takequeue()) - 1:
                    number = None
            if change_queue == 1:
                number = random.randrange(0, len(takequeue()) - 1, 1)
            if change_queue == 2:
                number += 1
                if number > len(takequeue()) - 1:
                    number = 0
            if change_queue == 3:
                number = number
            if number != None:
                song.__init__(number)
                start_realtime = pygame.time.get_ticks()
                playMusic(number)

        if run_pause != -1:
            mixer.music.pause()
        else:
            mixer.music.unpause()

        stop_realtime = pygame.time.get_ticks()
        realtime = stop_realtime - start_realtime
        pause = unpause_realtime - pause_realtime
        displayBack('background1.png', WINDOWWIDTH, WINDOWHEIGHT, 0, 0)
        disc.update(run_pause, volume.out())
        disc.draw()
        volume.draw()
        page.draw()
        if mixer.music.get_busy():
            song.draw(realtime - pause, True)
        else:
            song.draw(realtime, False)
        icon.draw(run_pause)


        pygame.display.update()
        fpsClock.tick(FPS)

play_screen()

