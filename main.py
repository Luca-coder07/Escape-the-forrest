import pygame as pg
import random as rd

pg.init()

screen = pg.display.set_mode((500, 500))
tree = pg.image.load("assets/images/tree.png")
perso = pg.image.load("assets/images/Brick.png")

# on crée une liste qui va contenir tous les arbres
forrest = []
tree_nbr = rd.randint(10, 20)

for i in range (tree_nbr):
    # On choisit la position de chaque arbre au hasard.
    pos = [rd.randint(0, 400), rd.randint(0, 400)] 
    forrest.append(pos)

pg.display.set_caption("Escape the forrest")

# Taille et position initiale du personnage
perso_largeur = 100
perso_hauteur = 100
perso_x = 225
perso_y = 225
vitesse = 0.3

#boucle principal du jeu
running = 1
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = 0

    # Deplacement
    touch = pg.key.get_pressed()
    if touch[pg.K_LEFT]:
        perso_x -= vitesse
    if touch[pg.K_RIGHT]:
        perso_x += vitesse
    if touch[pg.K_DOWN]:
        perso_y += vitesse
    if touch[pg.K_UP]:
        perso_y -= vitesse

    screen.fill((110, 55, 10))
    for i in range (tree_nbr):
        screen.blit(tree, (forrest[i][0], forrest[i][1]))
    screen.blit(perso, (perso_x, perso_y))
    pg.display.update()
    pg.display.flip()

pg.quit()