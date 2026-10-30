# system/base_system.py

from abc import ABC, abstractmethod
import numpy as np


class BaseSystem(ABC):
    """
    Interface commune des modèles de systèmes utilisés dans le projet.

    Convention pour les tableaux :
        Utiliser des tableaux NumPy contenant des flottants.
        Un vecteur a la forme (n,), et non (n, 1).

    Convention pour les bornes :
        Chaque ligne contient [minimum, maximum] pour une composante.
    """

    def __init__(self,tau: float,state_bounds: np.ndarray,control_bounds: np.ndarray,disturbance_bounds: np.ndarray,periodic_dims: tuple[int, ...] = ()) -> None:
        """
        Paramètres
        ----------
        tau :
            Durée entre deux mises à jour de l'état, en secondes.
            Doit être finie et strictement positive.

        state_bounds :
            Forme (n, 2), où n est la dimension de l'état.
            Définit le domaine utilisé pour construire la grille.
            Ces bornes ne doivent PAS servir à limiter artificiellement
            les positions calculées.

        control_bounds :
            Forme (m, 2), où m est la dimension de la commande.

        disturbance_bounds :
            Forme (d, 2), où d est la dimension de la perturbation.

        periodic_dims :
            Indices des coordonnées périodiques.
            Exemple : (2,) signifie que la troisième coordonnée
            est périodique.

        Retour
        ------
        None.

        À prévoir dans l'implémentation :
            Vérifier les dimensions, que les valeurs sont finies,
            et que minimum <= maximum pour chaque ligne de bornes.
        """

        # Les copies empêchent les modifications des tableaux fournis
        # de modifier accidentellement les paramètres du modèle.
        self.tau = float(tau)
        self.state_bounds = np.array(state_bounds, dtype=float, copy=True)
        self.control_bounds = np.array(control_bounds, dtype=float, copy=True)
        self.disturbance_bounds = np.array(disturbance_bounds, dtype=float, copy=True)
        self.periodic_dims = tuple(periodic_dims)

    @abstractmethod
    def step(self,x: np.ndarray,u: np.ndarray,w: np.ndarray | None = None) -> np.ndarray:
        """
        Calculer l'état après une période d'échantillonnage.

        Entrées :
            x : état courant, de forme (n,).
            u : commande appliquée, de forme (m,).
            w : perturbation, de forme (d,).
                None signifie une perturbation nulle.

        Retour :
            Un NOUVEAU tableau de flottants de forme (n,).

        Contrat :
            - Ne pas modifier les tableaux reçus en entrée.
            - Ne pas générer de perturbations aléatoires ici.
            - Ne pas ramener artificiellement les positions dans les bornes de l'espace d'état.
            - Lever ValueError si les formes sont incorrectes,
              si les valeurs ne sont pas finies, ou si les commandes
              ou perturbations sont hors de leurs bornes.

        Chaque classe fille implémente sa propre formule de mouvement.
        """
        raise NotImplementedError

    @abstractmethod
    def growth_bounds(self,u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Fournir les bornes d'incertitude pour une commande fixée.

        Entrée :
            u : commande, de forme (m,).

        Retour :
            (Dx, Dw), un tuple de deux tableaux de flottants.
            Dx est de forme (n, n). ( incertitude sur chaque composante)
            Dw est de forme (n, d).

        Utilisé par abstraction.py pour déterminer quelles cellules le robot pourrait atteindre 
        depuis une cellule donnée, avec une commande fixée, en tenant compte de tous les états de départ 
        et de toutes les perturbations possibles.

        
        Une commande invalide doit provoquer une ValueError.
        """
        raise NotImplementedError
