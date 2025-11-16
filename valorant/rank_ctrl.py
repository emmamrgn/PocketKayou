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
        # Vérifier le format
        if "#" not in username_tag:
            return {
                "success": False,
                "error": "Format incorrect. Utilisez: username#tag"
            }
        
        # Séparer le nom et le tag
        game_name, tag_line = username_tag.split("#")
        
        # Utiliser l'API valorantrank.chat (retourne du texte brut)
        url = f"https://valorantrank.chat/eu/{game_name}/{tag_line}?onlyRank=true"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 404:
                    return {
                        "success": False,
                        "error": "Joueur non trouvé. Vérifiez le nom et le tag."
                    }
                
                if response.status != 200:
                    return {
                        "success": False,
                        "error": f"Erreur lors de la récupération des données (Status: {response.status})"
                    }
                
                # Récupérer le texte brut (ex: "Diamond 3 : 19 RR")
                text = await response.text()
                text = text.strip()
                
                # Vérifier si le joueur a un rang
                if not text or "Unrated" in text:
                    return {
                        "success": False,
                        "error": "Le joueur n'a pas de rang en compétitif."
                    }
                
                # Parser le texte (format: "Rank : RR RR")
                if " : " in text:
                    rank_part, rr_part = text.split(" : ", 1)
                    rank = rank_part.strip()
                    rr = rr_part.replace(" RR", "").strip()
                else:
                    # Si le format est différent, utiliser le texte brut
                    rank = text
                    rr = "N/A"
                
                return {
                    "success": True,
                    "username": username_tag,
                    "rank": rank,
                    "rr": f"{rr} RR" if rr != "N/A" else "N/A",
                    "stats": {},
                    "url": f"https://tracker.gg/valorant/profile/riot/{game_name}%23{tag_line}/overview"
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
        "Iron": discord.Color.from_rgb(84, 89, 94),
        "Bronze": discord.Color.from_rgb(168, 94, 20),
        "Silver": discord.Color.from_rgb(181, 178, 178),
        "Gold": discord.Color.from_rgb(255, 205, 81),
        "Platinum": discord.Color.from_rgb(21, 126, 204),
        "Diamond": discord.Color.from_rgb(223, 113, 255),
        "Ascendant": discord.Color.from_rgb(30, 153, 19),
        "Immortal": discord.Color.from_rgb(255, 0, 55),
        "Radiant": discord.Color.from_rgb(255, 255, 150)
    }
    
    # Trouver la couleur appropriée
    embed_color = discord.Color.blue()
    for rank_name, color in rank_colors.items():
        if rank_name.lower() in data["rank"].lower():
            embed_color = color
            break
    
    embed = discord.Embed(
        title=f"🎮 {data['username']}",
        description=f"**{data['rank']}** - {data['rr']}",
        color=embed_color,
        url=data['url']
    )
    
    # Ajouter les stats si disponibles
    if data.get("stats"):
        for stat_name, stat_value in data["stats"].items():
            embed.add_field(name=stat_name, value=stat_value, inline=True)
    
   
    
    return embed
