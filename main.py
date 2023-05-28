import sys
import random
import pygame
from pygame.locals import *


# pygame setup 
pygame.font.init()

# variable globale
s_width = 1280
s_height = 720
play_width = 300  #  300 // 10 = 30 largeur par block
play_height = 600  #  600 // 20 = 30 hauteur par block
block_taille = 30


top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# format des formes

S = [['.....',
      '.....',
      '..00.',
      '.00..',
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

# list des formes
formes = [S, Z, I, O, J, L, T]


def couleur_aléatoire():
    r =random.randint(100, 255) # rouge 
    g = random.randint(100, 255) # vert
    b = random.randint(100, 255) # bleu
    rgb = [r, g, b] # rgb liste 
    return rgb


class Piece(object):  
    def __init__(self, x, y, forme):
        self.x = x
        self.y = y
        self.forme = forme
        self.couleur = couleur_aléatoire()
        self.rotation = 0


def créer_grille(bloqué_pos={}):  
    grille = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if (j, i) in bloqué_pos:
                c = bloqué_pos[(j,i)]
                grille[i][j] = c
    return grille


def convertir_format_forme(forme):
    positions = []
    format = forme.forme[forme.rotation % len(forme.forme)]

    for i, ligne in enumerate(format):
        ligne = list(ligne)
        for j, column in enumerate(ligne):
            if column == '0':
                positions.append((forme.x + j, forme.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def espace_valide(forme, grille):
    position_accepté = [[(j, i) for j in range(10) if grille[i][j] == (0,0,0)] for i in range(20)]
    position_accepté = [j for sub in position_accepté for j in sub]

    formatté = convertir_format_forme(forme)

    for pos in formatté:
        if pos not in position_accepté:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def obtenir_forme():
    return Piece(5, 0, random.choice(formes))


def dessiner_text_millieu(surface, text, taille, couleur):
    font = pygame.font.SysFont("carlito", taille, bold=True)
    label = font.render(text, 1, couleur)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))    


def dessiner_grille(surface, grille):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grille)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_taille), (sx+play_width, sy+ i*block_taille))
        for j in range(len(grille[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_taille, sy),(sx + j*block_taille, sy + play_height))


def lignes_libre(grille, bloqué):
    inc = 0
    for i in range(len(grille)-1, -1, -1):
        ligne = grille[i]
        if (0,0,0) not in ligne:
            inc += 1
            ind = i
            for j in range(len(ligne)):
                try:
                    del bloqué[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(bloqué), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                bloqué[newKey] = bloqué.pop(key)

    return inc


def dessiner_prochaine_forme(forme, surface):
    font = pygame.font.SysFont('carlito', 30)
    label = font.render('forme suivante', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = forme.forme[forme.rotation % len(forme.forme)]

    for i, ligne in enumerate(format):
        ligne = list(ligne)
        for j, column in enumerate(ligne):
            if column == '0':
                pygame.draw.rect(surface, forme.couleur, (sx + j*block_taille, sy + i*block_taille, block_taille, block_taille), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('scores.txt', 'r') as f:
        lignes = f.readlines()
        score = lignes[0].strip()

    return score


def dessiner_fenetre(surface, grille, score=0, dernier_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('carlito', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('carlito', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('Meilleur score: ' + dernier_score, 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx - 90, sy + 160))

    for i in range(len(grille)):
        for j in range(len(grille[i])):
            pygame.draw.rect(surface, grille[i][j], (top_left_x + j*block_taille, top_left_y + i*block_taille, block_taille, block_taille), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    dessiner_grille(surface, grille)
    

def main(win):  
    dernier_score = max_score()
    bloqué_positions = {}
    grille = créer_grille(bloqué_positions)

    change_piece = False
    run = True
    current_piece = obtenir_forme()
    next_piece = obtenir_forme()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    cross_couleur = (255, 0, 0)
    cross_pos = (s_width - 200, 50)
    cross_taille = 50

    while run:
        grille = créer_grille(bloqué_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(espace_valide(current_piece, grille)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            # pour mettre le jeu en pause
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                win.fill((0, 0, 0))
                dessiner_text_millieu(win, 'LE JEU EST EN PAUSE', 60, (255,255,255))
                pygame.display.update()
            
                # sous boucle unpause
                while run: 
                    ev = pygame.event.wait()
                    if ev.type == KEYDOWN and ev.key == K_ESCAPE:   
                        break

            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if pygame.Rect(cross_pos, (cross_taille, cross_taille)).collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            pygame.key.set_repeat(200)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(espace_valide(current_piece, grille)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(espace_valide(current_piece, grille)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(espace_valide(current_piece, grille)):
                        current_piece.y -= 1
                if event.key == pygame.K_SPACE:
                    current_piece.rotation += 1
                    if not(espace_valide(current_piece, grille)):
                        current_piece.rotation -= 1

        forme_pos = convertir_format_forme(current_piece)

        for i in range(len(forme_pos)):
            x, y = forme_pos[i]
            if y > -1:
                grille[y][x] = current_piece.couleur

        if change_piece:
            for pos in forme_pos:
                p = (pos[0], pos[1])
                bloqué_positions[p] = current_piece.couleur
            current_piece = next_piece
            next_piece = obtenir_forme()
            change_piece = False
            score += lignes_libre(grille, bloqué_positions) * 10

        dessiner_fenetre(win, grille, score, dernier_score)
        dessiner_prochaine_forme(next_piece, win)
        
        # dessiner croix pour fermer le jeu
        pygame.draw.line(win, cross_couleur, cross_pos, (cross_pos[0] + cross_taille, cross_pos[1] + cross_taille), 10)
        pygame.draw.line(win, cross_couleur, (cross_pos[0] + cross_taille, cross_pos[1]), (cross_pos[0], cross_pos[1] + cross_taille), 10)
        
        pygame.display.update()

        if check_lost(bloqué_positions):
            dessiner_text_millieu(win, "TU AS PERDU!!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(2500)
            run = False
            update_score(score)


def main_menu(win):  
    run = True
    cross_couleur = (255, 0, 0)
    cross_pos = (s_width - 100, 50)
    cross_taille = 50
    
    while run:
        win.fill((0,0,0))
        dessiner_text_millieu(win, 'Appuie sur une touche pour commencer', 60, (255,255,255))
        
        # dessiner croix pour fermer le jeu
        pygame.draw.line(win, cross_couleur, cross_pos, (cross_pos[0] + cross_taille, cross_pos[1] + cross_taille), 10)
        pygame.draw.line(win, cross_couleur, (cross_pos[0] + cross_taille, cross_pos[1]), (cross_pos[0], cross_pos[1] + cross_taille), 10)

        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if pygame.Rect(cross_pos, (cross_taille, cross_taille)).collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                main(win)
            

    pygame.display.quit()


win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Le meilleur jeu du monde !!')
main_menu(win)

