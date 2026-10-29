"""synthesis/safety.py

Synthèse de contrôleur de sûreté (S7467, section 2.1).

Interface avec symbolic/abstraction.py (SymbolicAbstraction) :
    - abstraction.nb_states, abstraction.nb_controls : cardinaux de Ξ et Σ.
    - abstraction.pre(target) -> valid, masque bool de forme (nb_states, nb_controls) :
          valid[ξ, σ] = True si TOUS les successeurs de (ξ, σ) sont dans `target`
          et si le couple n'est pas en overflow (il ne sort pas de X).
      C'est exactement la condition de sûreté d'une commande : on ne la réécrit pas ici.
    - abstraction.g(ξ, σ) : successeurs d'un seul couple (réservé aux tests/débogage).

Conventions :
    - Pas d'état "hors de X" : les sorties de X sont gérées par `overflow` dans l'abstraction.
    - Un ensemble d'états (R, Q_s, R*) est un vecteur booléen de forme (nb_states,).
    - H (commandes sûres) est un masque bool de forme (nb_states, nb_controls) : H[ξ, σ].
    - h (contrôleur) est un tableau d'entiers de forme (nb_states,), -1 hors de R*.
"""
from __future__ import annotations

import numpy as np

from symbolic.abstraction import SymbolicAbstraction


def safe_command_mask(abstraction: SymbolicAbstraction, R: np.ndarray) -> np.ndarray:
    """H[ξ, σ] = True si la commande σ, appliquée depuis ξ, garde tous les successeurs dans R.
    Forme : (nb_states, nb_controls).
    Indication : délègue à abstraction.pre(R)."""
    ...


def compute_safety_domain(
    abstraction: SymbolicAbstraction,
    Q_s: np.ndarray,
    max_iter: int | None = None,
) -> tuple[np.ndarray, int]:
    """Algorithme 1 : R_0 = Q_s ; R_{k+1} = Q_s ∩ Pre(R_k) ; arrêt quand R_{k+1} == R_k.
    Pre(R) = safe_command_mask(abstraction, R).any(axis=1).
    Retourne (R_star, nombre d'itérations)."""
    ...


def extract_safe_controller(H: np.ndarray, R_star: np.ndarray) -> np.ndarray:
    """h[ξ] = première commande sûre de H[ξ] (argmax sur l'axe des commandes) pour ξ dans R*,
    -1 ailleurs. H = safe_command_mask(abstraction, R_star).
    Attention : argmax d'une ligne toute False renvoie 0, d'où le masquage par R_star."""
    ...


def build_safety_controller(
    abstraction: SymbolicAbstraction,
    Q_s: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Enchaîne compute_safety_domain -> safe_command_mask -> extract_safe_controller.
    Retourne (R_star, h)."""
    ...


# --- Optionnel (section 2.1.3), à faire une fois le reste validé ---

def optimize_safe_controller(
    abstraction: SymbolicAbstraction,
    H: np.ndarray,
    j_symb: np.ndarray,
    lam: float,
    horizon: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Programmation dynamique min-max (éq. 11-13) parmi les commandes de H.
    j_symb : coût symbolique, forme (nb_states, nb_controls). Retourne (J0, h_star)."""
    ...