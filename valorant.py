import aiohttp
import re
import discord

class rank_modele:
    def __init__(self, username, tag):
        self.username = username
        self.tag = tag
        self.url = f'https://splendid-groovy-feverfew.glitch.me/valorant/eu/{username}/{tag}?mmrChange=true'
        self.tracker_url = f"https://tracker.gg/valorant/profile/riot/{self.username}%23{self.tag}/overview"

    async def fetch_rank_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    content = await response.text()
                    if self.is_valid_content(content):
                        return self.parse_content(content)
                return None
            
    def get_tracker_url(self):
        return self.tracker_url
    
    def is_valid_content(self, content):
        return bool(re.search(r"(.+?)#(\w+) \[(.*?)\] : (\d+) RR \[(.*?)\]", content))

    def parse_content(self, content):
        match = re.search(r"(.+?)#(\w+) \[(.*?)\] : (\d+) RR \[(.*?)\]", content)
        if match:
            return {
                "username": f"{match.group(1)}#{match.group(2)}",
                "rank": match.group(3),
                "rr": match.group(4),
                "rr_change": match.group(5)
            }
        return None

class rank_vue:
    @staticmethod
    async def display_rank(ctx, rank_data):
        if rank_data and all(key in rank_data for key in ['username', 'rank', 'rr', 'rr_change']):
            rr_change = int(rank_data['rr_change'])
            if rr_change >= 0:
                rr_change = f"+{rr_change}"
            embed_rank = discord.Embed(title=f"{rank_data['username']}", color=discord.Color.brand_red(), timestamp=ctx.message.created_at)
            embed_rank.add_field(name="rank : ", value=f"``{rank_data['rank']} - {rank_data['rr']} rr``", inline=False)
            embed_rank.add_field(name="last game : ", value=f"``{rr_change} rr``", inline=False)
            # Create an instance of rank_modele to get the tracker URL
            username, tag = rank_data['username'].split('#')
            rank_model_instance = rank_modele(username, tag)
            embed_rank.add_field(name="tracker : ", value=f"[tracker.gg/{rank_data['username']}]({rank_model_instance.get_tracker_url()})", inline=False)
            await ctx.send(f"{ctx.author.mention}", embed=embed_rank)
        else:
            print("Impossible de récupérer les données. Format invalide.")
            await ctx.send(f"{ctx.author.mention}```Impossible de récupérer les données. \nFaute d'orthographe ? Mauvais pseudo ou tag ?```")

class rank_ctrl:
    def __init__(self, ctx, username, tag):
        self.ctx = ctx
        self.model = rank_modele(username, tag)

    async def get_rank(self):
        rank_data = await self.model.fetch_rank_data()
        await rank_vue.display_rank(self.ctx, rank_data)
