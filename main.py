import os
import pygame
import shutil
import sys

from screeninfo import get_monitors


accepted_keys = [pygame.K_RETURN, pygame.K_BACKSPACE]
output = []

monitor = get_monitors()[0]

if not os.path.isdir("photos/"):
    os.mkdir("photos/")

if not os.path.isdir("output/"):
    os.mkdir("output/")
else:
    shutil.rmtree("output/")
    os.mkdir("output/")

pygame.init()

photo_dir = os.listdir("photos/")
photos = [f for f in photo_dir if os.path.isfile(os.path.join("photos/", f))]

running = True
photo_num = 0

photo = pygame.image.load(os.path.join("photos/", photos[0]))
photo_rect = photo.get_rect()

screen = pygame.display.set_mode((photo_rect.width, photo_rect.height))
pygame.display.set_caption("PhotoSort: " + photos[0])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in accepted_keys:
                if photo_num == len(photos) - 1:
                    running = False
                else:
                    photo_num += 1

                    screen.fill((0, 0, 0))

                    photo = pygame.image.load(os.path.join("photos/", photos[photo_num]))
                    photo_rect = photo.get_rect()

                    if photo_rect.width > monitor.width / 1.5:
                        photo = pygame.transform.scale(photo, (monitor.width / 1.5, photo_rect.height * monitor.width / 1.5 / photo_rect.width))
                        photo_rect = photo.get_rect()

                    if photo_rect.height > monitor.height / 1.5:
                        photo = pygame.transform.scale(photo, (photo_rect.width * monitor.height / 1.5 / photo_rect.height, monitor.height / 1.5))
                        photo_rect = photo.get_rect()

                    screen = pygame.display.set_mode((photo_rect.width, photo_rect.height))
                    pygame.display.set_caption("PhotoSort: " + photos[photo_num])
            if event.key == pygame.K_RETURN:
                output.append(photos[photo_num])

    screen.blit(photo, photo_rect)
    pygame.display.flip()

for photo_name in output:
    shutil.copy(os.path.join("photos/", photo_name), os.path.join("output/", photo_name))

pygame.quit()
sys.exit()
