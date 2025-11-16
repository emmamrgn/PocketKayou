# 🤖 PocketKayou

Bot Discord multifonctions avec surveillance de streams, jeux interactifs et gestion de serveur.

## 📋 Fonctionnalités

### 🎮 Jeux
- **Wordle en français** : Jeu de devinettes de mots de 5 lettres
  - `/wordle` - Démarrer une nouvelle partie
  - `/guess <mot>` - Proposer un mot
  - `/abandon` - Abandonner la partie en cours

### 🎥 Surveillance de Streams
- **Twitch** : Notifications automatiques quand le streamer est en direct
- **TikTok** : Surveillance des nouvelles vidéos TikTok

### 🎯 Valorant
- **Statistiques de rang** : Affichage des statistiques Valorant d'un joueur
  - `k?rank <username#tag>` - Afficher le rang d'un joueur

### 🛠️ Modération
- **Suppression de messages** : Commande réservée aux administrateurs
  - `/clear <nombre>` - Supprimer entre 1 et 100 messages

### 📊 Utilitaires
- `k?ping` - Vérifier la latence du bot
- `k?aide` - Afficher le message d'aide

## 🚀 Installation

### Prérequis
- Python 3.12+
- Un bot Discord avec les intents activés
- Compte Twitch Developer (pour surveillance Twitch)

### Installation des dépendances

```bash
# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement virtuel
source .venv/bin/activate  

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration

1. Créer un fichier `global_var.py` à la racine du projet :

```python
# Discord
TOKEN = "votre_token_discord"

# Twitch
TWITCH_CLIENT_ID = "votre_client_id_twitch"
TWITCH_CLIENT_SECRET = "votre_client_secret_twitch"
TWITCH_USERNAME = "nom_du_streamer"
TWITCH_NOTIFICATION_CHANNEL_ID = "ID du channel discord pour les notifs"   
TWITCH_ROLE_ID = "ID du rôle à mentionner" 

# TikTok
TIKTOK_USERNAME = "nom_utilisateur_tiktok"
TIKTOK_NOTIFICATION_CHANNEL_ID = "ID du channel discord pour les notifs" 

# Logs
CHANNEL_ID = "ID du channel discord pour les logs" 
```

2. Configurer les intents du bot Discord :
   - Aller sur le [Discord Developer Portal](https://discord.com/developers/applications)
   - Activer les intents : **Presence Intent**, **Server Members Intent**, **Message Content Intent**

3. Inviter le bot avec les permissions nécessaires :
   - `Read Messages/View Channels`
   - `Send Messages`
   - `Embed Links`
   - `Read Message History`
   - `Manage Messages` (pour /clear)
   - `Mention Everyone` (optionnel, pour les notifications)

## 🎯 Utilisation

### Démarrer le bot

```bash
python main.py
```

### Commandes disponibles

#### Commandes Slash (/)
- `/wordle` - Démarrer une partie de Wordle
- `/guess <mot>` - Proposer un mot (5 lettres)
- `/abandon` - Abandonner la partie
- `/clear <nombre>` - Supprimer des messages (admin uniquement)

#### Commandes Préfixe (k?)
- `k?ping` - Vérifier la latence
- `k?aide` - Afficher l'aide
- `k?rank <username#tag>` - Statistiques Valorant

## 📁 Structure du projet

```
PocketKayou/
├── main.py                 # Point d'entrée du bot
├── global_var.py          # Configuration (à créer)
├── log.py                 # Système de logging
├── requirements.txt       # Dépendances Python
├── games/
│   ├── __init__.py
│   ├── dico.py           # Dictionnaire français (1264 mots)
│   └── wordle_game.py    # Logique du jeu Wordle
├── twitch/
│   ├── __init__.py
│   └── stream_monitor.py # Surveillance Twitch
├── tiktok/
│   ├── __init__.py
│   └── tiktok_monitor.py # Surveillance TikTok
└── valorant/
    ├── __init__.py
    └── rank_ctrl.py      # API Valorant
```

## 🔧 Technologies utilisées

- **discord.py** - Bibliothèque Discord
- **aiohttp** - Requêtes HTTP asynchrones
- **beautifulsoup4** - Web scraping pour TikTok

## 📝 Notes

- Le dictionnaire Wordle contient **1264 mots français uniques** de 5 lettres
- Les surveillances Twitch et TikTok se lancent automatiquement au démarrage
- Les commandes slash sont synchronisées automatiquement au démarrage
- Les logs sont envoyés dans le canal configuré

## 👤 Auteur

@[emmamrgn](https://github.com/emmamrgn)

## 📄 Licence

Ce projet est à usage personnel.

--- 