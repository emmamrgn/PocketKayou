import discord
from datetime import datetime
from global_var import CHANNEL_LOG_ID

async def log_command(ctx, response):
    channel = ctx.bot.get_channel(CHANNEL_LOG_ID)
    if channel:
        embed = discord.Embed(title="Command Log", color=discord.Color.blue())
        embed.add_field(name="User", value=f"<@{ctx.author.id}>", inline=True)
        embed.add_field(name="Command", value=f"``{ctx.message.content}``", inline=True)
        embed.add_field(name="Response", value=f"{response}", inline=False)
        embed.set_footer(text=datetime.now().strftime("%H:%M - %d-%m-%Y"))
        await channel.send(embed=embed)

async def log_bot_ready(bot):
    channel = bot.get_channel(CHANNEL_LOG_ID)
    if channel:
        bot_status = f"🤖 {bot.user} est connecté et prêt!"
        date = datetime.now().strftime("%H:%M %d-%m-%Y")
        content = date + " : " + bot_status
        await channel.send(f"```{content}```")
