import sys
import random
import pygame_textinput
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

# initialisation du module pour permettre à l'utilisateur d'écrire 
text_input = pygame_textinput.TextInputVisualizer()
text_input.font_color = (255, 0, 0)
text_input.cursor_color = (255, 0, 0)

# liste et fichier pour sauvegarder les scores
fichier_score = "scores.txt"
scores = []

# vitesse de la chute des formes (valeur plus petite = vitesse plus élevée)
fall_speed = 0.27

# formes
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

# liste des formes
formes = [S, Z, I, O, J, L, T]

# permet de générer une couleur aléatoire pour chaque pièce
def couleur_aléatoire():
    r =random.randint(100, 255) # rouge 
    g = random.randint(100, 255) # vert
    b = random.randint(100, 255) # bleu
    rgb = [r, g, b] # rgb liste 
    return rgb

class Piece(object):  
    def __init__(self, x, y, forme):
        self.x = x # position x de la pièce
        self.y = y # position y de la pièce
        self.forme = forme 
        self.couleur = couleur_aléatoire() # appel la fonction pour créer une couelur aléatoire pour chaque pièce
        self.rotation = 0 # orientation de la pièce 

def créer_grille(bloqué_pos={}):  
    # permet de créer une liste de 20 éléments où chaque élément est défini par (0, 0, 0)
    # chaque élkément de la liste contient aussi une liste de 10 éléments défini par (0, 0, 0)
    # cela permet de créer la grille du jeu

    grille = [[(0,0,0) for _ in range(10)] for _ in range(20)] 

    for i in range(len(grille)): # permet d'accéder à chaque ligne de la grille
        for j in range(len(grille[i])): #permet d'accéder à chaque colonne de la ligne
            if (j, i) in bloqué_pos: # vérifie si la position actuelle dans la grille se trouve également dans le dictionnaire bloqué_pos 
                c = bloqué_pos[(j,i)] # la valeur correspondant à (j, i) est récupéré dans le dictionnaire bloqué_pos
                grille[i][j] = c # remplace la valeur initiale (0, 0, 0) de la cellule par la valeur extraite du dictionnaire
    return grille # mise à jour de la grille

def convertir_format_forme(forme):
    positions = []
    format = forme.forme[forme.rotation % len(forme.forme)] # permet de récupérer l'orientation de la forme

    for i, ligne in enumerate(format):
        ligne = list(ligne)
        for j, column in enumerate(ligne):
            if column == '0': # vérifie si la colonne contient le caractère 0
                positions.append((forme.x + j, forme.y + i)) # ajoute la position de la forme dans la liste positions

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def espace_valide(forme, grille): # permet de gérer les colisions 
    position_accepté = [[(j, i) for j in range(10) if grille[i][j] == (0,0,0)] for i in range(20)] # la variable est initialisé en récupérant les cellules où la valeur est égale à (0, 0, 0)
    position_accepté = [j for sub in position_accepté for j in sub]

    formatté = convertir_format_forme(forme) # récupère la forme formatté  

    for pos in formatté:
        if pos not in position_accepté: # vérifie si la forme est en dehors de la grille ou chevauche une autre forme
            if pos[1] > -1:
                return False # la forme ne peut être placée
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1: # vérifie si la coordonnée y est inférieur à 1, soit au-dessus ou en-dessous de la première ligne de la grille
            return True # la forme ne peut être placée 

    return False

def obtenir_forme(): # permet de récupérer une forme au hasard
    return Piece(5, 0, random.choice(formes))

def dessiner_text_millieu(surface, text, taille, couleur): # permet de dessiner le text au millieu de l'écran
    font = pygame.font.SysFont("carlito", taille, bold=True) # définition de la police et de la taille 
    label = font.render(text, 1, couleur) # permet de faire un rendu du texte avec les paramètres de police défini dans la variable font

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2)) # permet de dessiner le texte

