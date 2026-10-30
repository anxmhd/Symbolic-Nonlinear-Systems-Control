# system/unicycle_robot.py

import numpy as np
from .base_system import BaseSystem


class UnicycleRobot(BaseSystem):
    """
    Modèle du robot correspondant à l'équation (16) de l'article.

    État :
        x = [px, py, theta], de forme (3,)
        px, py : en mètres
        theta : en radians

    Commande :
        u = [v, omega], de forme (2,)
        v : en mètres/seconde
        omega : en radians/seconde

    Perturbation :
        w = [wx, wy, wtheta], de forme (3,)
        wx, wy : en mètres/seconde
        wtheta : en radians/seconde
    """

    def __init__(self, tau: float = 1.0) -> None:
        """
        Créer le robot avec les valeurs des paramètres de l'article.

        tau :
            Période d'échantillonnage en secondes ; vaut 1.0 par défaut.

        Retour :
            None.

        La grille, les obstacles, la cible et l'état initial
        sont configurés dans d'autres modules.
        """

        state_bounds = np.array([
            [0.0, 10.0],        # Position horizontale
            [0.0, 10.0],        # Position verticale
            [-np.pi, np.pi]     # Orientation
        ])

        control_bounds = np.array([
            [0.25, 1.0],       # Vitesse d'avancement
            [-1.0, 1.0]        # Vitesse de rotation
        ])

        disturbance_bounds = np.array([
            [-0.05, 0.05],     # Dérive horizontale
            [-0.05, 0.05],     # Dérive verticale
            [-0.05, 0.05]      # Dérive angulaire
        ])

        # La classe parent stocke ces paramètres communs.
        super().__init__(
            tau=tau,
            state_bounds=state_bounds,
            control_bounds=control_bounds,
            disturbance_bounds=disturbance_bounds,
            periodic_dims=(2,)
        )

    def step(self,x: np.ndarray,u: np.ndarray,w: np.ndarray | None = None) -> np.ndarray:
        """
        Appliquer l'équation (16) sur une période d'échantillonnage.

        Entrées :
            x : [px, py, theta], de forme (3,).
            u : [v, omega], de forme (2,).
            w : [wx, wy, wtheta], de forme (3,).
                Si None, utiliser [0.0, 0.0, 0.0].

        Calcul :
            px_next = px + tau * (v*cos(theta) + wx)
            py_next = py + tau * (v*sin(theta) + wy)
            theta_next = wrap_angle(
                theta + tau * (omega + wtheta)
            )

        Retour :
            NOUVEAU tableau de flottants :
            [px_next, py_next, theta_next].
            Forme : (3,).
            Angle retourné : dans [-pi, pi).

        Important :
            - Les deux mises à jour de position utilisent
              la valeur INITIALE de theta.
            - Retourner les positions calculées même si elles sortent
              du domaine. Les autres modules détectent et traitent
              les sorties dangereuses.
            - Aucune vérification d'obstacles ni sélection
              de commande ici.
            - Respecter le contrat de validation de BaseSystem.
        """
        raise NotImplementedError

    def growth_bounds(self,u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """
        Retourner les bornes nécessaires au module d'abstraction.

        Entrée :
            u = [v, omega], de forme (2,).

        Retour :
            (Dx, Dw) : deux tableaux de flottants de forme (3, 3).

        Matrices :
            Dx = [[1, 0, tau*abs(v)],
                  [0, 1, tau*abs(v)],
                  [0, 0, 1]]

            Dw = tau * matrice_identite_de_taille_3

        Signification :
            Dx borne l'effet de l'incertitude sur l'état initial.
            Dw borne l'effet des perturbations.

        IMPORTANT POUR L'ÉQUIPE D'ABSTRACTION :
            Ces bornes s'appliquent avant la normalisation de l'angle.
            Traiter l'intervalle angulaire obtenu comme périodique :
            le découper s'il franchit la frontière -pi/pi.
            S'il couvre un tour complet, inclure toutes les orientations.
            Ne pas simplement normaliser ses deux extrémités.

        Une commande invalide doit provoquer une ValueError.
        """
        raise NotImplementedError

    @staticmethod
    def wrap_angle(theta: float) -> float:
        """
        Exprimer un angle dans l'intervalle [-pi, pi).

        Entrée :
            Un angle fini en radians.

        Retour :
            Un float Python représentant la même direction.

        Formule :
            ((theta + pi) % (2*pi)) - pi

        Cette méthode normalise un seul angle,
        pas un intervalle d'angles.
        """
        raise NotImplementedError
