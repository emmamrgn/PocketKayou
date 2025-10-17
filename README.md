# PocketKayou

## Description

Un petit bot Discord orienté utilitaires pour Valorant.

## Fonctionnalités

- Réponse à une commande qui renvoie le rang du joueur.
- Journalisation des changements de rôles, du statut du bot et de la vérification des membres.
- Commande de vérification manuelle des rôles.
- Commande ping simple pour vérifier la latence du bot.

## Prérequis

- Python 3.8+
- Les dépendances listées dans `requirements.txt`
- Un token de bot Discord (voir section Configuration).

## Installation

1. Clonez le dépôt et entrez dans le dossier :

	`git clone <repo-url>
	cd PocketKayou`

2. Installez les dépendances :

	`python -m pip install -r requirements.txt`

3. Configurez les variables dans `global_var.py` ou, de préférence, remplacez l'usage direct du token par une variable d'environnement (voir sécurité).

## Utilisation

Lancez le bot :

	python main.py

#### Commandes disponibles (préfixe `k!`) :

- `k!aide` : affiche l'aide et les commandes disponibles.
- `k!ping` : répond avec la latence du bot.
- `k!rank username#tag` : récupère le rang Valorant pour `username#tag`. Le format accepte aussi `username tag` (séparé par un espace).

## Journalisation

Le bot journalise les événements importants tels que les appels aux commandes, les changements de rôles, le statut du bot et la vérification des membres dans un canal Discord spécifié.

Événements automatisés :

- À la mise en ligne (`on_ready`) le bot parcourt les membres du serveur et exécute la vérification des rôles.
- À l'arrivée d'un nouveau membre (`on_member_join`) ou à toute modification de rôles (`on_member_update`) la vérification est relancée pour ce membre.


## Développeur
Ce projet a été développé par [emmamrgn](https://github.com/emmamrgn).