def dessiner_grille(surface, grille): # permet de dessiner la grille 
    sx = top_left_x 
    sy = top_left_y

    for i in range(len(grille)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_taille), (sx+play_width, sy+ i*block_taille)) # dessine les lignes
        for j in range(len(grille[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_taille, sy),(sx + j*block_taille, sy + play_height)) # dessine les colonnes

def lignes_libre(grille, bloqué):
    global fall_speed
    inc = 0 # compteur de ligne pleine
    for i in range(len(grille)-1, -1, -1): # itère sur les lignes en partant de la dernière jusqu'à la dernière
        ligne = grille[i]
        if (0,0,0) not in ligne: # vérifie si la ligne est pleine
            inc += 1
            ind = i
            for j in range(len(ligne)): # itère sur les colonnes 
                try:
                    del bloqué[(j,i)] # supprime la ligne si elle est pleine
                except:
                    continue

    if inc > 0: # vérifie si le nombre de lignes pleines est supérieur à zéro.
        for key in sorted(list(bloqué), key=lambda x: x[1])[::-1]:
            x, y = key # extrait les coordonnées x et y
            if y < ind: # vérifie si la coordonnée est inférieure à l'indice de la première ligne stockée
                newKey = (x, y + inc) # déplace la position vers le bas en tenant compte du nombre de ligne supprimées
                bloqué[newKey] = bloqué.pop(key) # supprime la clé d'origine et la remplace par la nouvelle
        fall_speed -= 0.01 * inc
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


def sauvegarder_score(score, pseudo_du_joueur, chemin_fichier):
    global scores
    scores.append({"pseudo": pseudo_du_joueur, "score" : score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:3] # garde uniquement les 3 meilleurs scores
    
    with open(chemin_fichier, "w") as fichier:
        for score_donnée in scores:
            ligne = f"{score_donnée['pseudo']}, {score_donnée['score']}\n"
            fichier.write(ligne)
    

def load_scores(chemin_fichier):
    scores.clear()
    try:
        with open(chemin_fichier, "r") as fichier:
            lignes = fichier.readlines()
            for ligne in lignes:
                pseudo, score  = ligne.strip().split(",")
                scores.append({"pseudo": pseudo, "score": int(score)})
    except FileNotFoundError:
        pass


def dessiner_fenetre(surface, grille, score=0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('carlito', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # score actuel
    font = pygame.font.SysFont('carlito', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))


    # meilleurs score
    load_scores(fichier_score)

    font_meilleurs_scores = pygame.font.SysFont('carlito', 50)

    sx_meilleurs_scores = top_left_x - 380
    sy_meilleurs_scores = top_left_y + 200

    for i, score in enumerate(scores):
        text = f"{i + 1}. {score['pseudo']}: {score['score']}"
        rendu_text = font_meilleurs_scores.render(text, True, (255,255,255))
        win.blit(rendu_text, (sx_meilleurs_scores, sy_meilleurs_scores))
        sy_meilleurs_scores += 80


    for i in range(len(grille)):
        for j in range(len(grille[i])):
            pygame.draw.rect(surface, grille[i][j], (top_left_x + j*block_taille, top_left_y + i*block_taille, block_taille, block_taille), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    dessiner_grille(surface, grille)
    

def main(win):  
    bloqué_positions = {}
    grille = créer_grille(bloqué_positions)

    change_piece = False
    run = True
    current_piece = obtenir_forme()
    next_piece = obtenir_forme()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score_actuel = 0

    cross_couleur = (255, 0, 0)
    cross_pos = (s_width - 200, 50)
    cross_taille = 50

    
    while run:
        grille = créer_grille(bloqué_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        
        if level_time/1000 > 5:
            level_time = 5
            
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
                sauvegarder_score(score_actuel, text_input.value, fichier_score)
                pygame.display.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if pygame.Rect(cross_pos, (cross_taille, cross_taille)).collidepoint(event.pos):
                    sauvegarder_score(score_actuel, text_input.value, fichier_score)
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
            score_actuel += lignes_libre(grille, bloqué_positions) * 10 
            
            

        dessiner_fenetre(win, grille, score_actuel)
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
            sauvegarder_score(score_actuel, text_input.value, fichier_score)


def main_menu(win, text_input):  
    run = True
    cross_couleur = (255, 0, 0)
    cross_pos = (s_width - 100, 50)
    cross_taille = 50
    boutton_enter_pos = (s_width / 2 - 80, s_height / 2 + 160)

    
    while run:
        win.fill((0,0,0))

        events = pygame.event.get()

        # input pou pseudo
        pygame.draw.rect(win, (255, 255, 255), (s_width / 2 - 215, s_height / 2 + 10, 500, 100), 3)


        text_input.update(events)
        win.blit(text_input.surface, (s_width / 2.8, s_height / 2 + 50))
    
        font = pygame.font.SysFont("carlito", 55, bold=True)
        label = font.render("Veuillez écrire un pseudo", 1, (0,191,255))
        win.blit(label, (s_width / 2 - label.get_width() / 2.3, s_height / 2 - 130))    


        # boutton entrer 
        pygame.draw.rect(win, (255, 255, 255), (boutton_enter_pos[0], boutton_enter_pos[1], 200, 50))
        font_for_boutton = pygame.font.SysFont("carlito", 25, bold=True)
        text_boutton = font_for_boutton.render("jouer", 1, (0, 0, 0))
        win.blit(text_boutton, (s_width / 2 - 7, s_height / 2 + 173))

        # dessiner croix pour fermer le jeu
        pygame.draw.line(win, cross_couleur, cross_pos, (cross_pos[0] + cross_taille, cross_pos[1] + cross_taille), 10)
        pygame.draw.line(win, cross_couleur, (cross_pos[0] + cross_taille, cross_pos[1]), (cross_pos[0], cross_pos[1] + cross_taille), 10)


        pygame.display.update()

        pygame.key.set_repeat(200, 25) 
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if pygame.Rect(cross_pos, (cross_taille, cross_taille)).collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if pygame.Rect(boutton_enter_pos,(200, 50)).collidepoint(event.pos):
                    if text_input.value == "":
                        text_input.value = "un pseudo est requis"   
                    else:
                        main(win)
            

    pygame.display.quit()


win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # créer une fenêtre en plein écran
pygame.display.set_caption('Le meilleur jeu du monde !!') # titre de la fenêtre
main_menu(win, text_input)

