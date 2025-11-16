import aiohttp
import discord
from discord.ext import tasks
from datetime import datetime
import re

class TikTokMonitor:
    def __init__(self, bot, tiktok_username: str, notification_channel_id: int):
        """
        Moniteur de nouveaux TikToks
        
        Args:
            bot: Instance du bot Discord
            tiktok_username: Nom d'utilisateur TikTok à surveiller (avec ou sans @)
            notification_channel_id: ID du salon Discord où envoyer les notifications
        """
        self.bot = bot
        self.tiktok_username = tiktok_username.replace('@', '')
        self.notification_channel_id = notification_channel_id
        self.last_video_id = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    async def get_latest_video(self):
        """Récupère la dernière vidéo TikTok via le feed RSS"""
        try:
            # Utiliser le feed RSS de TikTok
            url = f"https://www.tiktok.com/@{self.tiktok_username}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=10) as response:
                    if response.status != 200:
                        print(f"⚠️ Erreur lors de la récupération du profil TikTok: {response.status}")
                        return None
                    
                    html = await response.text()
                    
                    # Chercher l'ID de la dernière vidéo dans le HTML
                    # Pattern pour trouver les IDs de vidéos TikTok
                    video_pattern = r'"id":"(\d{19})"'
                    matches = re.findall(video_pattern, html)
                    
                    if matches:
                        latest_id = matches[0]
                        video_url = f"https://www.tiktok.com/@{self.tiktok_username}/video/{latest_id}"
                        
                        # Extraire d'autres infos si possible
                        desc_pattern = r'"desc":"([^"]*)"'
                        desc_matches = re.findall(desc_pattern, html)
                        description = desc_matches[0] if desc_matches else "Nouvelle vidéo TikTok"
                        
                        return {
                            "id": latest_id,
                            "url": video_url,
                            "description": description,
                            "username": self.tiktok_username
                        }
                    
                    return None
                    
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de la vidéo TikTok: {e}")
            return None
    
    async def send_tiktok_notification(self, video_data):
        """Envoie une notification Discord quand une nouvelle vidéo TikTok est postée"""
        channel = self.bot.get_channel(self.notification_channel_id)
        if not channel:
            print(f"❌ Canal de notification introuvable (ID: {self.notification_channel_id})")
            return
        
        # Créer l'embed de notification
        embed = discord.Embed(
            title=f"🎵 Nouvelle vidéo TikTok de @{video_data['username']} !",
            description=video_data['description'][:200] if len(video_data['description']) > 200 else video_data['description'],
            color=discord.Color.from_rgb(255, 0, 80),  # Couleur rose TikTok
            url=video_data['url']
        )
        
        # Ajouter le lien
        embed.add_field(
            name="🔗 Lien",
            value=f"[Regarder sur TikTok]({video_data['url']})",
            inline=False
        )
        
        # Thumbnail TikTok logo
        embed.set_thumbnail(url="https://sf-tb-sg.ibytedtos.com/obj/eden-sg/uhtyvueh7nulogpoguhm/tiktok-icon2.png")
        
        embed.set_footer(text="TikTok", icon_url="https://sf-tb-sg.ibytedtos.com/obj/eden-sg/uhtyvueh7nulogpoguhm/tiktok-icon2.png")
        embed.timestamp = datetime.utcnow()
        
        await channel.send(
            content=video_data['url'],
            embed=embed
        )
        print(f"✅ Notification TikTok envoyée pour @{self.tiktok_username}")
    
    @tasks.loop(minutes=5)  # Vérifie toutes les 5 minutes
    async def monitor_tiktok(self):
        """Tâche périodique pour surveiller les nouveaux TikToks"""
        video_data = await self.get_latest_video()
        
        if video_data:
            # Si c'est la première vérification, enregistrer l'ID sans notifier
            if self.last_video_id is None:
                self.last_video_id = video_data['id']
                print(f"ℹ️ Dernière vidéo TikTok enregistrée: {video_data['id']}")
            
            # Si une nouvelle vidéo est détectée
            elif video_data['id'] != self.last_video_id:
                self.last_video_id = video_data['id']
                await self.send_tiktok_notification(video_data)
    
    @monitor_tiktok.before_loop
    async def before_monitor_tiktok(self):
        """Attend que le bot soit prêt avant de démarrer la surveillance"""
        await self.bot.wait_until_ready()
        print(f"🔍 Surveillance TikTok de @{self.tiktok_username} démarrée")
    
    def start(self):
        """Démarre la surveillance TikTok"""
        self.monitor_tiktok.start()
    
    def stop(self):
        """Arrête la surveillance TikTok"""
        self.monitor_tiktok.cancel()
