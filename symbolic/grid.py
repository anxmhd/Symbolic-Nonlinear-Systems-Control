"""
    Partition de l'espace d'état X en états symboliques (cellules) 

    Réf : -Sec. 1.1.1 (partition X_1..X_m, interface d'abstraction q)
          -Sec. 3.2 / Tableau 3 (partition cartésienne uniforme).

    Convention : un état symbolique est identifié par un entier plat q dans [0, n_states),
    en ordre row-major (C). L'état « hors de X » (xi = 0 dans l'article) n'est PAS
    une cellule de la grille : cell_of renvoie -1 pour un point hors de X.

"""

from typing import Optional, Iterator

import numpy as np


class Grid : 
    """
      Grille sur X = [lower, upper], immuable après construction.

      Attributs publics :
      -------------------------------------------------------------------------------------------
      lower_x : np.ndarray[float]   bornes inférieures de X
      upper_x : np.ndarray[float]   bornes supérieures de X
      shape : np.ndarray[int]   nombre d'état symbolique par dimension (N_xi)
      periodic : np.ndarray[bool] dimensions périodiques (ex : angle x3 modulo 2π)
      eta : np.ndarray[float] (n,)     taille d'une cellule = (upper_x - lower_x) / shape 
      n_states : int         nombre total d'états symboliques' = prod(shape) = N_x1 * N_x2 * N_x3 
      -------------------------------------------------------------------------------------------
      =>l’indexation des cellules commence à 0 dans chaque dimension

    """

    def __init__(
                    self,
                    lower_x: np.ndarray, 
                    upper_x: np.ndarray, 
                    shape: np.ndarray,  
                    periodic: Optional[np.ndarray] = None ) -> None:

            """
                Construit la grille et calcule eta et n_states une seule fois.

                Paramètres
                -----------------------------------------------------------------------------
                lower_x upper_x : bornes de X par dimension de la forme (dim_x).
                shape : nombre de sous-intervalles par dimension (ex. [100, 100, 30], Tableau 3).
                periodic : indicateur par dimension ; par défaut aucune dimension périodique.
                -----------------------------------------------------------------------------

            """

            lower_x = np.asarray(lower_x, dtype=float)
            upper_x = np.asarray(upper_x, dtype=float)
            shape = np.asarray(shape)


            # Verification des dimension
            if lower_x.ndim != 1 or upper_x.ndim != 1 or shape.ndim != 1:
                raise ValueError("Grid parameters must be 1D arrays.")

            if not (lower_x.shape == upper_x.shape == shape.shape):
                raise ValueError("lower_x, upper_x and shape must have the same dimensions.")


            # Verification des bornes
            if not np.all(np.isfinite(lower_x)) or not np.all(np.isfinite(upper_x)):
                raise ValueError("Bounds must contain only finite values.")

            if np.any(upper_x <= lower_x):
                raise ValueError("upper_x must be greater than lower_x in every dimension.")


            # Vérification de la forme avant de la convertir en entiers
            if not np.issubdtype(shape.dtype, np.integer):
                raise TypeError("shape must contain integers.")

            if np.any(shape <= 0):
                raise ValueError("Every dimension in shape must be positive.")


            #  Verification de `periodic`
            if periodic is None:
                periodic = np.zeros(shape.size, dtype=bool)
            else:
                periodic = np.asarray(periodic)

                if periodic.shape != shape.shape:
                    raise ValueError("periodic must have the same dimensions as shape.")

                if not np.issubdtype(periodic.dtype, np.bool_):
                    raise TypeError("periodic must contain Boolean values.")


            # Stocker les attributs validés
            self.lower_x = lower_x
            self.upper_x = upper_x
            self.shape = shape
            self.periodic = periodic

            self.eta = (upper_x - lower_x) / shape
            self.n_states = int(np.prod(shape))
                    

            


    def q_grid(self, x:np.ndarray[float]) -> int:
      """
          Interface d'abstraction q : x ∈ X -> ξ ∈ Ξ  [ Sec. 1.1.1 ]
            => Associe chaque vecteur d'état continu à son état symbolique
            => Les dimensions périodiques sont ramenées dans [lower_x, upper_x) avant le calcul.

          Paramètres
          ---------------------------------------------------------------------------------------------------
          x : vecteur d'état continu de forme (dim_x)

          Retour
          ------------------------------------------------------------
          Identifiants plats de la cellule contenant x  
            => -1 si le point est hors de X.

      """
      pass

    def center_of(self, xi: int) -> np.ndarray[float]:
          """
            Cellules -> centre x* de chaque cellule
              => Calcule le centre de chaque cellule X_ξ : x* = (lo_ξ + hi_ξ) / 2

            [ Sec. 1.1.3, centre de l'intervalle d'états (méthode des dérivées
              bornées, Fig. 3b)]

            Paramètres
            ------------------------------------------------------------
            xi (int) : identifiants plat ξ 

            Retour
            ------------------------------------------------------------
            Centre de la cellule correspondante à l'état x_i forme (dim_x)
            
              
          """
          pass

  
    def p_grid(self, xi : int) -> np.ndarray:
              """
                Identifiant plat ξ -> bornes (lo_ξ , hi_ξ ) de la cellule (concrétisation).
                  => Associe chaque état symbolique à son hyper-rectangle continu

                [ Sec. 1.1.1, ensemble X_xi ; Eq. (3), fermeture cl(X_xi).
                  lo = lower_x + multi * eta et hi = lo + eta]

                Paramètres
                -----------------------------------------------------------------
                xi (int) : Identifiants plats ξ .
          
                Retour
                -----------------------------------------------------------------
                Coins min et max de la cellule X_ξ : (lo_ξ, hi_ξ)  
                de la forme (2 , dim_x) 

              """
              pass
        



    def cells_intersect(self, low: np.ndarray[float], high: np.ndarray[float]) -> np.ndarray[int]:
          """
            Identifiants de toutes les cellules dont l'intersection avec la boîte [low, high]
            est non vide .

            [ Sec. 1.1.2, définition de g(xi, sigma) juste après Eq. (3) :
              l'intersection avec cl(X_ξ+) doit être non vide ]

              => Comme la grille est uniforme, les cellules intersectées forment un
            hyper-rectangle d'indices obtenu à partir de :

                    idx_min = floor((low  - lower_x) / eta)
                    idx_max = floor((high - lower_x) / eta)

              => Dimensions périodiques : indices pris modulo shape . 
              => Dimensions non périodiques : la partie hors de X est ignorée.

              
          """
          pass


    def cells_inside(self, lo: np.ndarray[float], hi:np.ndarray[float]) -> np.ndarray[int]:
          """
            Identifiants des cellules entièrement contenues dans [lo, hi].

            Approximation intérieure, pour les ensembles sûrs et les cibles.
            Réf. : Sec. 3.2, Q_i = {xi | X_xi inclus dans R_i} ; Sec. 2.1 (ensemble S).

              =>Comme la grille est uniforme, les cellules incluses forment un
              hyper-rectangle d'indices obtenu à partir de :

                    idx_min = ceil((low  - lower_x) / eta)
                    idx_max = ceil((high - lower_x) / eta) - 1

              => Dimensions périodiques : indices pris modulo shape.
              => Dimensions non périodiques : la partie hors de X est ignorée.

          """
          pass


    def to_multi(self, xi: int) -> np.ndarray[int]:
          """
            Identifiant plat -> indice multidimensionnel

            Exemple
            ---------------------
            ξ = n -> (i, j, k)

          """
          pass
               

    def to_flat(self, multi: np.ndarray[int]) -> int :
          """
            Indice multidimensionnel -> identifiant plat 

          """

          # input could be a list or a numpy array
          multi = np.asarray(multi)

          # Verifying the dimension of the input 
          if multi.ndim !=1  :
              raise ValueError("The input be a 1D array")
          
          if not(multi.shape == self.shape.shape)  :
              raise ValueError("The input should have the same dimension as shape")

          xi+= multi[-1]
          l = len(self.shape)

          if l>=2:
            for i in range(l-2, 0,-1):
                xi+= multi[i]*self.shape[i+1:]
               
          return xi      
              
               
    

    def iter_all_symbolic_states(self, batch_size: int = 100_000) -> Iterator[np.ndarray[int]]:
            """
            Itérateur parcourant l'ensemble fini des états symboliques Ξ par lots, afin
            de borner la mémoire tout en permettant un traitement vectorisé de chaque lot.
    
            Paramètres
            ---------------------------------------------------------------------------
            batch_size (int) : Nombre maximal d'états symboliques par lot.

            Retour 
            ---------------------------------------------------------------------------
            Iterator[np.ndarray] :Suite de tableaux de forme (≤ batch_size,) contenant les identifiants plats des
            états symboliques .

            """
            pass

    


    
     
