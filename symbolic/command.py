"""
    Ensemble fini de commandes symboliques U_symb.

    Réf. : Sec. 1.1.1 (ensemble fini {u_1..u_l} inclus dans U,
    Sigma = {1..l}, interface de concrétisation p) et Sec. 3.2 / Tableau 3
    (discrétisation uniforme des intervalles de commande).

"""

from typing import Tuple, Iterator

import numpy as np



class Command:
    """
        Ensemble fini de commandes, immuable après construction.

        Attributs
        ------------------------------------------------------------------------------------------
        control_upper Tuple[float, float] : bornes supérieures de U de la forme (ū₁ , ū₂)
        control_lower Tuple[float, float] : bornes inférieures de U de la forme (u̲₁ , u̲₂)
        nb_commands (int)   : nombre de commandes symboliques 
        size Tuple[float, float] : taille d'un sous-intervalles de U = (ū - u̲) / nb_commands
        ------------------------------------------------------------------------------------------
        =>l’indexation des commandes symboliques commence à 0 dans chaque dimension
        
    """

    def __init__(self, 
                 control_upper :Tuple[float, float], 
                 control_lower :Tuple[float, float] , 
                 nb_commands : int) -> None:

        pass


    def q_command(self , u:np.ndarray[float] ) -> int:
        '''         
            Commandes continues uσ -> Commande symbolique σ (interface de discrétisation).

            Paramètres
            ---------------------------------------------------------------------------
            u : Commandes continues uσ de la forme (dim_u)
            
            Retour
            ---------------------------------------------------------------------------
            Identifiant de la commande symbolique σ représentant l'intervalle contenant uσ
            => σ = floor((uσ- u̲)/size)
             
        '''

        pass


    def p_command(self, sigma: int) -> np.ndarray[float]:
        """
            Commande symbolique σ -> boîte de commandes continues uσ
            (interface de concrétisation).

            [Sec. 1.1.1, interface de concrétisation p(σ) = uσ ;
             utilisée dans le contrôleur concrétisé, Eq. (7)]

            Paramètres
            ---------------------------------------------------------------------------
            sigma (int) : identifiant de la commande symbolique σ
            
            Retour
            ---------------------------------------------------------------------------
            l'ensemble des commandes continues représentées par σ de forme (dim_u, 2)
             => Pour chaque dimension de commande u_i :[u_i_min, u_i_max]

        """
        pass

    def to_multi(self, sigma: int) -> Tuple[int]:
        """
            Identifiant plat -> indice multidimensionnel

        """
        pass

    def to_flat(self, multi: Tuple[int]) -> int :
        """
            Indice multidimensionnel -> identifiant plat 

        """
        pass
    
    def iter_all_symbolic_controls(self) -> Iterator[int]:
        """
            Itérateur parcourant l'ensemble fini des commandes symboliques discrètes Σ.
            Σ étant de petite taille, l'itération se fait une commande à la fois.

            Retour: 
            ---------------------------------------------------------------------------
            Iterator[int] :Les identifiants plats de toutes les commandes symboliques.

        """
        pass
