"""
Synthèse d'un contrôleur d'atteignabilité sur le modèle symbolique.
Référence : papier, section 2.2.1, Algorithme 2 + Théorème 4.

"""

import numpy as np
from abstraction import SymbolicAbstraction




class ReachabilitySynthesis:
    """
    Synthèse d'un contrôleur d'atteignabilité (Algorithme 2 + Théorème 4).

    Cycle d'utilisation typique (depuis main.py) :

        synth = ReachabilitySynthesis(model, target_mask)
        synth.compute_domain()             # remplit domain, rank, nb_iterations
        synth.synthesize_controller()      # remplit controller
        h = synth.controller               # np.ndarray (nb_states,)


    Attributs publics (remplis par compute_domain) :
        - domain         : StateMask  (R*, masque booléen)
        - rank           : Rank       (k(ξ), -1 si ξ ∉ R*)
        - controller     : Controller (h(ξ), -1 si ξ ∉ R*)
        - nb_iterations  : int        (nombre de couches calculées)
    """

    # -----------------------------------------------------------------------
    # Construction
    # -----------------------------------------------------------------------
    def __init__(self, model:SymbolicAbstraction , target: np.ndarray) -> None: # target : State Mask 
        """
        Mémorise le modèle et la cible Q_a, vérifie la cohérence
        (target.shape == (nb_states,), target.dtype == bool), et initialise les
        attributs de sortie : domain et controller à des masques vides, rank à -1,
        nb_iterations à 0.

        Variables :
            - model (SymbolicAbstraction) : modèle symbolique déjà construit par
              build() ; doit exposer nb_states, nb_controls, overflow, indptr,
              indices et Pre(target).
            - target (np.ndarray) : masque booléen de Q_a ⊆ Ξ, de forme
              (nb_states,).
        """
        self.model = model 
        self.target= target
        self.domain = np.zeros(model.nb_states, dtype=bool)
        self.controller = np.full(model.nb_states,-1, dtype=int)
        self.rank = np.full(model.nb_states, -1, dtype=int)
        self.nb_iterations = 0 


    # -----------------------------------------------------------------------
    # Algorithme 2 : domaine d'atteignabilité
    # -----------------------------------------------------------------------
    def compute_domain(self) -> np.ndarray:     
        """
        Algorithme 2 :
            R_0 = Q_a
            R_{k+1} = Q_a ∪ Pre(R_k)
            jusqu'à R_{k+1} = R_k.  R* = R_k.

        Remplit self.domain, self.rank, self.nb_iterations . Renvoie aussi self.domain pour
        permettre l'enchaînement `domain = synth.compute_domain()`.

        Interprétation de R_k :
            États depuis lesquels on peut atteindre Q_a en AU PLUS k pas.

        Point fixe :
            Ξ fini + suite croissante ⇒ point fixe en ≤ |Ξ \\ Q_a| + 1 itérations.

        Paramètres :
            -
        Retour :
            - StateMask : R* (masque booléen). Tout False si Q_a vide ou
              inatteignable : pas d'exception.
        """
        self.domain= self.target.copy()
        self.rank = np.full(self.model.nb_states, -1, dtype=int)
        self.rank[self.target]=0
        while True:
            pre_states = self.model.pre(self.domain).any(axis=1) 
            newly= pre_states & ~self.domain 
            if not newly.any(): 
                break 
            self.domain = self.domain | newly 
            self.nb_iterations+=1 
            self.rank[newly] =self.nb_iterations 
        return self.domain 

        


        

    # -----------------------------------------------------------------------
    # Théorème 4 : extraction du contrôleur statique
    # -----------------------------------------------------------------------
    def synthesize_controller(self) -> np.ndarray:
        """
        Théorème 4 :
            extraction du contrôleur statique h : R* → Σ tel que, pour
            tout k ∈ ℕ et tout ξ ∈ R_{k+1}, ∅ ≠ g(ξ, h(ξ)) ⊆ R_k (Q_a est atteint
            en au plus rank(ξ) pas). 
        La condition est vérifiée sans stocker les couches R_k via un critère 
        équivalent calculé en un seul passage sur le CSR : 
        succ_rank_max[ξ, σ] < rank(ξ) pour rank(ξ) ≥ 1, 
        succ_rank_max[ξ, σ] <nb_states pour rank(ξ) = 0. 
        Parmi les commandes admissibles, la première(indice minimal) est retenue.
        Utilisation : 
            après compute_domain() (appelé si nécessaire) ; remplit
            controller et le renvoie.

        Retourne :
            - controller (np.ndarray) : Commandes h(ξ), de forme (nb_states,), type
            int, -1 si ξ ∉ R*
        """
        ...
