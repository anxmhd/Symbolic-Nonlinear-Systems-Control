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
    Forme : (nb_states, nb_controls)."""
    return abstraction.pre(R)


def compute_safety_domain(
    abstraction: SymbolicAbstraction,
    Q_s: np.ndarray,
    max_iter: int | None = None,
) -> tuple[np.ndarray, int]:
    """Algorithme 1 : R_0 = Q_s ; R_{k+1} = Q_s ∩ Pre(R_k) ; arrêt quand R_{k+1} == R_k.
    Pre(R) = safe_command_mask(abstraction, R).any(axis=1).
    Retourne (R_star, nombre d'itérations)."""

    limit = max_iter if max_iter is not None else abstraction.nb_states + 1
    R = Q_s.copy()
    for k in range(limit):
        R_next = Q_s & safe_command_mask(abstraction, R).any(axis=1)
        if np.array_equal(R_next, R):
            return R, k
        R = R_next
    raise RuntimeError(
        f"Point fixe non atteint après {limit} itérations : vérifier pre() et g()"
    )


def extract_safe_controller(H: np.ndarray, R_star: np.ndarray) -> np.ndarray:
    """h[ξ] = première commande sûre de H[ξ] pour ξ dans R*, -1 ailleurs.
    H = safe_command_mask(abstraction, R_star)."""
    h = H.argmax(axis=1)   # premiere commande sûre (0 si la ligne est toute False)
    h[~R_star] = -1        # hors du domaine sûr ( n'ont aucune commande valable)
    return h


def build_safety_controller(
    abstraction: SymbolicAbstraction,
    Q_s: np.ndarray,
    max_iter: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Enchaîne compute_safety_domain -> safe_command_mask -> extract_safe_controller.
    Retourne (R_star, h)."""

    R_star, iter = compute_safety_domain(abstraction, Q_s, max_iter)
    H = safe_command_mask(abstraction, R_star)
    h = extract_safe_controller(H, R_star)
    return R_star, h

