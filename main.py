import random
import pygame
from pygame.locals import *



# pygame setup 
pygame.init()

# Variable global 
s_width = 800
s_height = 700
play_width = 300 # 300 // 10 = 30 largeur par block
play_height = 600 # 600 // 20 = 20 hauteur par block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# grille de 10 X 20 
# formes : S, Z, I, O, J, L, T
# dans l'ordre de 0 - 6 

# codage des formes 
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]


formes = [S, Z, I, O, J, L, T]
couleurs_formes = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    lignes = 20 # y
    colonnes = 10 # x

    def __init__(self, colonne, ligne, forme):
        self.x = colonne
        self.y = ligne
        self.forme = forme
        self.couleur = couleurs_formes[formes.index(forme)]
        self.rotation = 0 # un nombre entre 0 - 3

def créer_grille(positions_bloqué = {}):
    grille = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if (j, i) in positions_bloqué:
                c = positions_bloqué[(j, i)]
                grille[i][j] = c
    return grille

def convertir_forme_format(forme):
    pass

def espace_valide(forme, grille):
    pass

def check_lost(positions):
    pass

def obt_forme():
    global formes, couleurs_formes

    return Piece(5, 0, random.choice(formes))

def dessiner_text_milieu(text, size, color, surface):
    pass

def dessiner_grille(surface, ligne, colonne):
    pass

def nettoyer_ligne(grille, bloqué):
    pass

def dessiner_forme_suivante(forme, surface):
    pass

def dessiner_fenetre(surface):
    pass

def main():
    global grille

    positions_bloqué = {}
    grille = créer_grille(positions_bloqué)

    change_piece = False
    run = True
    piece_actuelle = obt_forme()
    piece_suivante = obt_forme()
    clock = pygame.time.Clock()
    durée_chute = 0 

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece_actuelle.x -= 1
                    if not espace_valide(piece_actuelle, grille):
                        piece_actuelle += 1


def main_menu():
    pass

main_menu() # start game









screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("le meilleur jeu jamais créé !!!!")
running = True


# position des formes
circle_position_x = screen.get_width() / 2
circle_position_y = screen.get_height() / 2
rect_position_x = screen.get_width() / 2
rect_position_y = screen.get_height() / 2



while running :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    image_fond = pygame.image.load("fond.jpg")
    fond = image_fond.convert()
    # fill the screen with an image
    screen.blit(fond, (0,0))

    pygame.draw.circle(screen, "black", (circle_position_x, circle_position_y), 100) 
    
    
    # binding
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] : 
        circle_position_y -= 10
    if keys[pygame.K_DOWN] :
        circle_position_y += 10
    if keys[pygame.K_LEFT] :
        circle_position_x -= 10
    if keys[pygame.K_RIGHT] :
        circle_position_x += 10
    

    pygame.display.update()

pygame.quit()