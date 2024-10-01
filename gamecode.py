import pygame
from sys import exit

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = font.render(f"Score: {current_time//1000}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(midbottom = (60, 30))
    screen.blit(score_surface, score_rect)
    return current_time//1000

pygame.init()

screen = pygame.display.set_mode((600,200))
pygame.display.set_caption("Bimbo Shooting Range")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf', 30)

running = False

start_time = 0
score = 0


#Background data
sky_surface = pygame.image.load('sprites/sky.png').convert()
ground_surface = pygame.image.load('sprites/ground.png').convert()


#Player initial data
bimbo_surface = pygame.image.load('sprites/bimbo/bimbo_front.png').convert_alpha()
bimbo_rect = bimbo_surface.get_rect(midbottom = (80, 150))
bimbo_gravity = 0


#Dino initial data
dino_surface = pygame.image.load('sprites/enemies/dino.png').convert_alpha()
dino_rect = dino_surface.get_rect(midbottom = (600, 150))


#Bullet initial data
bullet_surface = pygame.image.load('sprites/bullet.png').convert_alpha()


#Initial Screen data
bimbo_stand_surface = pygame.image.load('sprites/bimbo/bimbo_jump.png').convert_alpha()
bimbo_stand_surface = pygame.transform.rotozoom(bimbo_stand_surface, 0, 2)
bimbo_stand_rect = bimbo_stand_surface.get_rect(center = (300, 100))

game_name = font.render("Bimbo Shooting Range", False, 'White')
game_name_rect = game_name.get_rect(center = (300, 25))

game_message = font.render("Press Space to RUN!", False, 'White')
game_message_rect = game_message.get_rect(center = (300, 175))


#Game Loop
while True:
    #Actions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #During the active game
        if running == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bimbo_rect.bottom == 150:
                    bimbo_gravity = -12

        #During the restart screen
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True
                    dino_rect.left = 600
                    #Previous Time (in case of restart)
                    start_time = pygame.time.get_ticks()

    if running:

        #Background
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 150))

        #Player
        bimbo_gravity += 0.6
        bimbo_rect.y += bimbo_gravity
        if bimbo_rect.bottom >= 150:
            bimbo_rect.bottom = 150
            bimbo_surface = pygame.image.load('sprites/bimbo/bimbo_front.png').convert_alpha()
        else:
            bimbo_surface = pygame.image.load('sprites/bimbo/bimbo_jump.png').convert_alpha()
        screen.blit(bimbo_surface, bimbo_rect)

        #Dino
        dino_rect.right -= 5
        if dino_rect.right < 0:
            dino_rect.left = 600
        screen.blit(dino_surface, (dino_rect))

        #Score
        score = display_score() 

        #Collision
        if dino_rect.colliderect(bimbo_rect):
            running = False

    else:
        screen.fill((147, 47, 55))
        screen.blit(bimbo_stand_surface, bimbo_stand_rect)
        screen.blit(game_name, game_name_rect)

        score_message = font.render(f"Score: {score}", False, 'White')
        score_message_rect = score_message.get_rect(center = (300, 175))

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
