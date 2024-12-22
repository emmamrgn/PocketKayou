import discord
from global_var import CHANNEL_ID

async def log_role_change(member, role, action):
    channel = member.guild.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"🔄 {action} rôle '{role.name}' pour {member.display_name}")