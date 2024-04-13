import os

for file in os.listdir('./assets'):
    print(f"{file[:-4].upper()} = pygame.image.load('./assets/{file}')")