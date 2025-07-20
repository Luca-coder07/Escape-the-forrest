import pygame as pg
import random as rd

pg.init()

screen = pg.display.set_mode((500, 500))

# on ajoute la taille du monde en géneral
world_width = 1000
world_height = 1000

tree = pg.image.load("assets/images/tree.png")
# On ajoute des changements de direction au personnage
perso = [
    pg.image.load("assets/images/player_right.png"),
    pg.image.load("assets/images/player_left.png"),
    pg.image.load("assets/images/player_up.png"),
    pg.image.load("assets/images/player_down.png")
]
current_perso = perso[3] # On le met en face par defaut

# on crée une liste qui va contenir tous les arbres
forrest = []
tree_nbr = rd.randint(30, 50)

for i in range (tree_nbr):
    # On choisit la position de chaque arbre au hasard.
    pos = [rd.randint(0, 950), rd.randint(0, 950)] 
    forrest.append(pos)

pg.display.set_caption("Escape the forrest")

# Taille et position initiale du personnage
perso_largeur = 32
perso_hauteur = 32
perso_x = 225
perso_y = 225
vitesse = 1

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
        if player_screen_x >= 0:
            perso_x -= vitesse
    if touch[pg.K_RIGHT]:
        current_perso = perso[0]
        if player_screen_x <= 500 - 32: # Car le point a traiter est le point plus haut à gauche de l'image
            perso_x += vitesse
    if touch[pg.K_DOWN]:
        current_perso = perso[3]
        if player_screen_y <= 500 - 32: # Car le point a traiter est le point plus haut à gauche de l'image
            perso_y += vitesse
    if touch[pg.K_UP]:
        current_perso = perso[2]
        if player_screen_y >= 0:
            perso_y -= vitesse
    

    screen.fill((110, 55, 10))
    for i in range (tree_nbr):
        screen.blit(tree, (forrest[i][0] - camera_x, forrest[i][1] - camera_y)) # On affiche les arbres dans des positions random
    screen.blit(current_perso, (player_screen_x, player_screen_y)) # affichage du personnage au centre de l'ecran si on a pas atteint la position limite de l'ecran
    pg.display.update()
    pg.display.flip()

pg.quit()