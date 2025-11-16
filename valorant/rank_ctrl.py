import aiohttp
from bs4 import BeautifulSoup
import discord

async def get_valorant_rank(username_tag: str) -> dict:
    """
    Récupère les informations de rank Valorant depuis tracker.gg
    
    Args:
        username_tag: Le nom d'utilisateur avec le tag (ex: "emm4#000")
    
    Returns:
        dict: Dictionnaire contenant les informations du joueur ou une erreur
    """
    try:
        # Formatter l'URL pour tracker.gg
        formatted_tag = username_tag.replace("#", "%23")
        url = f"https://tracker.gg/valorant/profile/riot/{formatted_tag}/overview"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, allow_redirects=True) as response:
                if response.status == 404:
                    return {
                        "success": False,
                        "error": "Joueur non trouvé. Vérifiez le nom d'utilisateur et le tag."
                    }
                
                if response.status != 200:
                    return {
                        "success": False,
                        "error": f"Erreur lors de la récupération des données (Status: {response.status})"
                    }
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Chercher le rang actuel
                rank_element = soup.find('div', class_='valorant-rank-name')
                rating_element = soup.find('div', class_='rating-entry__rank-info')
                
                if not rank_element:
                    return {
                        "success": False,
                        "error": "Impossible de récupérer le rang. Le joueur n'a peut-être pas de rang en compétitif."
                    }
                
                rank = rank_element.text.strip()
                
                # Récupérer le RR (Rating Rank)
                rr = "N/A"
                if rating_element:
                    rr_text = rating_element.find('span', class_='valorant-rank-rating')
                    if rr_text:
                        rr = rr_text.text.strip()
                
                # Récupérer les stats additionnelles
                stats = {}
                stat_elements = soup.find_all('div', class_='stat')
                for stat in stat_elements[:3]:  # Limiter aux 3 premières stats
                    name = stat.find('span', class_='name')
                    value = stat.find('span', class_='value')
                    if name and value:
                        stats[name.text.strip()] = value.text.strip()
                
                return {
                    "success": True,
                    "username": username_tag,
                    "rank": rank,
                    "rr": rr,
                    "stats": stats,
                    "url": url.replace("%23", "%23")
                }
                
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}"
        }


def create_rank_embed(data: dict) -> discord.Embed:
    """
    Crée un embed Discord avec les informations de rank
    
    Args:
        data: Dictionnaire contenant les données du joueur
    
    Returns:
        discord.Embed: L'embed formaté
    """
    if not data["success"]:
        embed = discord.Embed(
            title="❌ Erreur",
            description=data["error"],
            color=discord.Color.red()
        )
        return embed
    
    # Déterminer la couleur selon le rank
    rank_colors = {
        "Iron": discord.Color.from_rgb(79, 89, 102),
        "Bronze": discord.Color.from_rgb(205, 127, 50),
        "Silver": discord.Color.from_rgb(192, 192, 192),
        "Gold": discord.Color.from_rgb(255, 215, 0),
        "Platinum": discord.Color.from_rgb(0, 255, 255),
        "Diamond": discord.Color.from_rgb(185, 130, 255),
        "Ascendant": discord.Color.from_rgb(50, 205, 50),
        "Immortal": discord.Color.from_rgb(255, 0, 127),
        "Radiant": discord.Color.from_rgb(255, 255, 150)
    }
    
    # Trouver la couleur appropriée
    embed_color = discord.Color.blue()
    for rank_name, color in rank_colors.items():
        if rank_name.lower() in data["rank"].lower():
            embed_color = color
            break
    
    embed = discord.Embed(
        title=f"🎮 Rang Valorant - {data['username']}",
        description=f"**{data['rank']}** {data['rr']}",
        color=embed_color,
        url=data['url']
    )
    
    # Ajouter les stats si disponibles
    if data.get("stats"):
        for stat_name, stat_value in data["stats"].items():
            embed.add_field(name=stat_name, value=stat_value, inline=True)
    
    embed.set_footer(text="Données de tracker.gg")
    
    return embed
