import discord
from discord.ext import commands

from global_var import *

# Configuration du bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='+', intents=intents)

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
    print(f"- Sub Emma: {has_sub_emma}")
    print(f"- Sub Ro: {has_sub_ro}")

    # Gestion du rôle les_subs
    should_have_role_les_subs = has_sub_emma or has_sub_ro
    
    if should_have_role_les_subs and role_les_subs not in member.roles:
        try:
            await member.add_roles(role_les_subs)
            print(f"✅ Rôle 'les_subs' ajouté à {member.display_name}")
        except discord.Forbidden:
            print(f"❌ Erreur de permissions pour ajouter 'les_subs' à {member.display_name}")
        except discord.HTTPException as e:
            print(f"❌ Erreur HTTP pour 'les_subs': {str(e)}")
    elif not should_have_role_les_subs and role_les_subs in member.roles:
        try:
            await member.remove_roles(role_les_subs)
            print(f"🔄 Rôle 'les_subs' retiré de {member.display_name} (conditions non remplies)")
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
        except discord.Forbidden:
            print(f"❌ Erreur de permissions pour ajouter 'super_subs' à {member.display_name}")
        except discord.HTTPException as e:
            print(f"❌ Erreur HTTP: {str(e)}")
    elif not should_have_role_super_subs and role_super_subs in member.roles:
        try:
            await member.remove_roles(role_super_subs)
            print(f"🔄 Rôle 'super_subs' retiré de {member.display_name} (conditions non remplies)")
        except discord.Forbidden:
            print(f"❌ Erreur de permissions pour retirer 'super_subs' de {member.display_name}")
        except discord.HTTPException as e:
            print(f"❌ Erreur HTTP: {str(e)}")

@bot.event
async def on_ready():
    print(f'🤖 {bot.user} est connecté et prêt!')
    
    for guild in bot.guilds:
        member_count = len(guild.members)
        print(f"\n📊 Vérification du serveur: {guild.name}")
        print(f"📋 Nombre de membres à vérifier: {member_count}")
        
        for i, member in enumerate(guild.members, 1):
            print(f"\nProgression: {i}/{member_count}")
            await gerer_roles(member)
    
    print("\n✅ Vérification initiale des rôles terminée")

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


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! ``{round(bot.latency * 1000)}ms``")