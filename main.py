import discord
from discord import app_commands
from discord.ext import commands
import re

from valorant.rank_ctrl import get_valorant_rank, create_rank_embed
from twitch import TwitchMonitor
from tiktok import TikTokMonitor
from games.wordle_game import wordle_game
from log import *
from global_var import *

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='k?', intents=intents)

# Initialiser le moniteur Twitch
twitch_monitor = TwitchMonitor(
    bot=bot,
    client_id=TWITCH_CLIENT_ID,
    client_secret=TWITCH_CLIENT_SECRET,
    twitch_username=TWITCH_USERNAME,
    notification_channel_id=TWITCH_NOTIFICATION_CHANNEL_ID,
    role_id=TWITCH_ROLE_ID
)

# Initialiser le moniteur TikTok
tiktok_monitor = TikTokMonitor(
    bot=bot,
    tiktok_username=TIKTOK_USERNAME,
    notification_channel_id=TIKTOK_NOTIFICATION_CHANNEL_ID
)

@bot.event
async def on_ready():
    await log.log_bot_ready(bot)
    print("valorant-bot is online and ready.")

@bot.command()
async def ping(ctx):
    print("k!ping command executed by : ", ctx.author)
    response = f"Pong! ``{round(bot.latency * 1000)}ms``"
    await ctx.send(response)
    await log.log_command(ctx, response)

@bot.command()
async def aide(ctx):
    print(f"k!aide command executed by : {ctx.author}")
    embed = discord.Embed(title="Aide valorant-bot", color=discord.Color.blue())
    embed.add_field(name="Préfixe :", value="``k!``")
    embed.add_field(name="Commandes : ", value = "``k!aide`` ``k!ping`` ``k!rank``")
    embed.add_field(name="Informations commandes :", value="", inline=False)
    embed.add_field(name="``k!aide``", value="Afficher ce message d'aide", inline=False)
    embed.add_field(name="``k!ping``", value="Vérifier la latence du bot",inline=False)
    embed.add_field(name="``k!rank username#tag``", value="Afficher le rang Valorant d'un joueur", inline=False)
    await ctx.send(embed=embed)
    await log.log_command(ctx, "k!aide command executed with embed")

@bot.command()
async def rank(ctx, *, username: str = None):
    """Affiche le rang Valorant d'un joueur depuis tracker.gg"""
    print(f"k!rank command executed by: {ctx.author}")
    
    if not username:
        await ctx.send("❌ Veuillez fournir un nom d'utilisateur avec le tag. Exemple: `k!rank emm4#000`")
        return
    
    # Vérifier le format username#tag
    if "#" not in username:
        await ctx.send("❌ Format incorrect. Utilisez: `k!rank username#tag` (ex: `k!rank emm4#000`)")
        return
    
    # Message de chargement
    loading_msg = await ctx.send("🔍 Recherche des informations du joueur...")
    
    try:
        # Récupérer les données
        data = await get_valorant_rank(username)
        
        # Créer et envoyer l'embed
        embed = create_rank_embed(data)
        await loading_msg.edit(content=None, embed=embed)
        
        # Log la commande
        log_msg = f"k!rank executed for {username} - Success: {data['success']}"
        await log.log_command(ctx, log_msg)
        
    except Exception as e:
        await loading_msg.edit(content=f"❌ Erreur lors de la récupération des données: {str(e)}")
        print(f"Error in k!rank command: {e}")

# ===== COMMANDES SLASH WORDLE =====

@bot.tree.command(name="wordle", description="Commencer une nouvelle partie de Wordle en français")
async def wordle_command(interaction: discord.Interaction):
    """Démarre une nouvelle partie de Wordle"""
    user_id = interaction.user.id
    
    # Vérifier si une partie est déjà en cours
    existing_game = wordle_game.get_game(user_id)
    if existing_game:
        await interaction.response.send_message(
            "❌ Vous avez déjà une partie en cours ! Utilisez `/abandon` pour l'abandonner ou `/guess` pour continuer.",
            ephemeral=True
        )
        return
    
    # Démarrer une nouvelle partie
    wordle_game.start_game(user_id)
    embed = wordle_game.create_board_embed(user_id, interaction.user.name)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="guess", description="Proposer un mot pour deviner le Wordle")
@app_commands.describe(mot="Le mot de 5 lettres à proposer")
async def guess_command(interaction: discord.Interaction, mot: str):
    """Propose un mot pour le Wordle"""
    user_id = interaction.user.id
    
    # Vérifier si une partie est en cours
    game = wordle_game.get_game(user_id)
    if not game:
        await interaction.response.send_message(
            "❌ Aucune partie en cours ! Utilisez `/wordle` pour commencer.",
            ephemeral=True
        )
        return
    
    # Vérifier la tentative
    valid, result, game_over, won = wordle_game.check_guess(user_id, mot)
    
    if not valid:
        embed = wordle_game.create_board_embed(user_id, interaction.user.name, invalid_word=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Afficher le résultat
    embed = wordle_game.create_board_embed(user_id, interaction.user.name, result, game_over, won)
    await interaction.response.send_message(embed=embed)
    
    # Si la partie est terminée, la supprimer
    if game_over:
        wordle_game.end_game(user_id)

@bot.tree.command(name="abandon", description="Abandonner la partie de Wordle en cours")
async def abandon_command(interaction: discord.Interaction):
    """Abandonne la partie de Wordle en cours"""
    user_id = interaction.user.id
    
    game = wordle_game.get_game(user_id)
    if not game:
        await interaction.response.send_message(
            "❌ Aucune partie en cours !",
            ephemeral=True
        )
        return
    
    word = game['word']
    wordle_game.end_game(user_id)
    
    embed = discord.Embed(
        title="🏳️ Partie abandonnée",
        description=f"Le mot était : **{word}**",
        color=discord.Color.orange()
    )
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f'🤖 {bot.user} est connecté et prêt!')
    await log_bot_online(bot)
    
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} commandes slash synchronisées")
    except Exception as e:
        print(f"❌ Erreur lors de la synchronisation des commandes: {e}")
    
    # Démarrer la surveillance Twitch
    twitch_monitor.start()
    print("🎥 Surveillance Twitch activée")
    
    # Démarrer la surveillance TikTok
    tiktok_monitor.start()
    print("🎵 Surveillance TikTok activée")
    


bot.run(TOKEN)
