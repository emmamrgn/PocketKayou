import discord
from discord.ext import commands
import re

from valorant import rank_ctrl
import log

from global_var import *
from log_discord import log_role_change, log_bot_online, log_member_verification

# Configuration du bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='k!', intents=intents)

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
async def rank(ctx, *, username_tag):
    print("k!rank command exexuted by : ", ctx.author)
    match = re.match(r"(.+?)#(\w+)", username_tag)
    if match:
        username, tag = match.groups()
    else:
        parts = username_tag.rsplit(' ', 1)
        if len(parts) == 2:
            username, tag = parts
        else:
            response = "Format invalide. Utiliser  ``k!rank username#tag``  ou  ``k!rank username tag``"
            await ctx.send(response)
            await log.log_command(ctx, response)
            return
    controller = rank_ctrl(ctx, username, tag)
    await controller.get_rank()
    response = f"rank data fetched for ``{username}#{tag}``"
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

async def gerer_roles(member):
    """Vérifie et gère l'attribution et le retrait des rôles selon les conditions"""
    # Obtenir les rôles avec gestion d'erreurs améliorée
    role_les_subs = member.guild.get_role(LES_SUBS)
    role_super_subs = member.guild.get_role(SUB_ALL)
    
    if not role_les_subs or not role_super_subs:
        print(f"Erreur critique pour {member.display_name}:")
        if not role_les_subs:
            print(f"- Rôle 'les_subs' (ID: {LES_SUBS}) introuvable")
        if not role_super_subs:
            print(f"- Rôle 'super_subs' (ID: {SUB_ALL}) introuvable")
        return

    # Vérification des rôles avec logging amélioré
    has_sub_emma = any(role.id == SUB_EMMA for role in member.roles)
    has_sub_ro = any(role.id == SUB_RO for role in member.roles)

    # Logging de l'état actuel
    print(f"\nVérification pour {member.display_name}:")
    # print(f"- Sub Emma: {has_sub_emma}")
    # print(f"- Sub Ro: {has_sub_ro}")

    # Gestion du rôle les_subs
    should_have_role_les_subs = has_sub_emma or has_sub_ro
    
    if should_have_role_les_subs and role_les_subs not in member.roles:
        try:
            await member.add_roles(role_les_subs)
            print(f"✅ Rôle 'les_subs' ajouté à {member.display_name}")
            await log_role_change(bot, member, "Ajouté", "les_subs")
        except discord.Forbidden:
            print(f"❌ Erreur de permissions pour ajouter 'les_subs' à {member.display_name}")
        except discord.HTTPException as e:
            print(f"❌ Erreur HTTP pour 'les_subs': {str(e)}")
    elif not should_have_role_les_subs and role_les_subs in member.roles:
        try:
            await member.remove_roles(role_les_subs)
            print(f"🔄 Rôle 'les_subs' retiré de {member.display_name} (conditions non remplies)")
            await log_role_change(bot, member, "Retiré", "les_subs")
        except discord.Forbidden:
            print(f"❌ Erreur de permissions pour retirer 'les_subs' de {member.display_name}")
        except discord.HTTPException as e:
            print(f"❌ Erreur HTTP: {str(e)}")

    # Gestion du rôle super_subs
    should_have_role_super_subs = has_sub_emma and has_sub_ro
    
    if should_have_role_super_subs and role_super_subs not in member.roles:
        try:
            await member.add_roles(role_super_subs)
            print(f"✅ Rôle 'super_subs' ajouté à {member.display_name}")
            await log_role_change(bot, member, "Ajouté", "super_subs")
        except discord.Forbidden:
            print(f"❌ Erreur de permissions pour ajouter 'super_subs' à {member.display_name}")
        except discord.HTTPException as e:
            print(f"❌ Erreur HTTP: {str(e)}")
    elif not should_have_role_super_subs and role_super_subs in member.roles:
        try:
            await member.remove_roles(role_super_subs)
            print(f"🔄 Rôle 'super_subs' retiré de {member.display_name} (conditions non remplies)")
            await log_role_change(bot, member, "Retiré", "super_subs")
        except discord.Forbidden:
            print(f"❌ Erreur de permissions pour retirer 'super_subs' de {member.display_name}")
        except discord.HTTPException as e:
            print(f"❌ Erreur HTTP: {str(e)}")

@bot.event
async def on_ready():
    print(f'🤖 {bot.user} est connecté et prêt!')
    await log_bot_online(bot)
    
    for guild in bot.guilds:
        member_count = len(guild.members)
        print(f"\n📊 Vérification du serveur: {guild.name}")
        print(f"📋 Nombre de membres à vérifier: {member_count}")
        print(f"\nProgression:")
        for i, member in enumerate(guild.members, 1):
            print(f"{i}/{member_count}")
            await gerer_roles(member)

    await log_member_verification(bot, member, i, member_count)
    print("\n✅ Vérification des rôles terminée")

@bot.event
async def on_member_join(member):
    print(f"\n👋 Nouveau membre: {member.display_name}")
    await gerer_roles(member)

@bot.event
async def on_member_update(before, after):
    # Vérifier si les rôles ont changé
    if before.roles != after.roles:
        print(f"\n🔄 Modification des rôles pour: {after.display_name}")
        await gerer_roles(after)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def verifier_roles(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    print(f"\n🔍 Vérification manuelle demandée pour: {member.display_name}")
    await gerer_roles(member)
    await ctx.send(f"✅ Vérification des rôles effectuée pour {member.display_name}")

bot.run(TOKEN)
