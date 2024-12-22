from global_var import CHANNEL_ID

async def log_role_change(bot, member, action, role_name):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"🔄 ``{action} rôle '{role_name}' pour `` <@{member.id}>")
    else:
        print(f"❌ ``Erreur: Channel ID {CHANNEL_ID} introuvable")

async def log_bot_online(bot):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"🤖 ``{bot.user} est connecté et prêt!``")
    else:
        print(f"❌ ``Erreur: Channel ID {CHANNEL_ID} introuvable")

async def log_member_verification(bot, member, index, total):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"📋`` Nombre de membre à vérifier = {total}``")
        await channel.send(f"✅``  Vérification Terminée {index}/{total}``")
    else:
        print(f"❌ ``Erreur: Channel ID {CHANNEL_ID} introuvable")
