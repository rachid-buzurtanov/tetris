import pygame
import random

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR, HAUTEUR = 300, 600
TAILLE_BLOC = 30
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
COULEURS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0)]

# Formes Tetris
FORMES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Création de la fenêtre de jeu
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Tetris")

# Horloge pour contrôler le taux d'images par seconde
horloge = pygame.time.Clock()

# Fonction pour dessiner une forme à l'écran
def dessiner_forme(forme, position, couleur):
    for i in range(len(forme)):
        for j in range(len(forme[i])):
            if forme[i][j] == 1:
                pygame.draw.rect(ecran, couleur, (position[0] * TAILLE_BLOC + j * TAILLE_BLOC,
                                                  position[1] * TAILLE_BLOC + i * TAILLE_BLOC,
                                                  TAILLE_BLOC, TAILLE_BLOC))

# Fonction pour vérifier si une forme peut être placée à une position donnée
def est_position_valide(forme, position, plateau):
    for i in range(len(forme)):
        for j in range(len(forme[i])):
            if forme[i][j] == 1:
                x = position[0] + j
                y = position[1] + i
                if x < 0 or x >= LARGEUR // TAILLE_BLOC or y >= HAUTEUR // TAILLE_BLOC or plateau[y][x] != 0:
                    return False
    return True

# Fonction pour effacer les lignes complètes dans le plateau
def effacer_lignes(plateau):
    lignes_completes = [ligne for ligne in range(len(plateau)) if all(cellule != 0 for cellule in plateau[ligne])]
    for ligne in lignes_completes:
        del plateau[ligne]
        plateau.insert(0, [0] * (LARGEUR // TAILLE_BLOC))
    return len(lignes_completes)

# Boucle principale du jeu
def main():
    # Initialisation des variables
    plateau = [[0] * (LARGEUR // TAILLE_BLOC) for _ in range(HAUTEUR // TAILLE_BLOC)]
    forme_courante = random.choice(FORMES)
    couleur_courante = random.choice(COULEURS)
    position_courante = [LARGEUR // (2 * TAILLE_BLOC) - len(forme_courante[0]) // 2, 0]
    fin_du_jeu = False
    vitesse_chute = 1  # Vitesse initiale de la chute

    while not fin_du_jeu:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                fin_du_jeu = True

        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT] and est_position_valide(forme_courante, [position_courante[0] - 1, position_courante[1]], plateau):
            position_courante[0] -= 1
        if touches[pygame.K_RIGHT] and est_position_valide(forme_courante, [position_courante[0] + 1, position_courante[1]], plateau):
            position_courante[0] += 1
        if touches[pygame.K_DOWN] and est_position_valide(forme_courante, [position_courante[0], position_courante[1] + 1], plateau):
            position_courante[1] += 1

        # Rotation de la forme
        if touches[pygame.K_UP]:
            forme_rotated = list(zip(*reversed(forme_courante)))
            if est_position_valide(forme_rotated, position_courante, plateau):
                forme_courante = forme_rotated

        # Mouvement automatique vers le bas
        if est_position_valide(forme_courante, [position_courante[0], position_courante[1] + vitesse_chute], plateau):
            position_courante[1] += vitesse_chute
        else:
            # Placer la forme sur le plateau
            for i in range(len(forme_courante)):
                for j in range(len(forme_courante[i])):
                    if forme_courante[i][j] == 1:
                        x = position_courante[0] + j
                        y = position_courante[1] + i
                        plateau[y][x] = couleur_courante

            # Vérifier les lignes complètes
            lignes_effacees = effacer_lignes(plateau)

            # Choisir une nouvelle forme et couleur
            forme_courante = random.choice(FORMES)
            couleur_courante = random.choice(COULEURS)
            position_courante = [LARGEUR // (2 * TAILLE_BLOC) - len(forme_courante[0]) // 2, 0]

            # Vérifier la fin du jeu
            if not est_position_valide(forme_courante, position_courante, plateau):
                fin_du_jeu = True

        # Dessiner le plateau et la forme actuelle
        ecran.fill(NOIR)
        for i in range(len(plateau)):
            for j in range(len(plateau[i])):
                if plateau[i][j] != 0:
                    pygame.draw.rect(ecran, plateau[i][j], (j * TAILLE_BLOC, i * TAILLE_BLOC, TAILLE_BLOC, TAILLE_BLOC))

        dessiner_forme(forme_courante, position_courante, couleur_courante)

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Contrôler le taux d'images par seconde
        horloge.tick(5)  # Ajustez la valeur pour définir la vitesse désirée

    pygame.quit()

if __name__ == "__main__":
    main()
