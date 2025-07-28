import pygame as pg
import random as rd
import time


pg.init()

screen = pg.display.set_mode((500, 500))

# on ajoute la taille du monde en géneral
world_width = 1000
world_height = 1000

font = pg.font.SysFont(None, 30)
key_to_find = 0
clock = pg.time.Clock()

tree_img = pg.image.load("assets/images/tree.png")
# On ajoute des changements de direction au personnage
perso = [
    pg.image.load("assets/images/player_right.png"),
    pg.image.load("assets/images/player_left.png"),
    pg.image.load("assets/images/player_up.png"),
    pg.image.load("assets/images/player_down.png")
]
current_perso = perso[3] # On le met en face par defaut

key_img = pg.image.load("assets/images/key.png")
keys_rect = []
display_keys = [1, 1, 1, 1, 1]
for i in range (5):
    key_x = rd.randint(0, 950)
    key_y = rd.randint(0, 950)
    key_width = 18
    key_height = 10
    key_rect = pg.Rect(key_x, key_y, key_width, key_height)
    keys_rect.append(key_rect)

# on crée une liste qui va contenir tous les arbres
forrest = []
forrest_rect = []
tree_nbr = rd.randint(30, 50)

for i in range (tree_nbr):
    valid_position = False
    while not valid_position:
        # On choisit la position de chaque arbre au hasard.
        x = rd.randint(0, 950)
        y = rd.randint(0, 950)
        tree_rect = pg.Rect(x + 10, y + 30, 10, 20)
        tree_pos = pg.Rect(x, y, 29, 54)
        # Verifie s'il y a collision avec les arbres placés
        collision = False
        for other_rect in forrest:
            if tree_pos.colliderect(other_rect):
                collision = True
                break
        if not collision:
            forrest.append(tree_pos)
            forrest_rect.append(tree_rect)
            valid_position = True

pg.display.set_caption("Escape the forrest")

# Taille et position initiale du personnage
perso_largeur = 16
perso_hauteur = 30
perso_x = 225
perso_y = 225
vitesse = 3

perso_rect = pg.Rect(perso_x, perso_y, perso_largeur, perso_hauteur)

def draw_key_found(surface, key_to_find):
    text = font.render(f"Keys found(s): {key_to_find} / 5", True, (255, 255, 255))
    surface.blit(text, (10, 10))

def can_move(dx, dy):
    new_rect = perso_rect.move(dx, dy)
    for tree in forrest_rect:
        if new_rect.colliderect(tree):
            return False
    return True

# On choisit l'orientation de la lumière
orientation = "down"

# Timer
start_time = time.time()
game_over = False
win = False
#boucle principal du jeu
running = 1
while running:
    # On calcuse l'offset du camera (au moitié de l'écran)
    camera_x = perso_x - 250
    camera_y = perso_y - 250

    # On limite le camera pour qu'il n'aille pas en dehors du monde
    camera_x = max(0, min(camera_x, world_width - 500))
    camera_y = max(0, min(camera_y, world_height - 500))

    # Pour que le joueur atteint le bord du monde
    player_screen_x = perso_x - camera_x
    player_screen_y = perso_y - camera_y
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = 0

    # Deplacement
    touch = pg.key.get_pressed()
    if touch[pg.K_LEFT]:
        current_perso = perso[1]
        orientation = "left"
        if player_screen_x >= 0 and can_move(-vitesse, 0):
            perso_x -= vitesse
            perso_rect.x = perso_x
    elif touch[pg.K_RIGHT]:
        current_perso = perso[0]
        orientation = "right"
        if player_screen_x <= 500 - 32 and can_move(vitesse, 0): # Car le point a traiter est le point plus haut à gauche de l'image
            perso_x += vitesse
            perso_rect.x = perso_x
    elif touch[pg.K_DOWN]:
        current_perso = perso[3]
        orientation = "down"
        if player_screen_y <= 500 - 32 and can_move(0, vitesse): # Car le point a traiter est le point plus haut à gauche de l'image
            perso_y += vitesse
            perso_rect.y = perso_y
    elif touch[pg.K_UP]:
        current_perso = perso[2]
        orientation = "up"
        if player_screen_y >= 0 and can_move(0, -vitesse):
            perso_y -= vitesse
            perso_rect.y = perso_y

    # On verifie la collision entre la cle et le perso
    for i in range(5):
        if perso_rect.colliderect(keys_rect[i]) and display_keys[i]:
            key_to_find += 1
            display_keys[i] = 0

    # Calcul de la position de la lumière
    offset = 50
    center_x = player_screen_x + perso_largeur // 2
    center_y = player_screen_y + perso_hauteur // 2
    if orientation == "up":
        light_pos = (center_x, center_y - offset)
    elif orientation == "down":
        light_pos = (center_x, center_y + offset)
    elif orientation == "left":
        light_pos = (center_x - offset, center_y)
    elif orientation == "right":
        light_pos = (center_x + offset, center_y)

    if not game_over and not win:
        elapsed = time.time() - start_time
        remaining = max(0, 15 - int(elapsed))

        # Win 
        if key_to_find >= 5:
            win = True

        # Temps ecoulé
        if remaining <= 0:
            game_over = True
        
        screen.fill((32, 62, 10))
        light_surf = pg.Surface((800, 600), pg.SRCALPHA)
        pg.draw.circle(light_surf, (255, 255, 100, 50), light_pos, 50)
        for i in range(5):
            if display_keys[i]:
                screen.blit(key_img, (keys_rect[i].x - camera_x, keys_rect[i].y - camera_y)) # affichage du clé à chercher par le personnage
        screen.blit(current_perso, (player_screen_x, player_screen_y)) # affichage du personnage au centre de l'ecran si on a pas atteint la position limite de l'ecran
        for i in range (tree_nbr):
            screen.blit(tree_img, (forrest[i][0] - camera_x, forrest[i][1] - camera_y)) # On affiche les arbres dans des positions random
        screen.blit(light_surf, (0, 0))
        draw_key_found(screen, key_to_find)
        # Affichage du timer
        if remaining <= 5:
            timer_text = font.render(f"{remaining}s", True, (255, 0, 0))
        else:
            timer_text = font.render(f"{remaining}s", True, (255, 255, 255))
        screen.blit(timer_text, (10, 470))
    elif win:
        # Affichage de win
        screen.fill((0, 0, 0))
        win_text = font.render("YOU WIN", True, (20, 250, 0))
        screen.blit(win_text, (200, 250))

    else:
        # Affichage de la game over
        screen.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (200, 250))
    pg.display.update()
    pg.display.flip()
    clock.tick(60)

pg.quit()
