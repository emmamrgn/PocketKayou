# PocketKayou

Un petit bot Discord orienté gestion de rôles (basé sur des subs) et utilitaires pour Valorant.

## Description

Le bot effectue plusieurs tâches :

- Gère l'attribution et le retrait des rôles en fonction d'abonnements (subs) à des chaînes Twitch (rôles définis dans `global_var.py`).
- Fournit une commande `k!rank` qui récupère et affiche le rang Valorant d'un joueur via une API tierce (utilise `valorant.py`).
- Commandes utilitaires : `k!ping` pour vérifier la latence et `k!aide` pour afficher l'aide.
- Journalise les actions importantes (changement de rôles, mise en ligne du bot, vérifications) dans un canal Discord (via `log_discord.py`).

## Prérequis

- Python 3.8+
- Les dépendances listées dans `requirements.txt` : `aiohttp`, `discord.py`.
- Un token de bot Discord (voir section Configuration).

## Installation

1. Clonez le dépôt et entrez dans le dossier :

	git clone <repo-url>
	cd PocketKayou

2. Installez les dépendances :

	python -m pip install -r requirements.txt

3. Configurez les variables dans `global_var.py` ou, de préférence, remplacez l'usage direct du token par une variable d'environnement (voir sécurité).

## Configuration

Les constantes importantes sont définies dans `global_var.py` :

- `LES_SUBS`, `SUB_EMMA`, `SUB_RO`, `SUB_ALL` : IDs des rôles utilisés par le bot.
- `CHANNEL_ID`, `CHANNEL_LOG_ID` : ID(s) du/des canal(aux) de log.
- `TOKEN` : token du bot Discord (NE JAMAIS partager ce token publiquement).

Important — Sécurité :

- Le dépôt contient actuellement un token en clair dans `global_var.py`. Changez-le immédiatement et utilisez une variable d'environnement à la place. Exemple :

  export DISCORD_TOKEN="votre_token_ici"

  puis dans le code remplacer `TOKEN = ...` par :

  import os
  TOKEN = os.environ.get('DISCORD_TOKEN')

## Utilisation

Lancez le bot :

	python main.py

Commandes disponibles (préfixe `k!`) :

- `k!aide` : affiche l'aide et les commandes disponibles.
- `k!ping` : répond avec la latence du bot.
- `k!rank username#tag` : récupère le rang Valorant pour `username#tag`. Le format accepte aussi `username tag` (séparé par un espace).
- `k!verifier_roles [membre]` : (nécessite la permission `manage_roles`) déclenche une vérification manuelle des rôles pour le membre spécifié ou pour l'émetteur.

Fonctionnement des rôles :

- `les_subs` : attribué si un membre a l'un des rôles `SUB_EMMA` ou `SUB_RO`.
- `super_subs` : attribué si un membre a à la fois `SUB_EMMA` et `SUB_RO`.

Événements automatisés :

- À la mise en ligne (`on_ready`) le bot parcourt les membres du serveur et exécute la vérification des rôles.
- À l'arrivée d'un nouveau membre (`on_member_join`) ou à toute modification de rôles (`on_member_update`) la vérification est relancée pour ce membre.

## Journalisation

Les fonctions de `log_discord.py` envoient des messages dans le canal défini par `CHANNEL_ID`. Si le canal est introuvable, le bot affiche un message dans la console.

## Remarques importantes et améliorations suggérées

- NE laissez jamais le token du bot en clair dans le dépôt : révoquez le token trouvé et en générez un nouveau si ce n'est pas déjà fait.
- Passer à l'utilisation de variables d'environnement pour les secrets.
- Ajouter une gestion d'exceptions et des tests pour la partie réseau (requests vers l'API Valorant).
- Documenter les rôles attendus et fournir un petit script d'initialisation pour créer/assigner les IDs sur un serveur de test.

## Développeur

Projet initial de emmamrgn. Contact/maintien : voir l'historique du dépôt.

