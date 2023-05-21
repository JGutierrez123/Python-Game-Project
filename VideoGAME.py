import pygame

pygame.font.init()



WIDTH, HEIGHT = 1000, 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("First Game!")



WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

F16 = (255, 0, 0)

F18 = (255, 0, 255)



BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

WINNER_FONT = pygame.font.SysFont('comicsans', 100)



FPS = 60

VEL = 5

BULLET_VEL = 20

MAX_BULLETS = 20
#55,40
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40



F18_HIT = pygame.USEREVENT + 1

F16_HIT = pygame.USEREVENT + 2



F18_SPACESHIP_IMAGE =  pygame.image.load('/home/kali/Downloads/plane1.jpg')

F18_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(

    F18_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)



F16_SPACESHIP_IMAGE =  pygame.image.load('/home/kali/Downloads/Plane2.jpg')

F16_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(

    F16_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)





def draw_window(f16, f18, f16_bullets, f18_bullets, F16_health, F18_health):

    WIN.fill(WHITE)

    pygame.draw.rect(WIN, BLACK, BORDER)



    F16_health_text = HEALTH_FONT.render(

        "Hits F16: " + str(F16_health), 1, BLACK)

    F18_health_text = HEALTH_FONT.render(

        "Hits F18: " + str(F18_health), 1, BLACK)

    WIN.blit(F16_health_text, (WIDTH - F16_health_text.get_width() - 10, 10))

    WIN.blit(F18_health_text, (3, 3))



    WIN.blit(F18_SPACESHIP, (f18.x, f18.y))

    WIN.blit(F16_SPACESHIP, (f16.x, f16.y))



    for bullet in f16_bullets:

        pygame.draw.rect(WIN, F16, bullet)



    for bullet in f18_bullets:

        pygame.draw.rect(WIN, F18, bullet)



    pygame.display.update()





def f18_handle_movement(keys_pressed, f18):

    if keys_pressed[pygame.K_a] and f18.x - VEL > 0:  # LEFT

        f18.x -= VEL

    if keys_pressed[pygame.K_d] and f18.x + VEL + f18.width < BORDER.x:  # RIGHT

        f18.x += VEL

    if keys_pressed[pygame.K_w] and f18.y - VEL > 0:  # UP

        f18.y -= VEL

    if keys_pressed[pygame.K_s] and f18.y + VEL + f18.height < HEIGHT - 15:  # DOWN

        f18.y += VEL





def f16_handle_movement(keys_pressed, f16):

    if keys_pressed[pygame.K_LEFT] and f16.x - VEL > BORDER.x + BORDER.width:  # LEFT

        f16.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and f16.x + VEL + f16.width < WIDTH:  # RIGHT

        f16.x += VEL

    if keys_pressed[pygame.K_UP] and f16.y - VEL > 0:  # UP

        f16.y -= VEL

    if keys_pressed[pygame.K_DOWN] and f16.y + VEL + f16.height < HEIGHT - 15:  # DOWN

        f16.y += VEL





def handle_bullets(f18_bullets, f16_bullets, f18, f16):

    for bullet in f18_bullets:

        bullet.x += BULLET_VEL

        if f16.colliderect(bullet):

            pygame.event.post(pygame.event.Event(F16_HIT))

            f18_bullets.remove(bullet)

        elif bullet.x > WIDTH:

            f18_bullets.remove(bullet)



    for bullet in f16_bullets:

        bullet.x -= BULLET_VEL

        if f18.colliderect(bullet):

            pygame.event.post(pygame.event.Event(F18_HIT))

            f16_bullets.remove(bullet)

        elif bullet.x < 0:

            f16_bullets.remove(bullet)





def draw_winner(text):

    draw_text = WINNER_FONT.render(text, 1, BLACK)

    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /

                         2, HEIGHT/2 - draw_text.get_height()/2))

    pygame.display.update()

    pygame.time.delay(5000)





def main():

    f16 = pygame.Rect(900, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    f18 = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)



    f16_bullets = []

    f18_bullets = []



    F16_health = 3

    F18_health = 3



    clock = pygame.time.Clock()

    run = True

    while run:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                run = False

                pygame.quit()



            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(f18_bullets) < MAX_BULLETS:

                    bullet = pygame.Rect(

                        f18.x + f18.width, f18.y + f18.height//2 - 2, 10, 5)

                    f18_bullets.append(bullet)



                if event.key == pygame.K_RALT and len(f16_bullets) < MAX_BULLETS:

                    bullet = pygame.Rect(

                        f16.x, f16.y + f16.height//2 - 2, 10, 5)

                    f16_bullets.append(bullet)



            if event.type == F16_HIT:

                F16_health -= 1


            if event.type == F18_HIT:

                F18_health -= 1

        winner_text = ""

        if F16_health <= 0:

            winner_text = "F18 Wins!"



        if F18_health <= 0:

            winner_text = "F16 Wins!"



        if winner_text != "":

            draw_winner(winner_text)
            break




        keys_pressed = pygame.key.get_pressed()

        f18_handle_movement(keys_pressed, f18)

        f16_handle_movement(keys_pressed, f16)



        handle_bullets(f18_bullets, f16_bullets, f18, f16)



        draw_window(f16, f18, f16_bullets, f18_bullets,

                    F16_health, F18_health)



