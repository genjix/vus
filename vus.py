import pygame
import random
from speakers import speakers
import life

def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

class SpeakerView:

    def __init__(self, speaker_model):
        name_font = pygame.font.SysFont("Ubuntu", 40)
        name_text = speaker_model[0] + " " + speaker_model[1]
        self.name = name_font.render(name_text, 1, (0xaf, 0x4e, 0x4e))
        path = "ppl/" + speaker_model[2].replace(".jpg", ".png")
        self.picture = pygame.image.load(path)
        self.picture_fadeable = self.picture.convert(24)
        # Bio
        self.bio_font = pygame.font.SysFont("Monospace", 14)
        self.remaining_bio = speaker_model[4]
        # Trim annoying "\n" at beginning of bio if it exists.
        if self.remaining_bio[0] == "\n":
            self.remaining_bio = self.remaining_bio[1:]
        self.typed_bio = ""
        self.bio_lines = []
        self.timeline = 0
        self.typing_timeline = 0
        # Stats
        self.progressbar = pygame.image.load("progressbar.png")
        self.stats = [
            # label current_progress max_value label
            ["Fury", 0, 40, None],
            ["Attack", 0, 100, None],
            ["Magic", 0, 200, None],
            ["Agility", 0, 200, None],
            ["Exp", 0, 200, None],
        ]
        # create stat values
        supply = 300 * 4
        values = [random.randrange(0, 1000) for i in range(len(self.stats))]
        values = [value * supply / sum(values) for value in values]
        assert sum(values) < supply
        # populate labels and copy values
        stat_font = pygame.font.SysFont("Ubuntu", 16)
        for i, stat in enumerate(self.stats):
            stat[2] = values[i] if values[i] < 300 else 300
            stat[3] = stat_font.render(stat[0] + ":", 1, (0xff, 0xff, 0xff))

    def finished(self):
        if self.timeline < 5000:
            return False
        if not self.remaining_bio:
            return True
        return False

    def update(self, time):
        self.timeline += time
        self.typing_timeline += time
        if self.timeline < 3000:
            for stat in self.stats:
                # Increase current towards max
                stat[1] = self.timeline * stat[2] / 3000
            self.picture_fadeable.set_alpha(self.timeline * 255 / 3000)
            self.render_picture = self.picture_fadeable
        else:
            for stat in self.stats:
                stat[1] = stat[2]
            self.render_picture = self.picture

        if self.typing_timeline > 10:
            self.next_letter()

    def cycle_remaining_bio(self):
        self.remaining_bio = self.remaining_bio[1:]

    def next_letter(self):
        if not self.remaining_bio:
            return
        # Strip out links
        if self.remaining_bio[0] == "<":
            while self.remaining_bio[0] != ">":
                self.cycle_remaining_bio()
            # Strip the > also
            self.cycle_remaining_bio()
        self.typing_timeline = 0
        # Turn "\n"s into spaces.
        if self.remaining_bio[0] == "\n":
            self.typed_bio += " "
        else:
            self.typed_bio += self.remaining_bio[0]
        self.cycle_remaining_bio()
        # Render lines
        lines = split_len(self.typed_bio, 80)
        self.bio_lines = []
        for line in lines:
            bio_line = self.bio_font.render(line, 1, (0xff, 0xff, 0xff))
            self.bio_lines.append(bio_line)

    def display(self, screen):
        screen.blit(self.render_picture, (50, 50))
        screen.blit(self.name, (300, 50))
        for i, line in enumerate(self.bio_lines):
            screen.blit(line, (50, 300 + i * self.bio_font.get_height()))
        for i, stat in enumerate(self.stats):
            label = stat[3]
            y = 120 + i * 25
            screen.blit(label, (300, y))
            progress = stat[1]
            screen.blit(self.progressbar, (360, y),
                        (0, 0, progress, self.progressbar.get_height()))

class LifeGrid:

    def __init__(self, screen_size, multp):
        width, height = screen_size[0] / multp, screen_size[1] / multp
        self.grid = [[round(random.random()) for cell in range(width)]
                     for row in range(height)]
        self.multp = multp
        self.timeline = 0

    def update(self, time):
        self.timeline += time
        if self.timeline > 200:
            self.timeline = 0
            self.grid = life.lifestep(self.grid)

    def display(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 0:
                    continue
                pos = (x * self.multp, y * self.multp)
                size = (self.multp, self.multp)
                screen.fill((0x0f, 0x0f, 0x0f), (pos, size))

if __name__ == "__main__":
    screen_size = (800, 600)
    life_granularity = 10

    pygame.init()
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    unsystem_font = pygame.font.SysFont("Ubuntu Italic Bold", 60)
    unsystem = unsystem_font.render("unSYSTEM.net (VIENNA 1-3 Nov 2013)",
                                    1, (0x2f, 0x1f, 0x1f))

    finished = False
    speaker = SpeakerView(speakers[0])
    lifegrid = LifeGrid(screen_size, life_granularity)
    clock = pygame.time.Clock()
    next_ticker = 0
    while not finished:
        clock.tick()
        if speaker.finished():
            next_ticker += clock.get_time()
        if next_ticker > 2000:
            # Rotate to next speaker
            speakers = speakers[1:] + speakers[0:1]
            speaker = SpeakerView(speakers[0])
            lifegrid = LifeGrid(screen_size, life_granularity)
            next_ticker = 0
        lifegrid.update(clock.get_time())
        speaker.update(clock.get_time())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finished = True
        screen.fill((0, 0, 0))
        lifegrid.display(screen)
        speaker.display(screen)
        screen.blit(unsystem, (50,
            screen_size[1] - unsystem_font.get_height() - 40))
        pygame.display.flip()
        pygame.time.wait(50)

