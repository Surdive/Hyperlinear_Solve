import itertools


def expand_matrix(matrix):
    """
    matrix : liste de listes dont les éléments sont des ensembles
    Retourne une liste de matrices où chaque élément est choisi
    dans l'ensemble correspondant de la matrice originale.
    """
    # Transformer la matrice en liste plate
    flat_sets = [cell for row in matrix for cell in row]

    # Produit cartésien de tous les ensembles
    all_combinations = itertools.product(*flat_sets)

    # Reconstruire les matrices à partir des combinaisons
    n_rows = len(matrix)
    n_cols = len(matrix[0]) if n_rows > 0 else 0

    result = []
    for comb in all_combinations:
        new_matrix = []
        for i in range(n_rows):
            row = []
            for j in range(n_cols):
                row.append(comb[i * n_cols + j])
            new_matrix.append(row)
        result.append(new_matrix)

    return result


#import itertools


def hyper_linear_solve(K, add_table, mul_table, A, B):
    """
    Résout B ⊆ A.X dans un hypercorps de Krasner K

    K : liste des éléments de l'hypercorps
    add_table : dict {(x,y): set} représentant l’hyperopération ⊕
    mul_table : dict {(x,y): element} représentant l’opération ⊙
    A : matrice (liste de listes) avec des éléments de K
    B : vecteur colonne (liste) avec des éléments de K

    Retourne l’ensemble des solutions S (liste de vecteurs X)
    """

    n_rows = len(A)
    n_cols = len(A[0])

    S = []

    # Produit cartésien pour générer tous les vecteurs candidats X
    for X in itertools.product(K, repeat=n_cols):
        # Calcul de A ⊙ X avec hyperaddition
        AX = []
        for i in range(n_rows):
            # On accumule l'ensemble des sommes possibles
            row_sets = [{mul_table[(A[i][j], X[j])]} for j in range(n_cols)]
            # Réduction avec l'hyperaddition
            possible = row_sets[0]
            for s in row_sets[1:]:
                new_possible = set()
                for u in possible:
                    for v in s:
                        new_possible |= add_table[(u, v)]
                possible = new_possible
            AX.append(possible)

        # Vérification B ⊆ A.X
        ok = True
        for i in range(n_rows):
            if B[i] not in AX[i]:
                ok = False
                break

        if ok:
            S.append(X)

    return S



# Exemple d'utilisation
M = [
    [{1, 2}, {0, 2}, {0, 1}],
    [{0, 1}, {1, 2}, {0, 2}],
    [{0, 1, 2}, {1, 2}, {1,2}]
]

L = expand_matrix(M)
#for mat in L:
 #   for row in mat:
  #      print(row)
   # print("---")
# --- Exemple ---
K = [0, 1, 2]

# Définition des tables d’un Krasner K
# hyperaddition:
add_table = {
    (0, 0): {0},
    (0, 1): {1},
    (0, 2): {2},
    (1, 0): {1},
    (1, 1): {1},
    (1, 2): {0, 1, 2},
    (2, 0): {2},
    (2, 1): {0, 1, 2},
    (2, 2): {2}
}

# multiplication:
mul_table = {
    (0, 0): 0,
    (0, 1): 0,
    (0, 2): 0,
    (1, 0): 0,
    (1, 1): 1,
    (1, 2): 2,
    (2, 0): 0,
    (2, 1): 2,
    (2, 2): 1
}

#A = [[1, 0],
 #    [0, 1]]
B = [1, 2, 0]

#solutions = hyper_linear_solve(K, add_table, mul_table, A, B)
#print("Solutions S =", solutions)
T=[]
for l in L:
   T.append(hyper_linear_solve(K, add_table, mul_table, l, B))

print(T)
print(len(T))