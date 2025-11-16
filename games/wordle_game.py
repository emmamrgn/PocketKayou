import discord
import random
from typing import Dict, Optional
import unicodedata

class WordleGame:
    def __init__(self):
        self.active_games: Dict[int, dict] = {}  # user_id: game_data
        
        # Liste de mots français de 5 lettres
        self.word_list = [
            "ABOUT", "ACIER", "ACTIF", "ADDON", "ADIEU", "ADMIN", "AGENT", "AIDER",
            "AIGLE", "AIMER", "AINSI", "ALBUM", "ALORS", "AMOUR", "ANIME", "APRES",
            "ARBRE", "ARCHE", "ARGENT", "ARMER", "ASILE", "ATLAS", "ATOME", "AUSSI",
            "AUTRE", "AVANT", "AVOIR", "BADGE", "BAGUE", "BARRE", "BASIL", "BASSE",
            "BATON", "BELLE", "BLANC", "BLOND", "BOIRE", "BOITE", "BOMBE", "BONUS",
            "BOTTE", "BOULE", "BRAVE", "BRUIT", "CABLE", "CADRE", "CAFE", "CALME",
            "CANAL", "CANNE", "CARTE", "CAUSE", "CENTS", "CHAMP", "CHANT", "CHAOS",
            "CHAUD", "CHIEN", "CHOSE", "CHUTE", "CIRCE", "CIVIL", "CLAIR", "CLASSE",
            "CLEFS", "COEUR", "COINS", "COLLE", "CONTE", "CORPS", "COTES", "COUPE",
            "COURS", "COURT", "CRIME", "CRUEL", "CYCLE", "DANSE", "DEBUT", "DECKH",
            "DENSE", "DEPOT", "DROIT", "ECHEC", "ECOLE", "ECRIRE", "EFFET", "ELEVE",
            "EMBLA", "EPAIS", "EPICE", "ERREUR", "ESPACE", "ESPRIT", "ESSAI", "ETAGE",
            "ETAPE", "ETATS", "ETUDE", "EXACT", "FACILE", "FAIRE", "FAUSSE", "FETES",
            "FEUIL", "FICHE", "FINAL", "FIXER", "FLAMME", "FLEUR", "FOIRE", "FORCE",
            "FORME", "FORTE", "FOULE", "FRUIT", "FUTUR", "GARDE", "GELER", "GENRE",
            "GLACE", "GLOBE", "GRACE", "GRAIN", "GRAND", "GRAVE", "GRILL", "GRISE",
            "GROS", "GROUPE", "GUIDE", "HAUTE", "HEROS", "HEURE", "HOMME", "HONET",
            "HUILE", "IDEES", "IMAGE", "INDEX", "ISSUE", "JETON", "JEURE", "JOINS",
            "JOUER", "JOURS", "JUSTE", "LANCE", "LARGE", "LASER", "LIBRE", "LIGNE",
            "LIVRE", "LOGIC", "LONGS", "LOURD", "LUEUR", "LUTTE", "MAGIE", "MAIRE",
            "MAJOR", "MAMAN", "MARCH", "MASSE", "MATCH", "MATEO", "MENUS", "METAL",
            "MICRO", "MIEUX", "MILAN", "MILLE", "MINES", "MIXER", "MODELS", "MOINS",
            "MONDE", "MONTE", "MORAL", "MORTE", "MOTIF", "MOYEN", "MUETS", "MURAL",
            "NAGER", "NEIGE", "NEUVE", "NOBLE", "NOIRE", "NORME", "NOTRE", "NUAGE",
            "OCEAN", "OFFRE", "ORDRE", "OUEST", "OUVRE", "PAIRE", "PANEL", "PAPAS",
            "PARCH", "PARIS", "PARLE", "PARTS", "PASSE", "PEINE", "PELLE", "PENSE",
            "PERTE", "PETIT", "PHOTO", "PIECE", "PISTE", "PLACE", "PLAGE", "PLANE",
            "PLATE", "PLEIN", "POCHE", "POEME", "POINT", "POKER", "POMME", "PORTE",
            "POSER", "POSTE", "POUND", "POWER", "PRETS", "PRIME", "PRISE", "PROCE",
            "PROFIT", "QUEUE", "QUITE", "RADIO", "RAIES", "RAPID", "RAYON", "RECIT",
            "REGAL", "REINE", "RESTE", "RICHE", "RIDER", "RIFLE", "RIGID", "RISKY",
            "RIVAL", "ROCHE", "ROMAN", "RONDE", "ROUGE", "ROUTE", "ROYAL", "RUGBY",
            "RUNES", "SABLE", "SAINE", "SAINT", "SALLE", "SAPIN", "SAUCE", "SCENE",
            "SERRE", "SIGNE", "SINGE", "SMOKE", "SOBRE", "SOLDE", "SOLID", "SONDE",
            "SORTE", "SORTS", "SOUPE", "SPIKE", "SPORT", "STAFF", "STAGE", "STAND",
            "STARS", "STYLE", "SUCRE", "SUITE", "SUPER", "TABLE", "TACHE", "TAPIS",
            "TARDE", "TARTE", "TASSE", "TEMPS", "TERME", "TERRE", "TESTE", "TETES",
            "TEXTE", "THEME", "TIGRE", "TITRE", "TOMBE", "TORCH", "TOTAL", "TOUCH",
            "TOURS", "TRACE", "TRAIN", "TRAIT", "TRAME", "TRASH", "TRIAL", "TRIBE",
            "TROIS", "TROOP", "TRUST", "TUERC", "TUEUR", "UNITE", "USAGE", "USINE",
            "UTILE", "VAGUE", "VALID", "VALSE", "VALUE", "VASTE", "VAULT", "VENUE",
            "VERRE", "VERSO", "VERTS", "VIBRE", "VIEUX", "VIGIL", "VILLE", "VIRUS",
            "VISER", "VISIT", "VITAE", "VIVANT", "VIVRE", "VOIES", "VOIRE", "VOLER",
            "VOLTE", "VOTES", "VOTRE", "WAGON", "YACHT", "YUZUS",  "ZONES", "ZOOMS"
        ]
    
    def normalize_text(self, text: str) -> str:
        """Normalise le texte en retirant les accents et en mettant en majuscule"""
        text = text.upper()
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
    
    def start_game(self, user_id: int) -> str:
        """Démarre une nouvelle partie de Wordle"""
        word = random.choice(self.word_list)
        self.active_games[user_id] = {
            'word': word,
            'attempts': [],
            'max_attempts': 6,
            'won': False
        }
        return word
    
    def get_game(self, user_id: int) -> Optional[dict]:
        """Récupère la partie en cours d'un joueur"""
        return self.active_games.get(user_id)
    
    def end_game(self, user_id: int):
        """Termine la partie d'un joueur"""
        if user_id in self.active_games:
            del self.active_games[user_id]
    
    def check_guess(self, user_id: int, guess: str) -> tuple:
        """
        Vérifie une tentative et retourne (valid, result, game_over, won)
        result est une liste de tuples (lettre, status) où status est:
        - 'correct': lettre correcte à la bonne position (vert)
        - 'present': lettre correcte mais mauvaise position (jaune)
        - 'absent': lettre absente (gris)
        """
        game = self.get_game(user_id)
        if not game:
            return False, None, True, False
        
        guess = self.normalize_text(guess)
        
        # Vérifier la longueur
        if len(guess) != 5:
            return False, None, False, False
        
        # Vérifier que c'est un mot valide (optionnel)
        if guess not in self.word_list:
            return False, None, False, False
        
        target = game['word']
        result = []
        
        # Compter les lettres dans le mot cible
        target_counts = {}
        for letter in target:
            target_counts[letter] = target_counts.get(letter, 0) + 1
        
        # Premier passage: marquer les lettres correctes
        guess_status = [''] * 5
        for i, letter in enumerate(guess):
            if letter == target[i]:
                guess_status[i] = 'correct'
                target_counts[letter] -= 1
        
        # Deuxième passage: marquer les lettres présentes
        for i, letter in enumerate(guess):
            if guess_status[i] == '':
                if letter in target_counts and target_counts[letter] > 0:
                    guess_status[i] = 'present'
                    target_counts[letter] -= 1
                else:
                    guess_status[i] = 'absent'
        
        # Créer le résultat
        for letter, status in zip(guess, guess_status):
            result.append((letter, status))
        
        # Ajouter la tentative
        game['attempts'].append((guess, result))
        
        # Vérifier si gagné
        won = guess == target
        if won:
            game['won'] = True
        
        # Vérifier si fin de partie
        game_over = won or len(game['attempts']) >= game['max_attempts']
        
        return True, result, game_over, won
    
    def create_board_embed(self, user_id: int, user_name: str, last_result=None, game_over=False, won=False, invalid_word=False) -> discord.Embed:
        """Crée l'embed pour afficher le plateau de jeu"""
        game = self.get_game(user_id)
        
        if invalid_word:
            embed = discord.Embed(
                title="❌ Mot invalide",
                description="Le mot doit contenir exactement 5 lettres et être dans la liste des mots valides.",
                color=discord.Color.red()
            )
            return embed
        
        if not game:
            embed = discord.Embed(
                title="❌ Aucune partie en cours",
                description="Utilisez `/wordle` pour commencer une nouvelle partie !",
                color=discord.Color.red()
            )
            return embed
        
        # Emojis pour les lettres
        emoji_map = {
            'correct': '🟩',
            'present': '🟨',
            'absent': '⬛'
        }
        
        # Construire le plateau
        board = ""
        for attempt, result in game['attempts']:
            line = ""
            for letter, status in result:
                line += emoji_map[status]
            board += line + f"  **{attempt}**\n"
        
        # Ajouter les lignes vides restantes
        remaining = game['max_attempts'] - len(game['attempts'])
        for _ in range(remaining):
            board += "⬜⬜⬜⬜⬜\n"
        
        # Créer l'embed
        if game_over:
            if won:
                title = f"🎉 Bravo {user_name} !"
                description = f"Vous avez trouvé le mot en {len(game['attempts'])} essai(s) !"
                color = discord.Color.green()
            else:
                title = f"😢 Perdu {user_name}"
                description = f"Le mot était : **{game['word']}**"
                color = discord.Color.red()
        else:
            title = f"🎮 Wordle - {user_name}"
            description = f"Essai {len(game['attempts'])}/{game['max_attempts']}"
            color = discord.Color.blue()
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        
        embed.add_field(name="Plateau", value=board, inline=False)
        
        if not game_over:
            embed.add_field(
                name="Comment jouer ?",
                value="Utilisez `/guess <mot>` pour proposer un mot de 5 lettres\n"
                      "🟩 = Bonne lettre, bonne position\n"
                      "🟨 = Bonne lettre, mauvaise position\n"
                      "⬛ = Lettre absente",
                inline=False
            )
        
        embed.set_footer(text="Wordle Français")
        
        return embed

# Instance globale du jeu
wordle_game = WordleGame()
