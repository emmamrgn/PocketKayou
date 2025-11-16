import aiohttp
import discord
from discord.ext import tasks
from datetime import datetime

class TwitchMonitor:
    def __init__(self, bot, client_id: str, client_secret: str, twitch_username: str, notification_channel_id: int, role_id: int = None):
        """
        Moniteur de streams Twitch
        
        Args:
            bot: Instance du bot Discord
            client_id: Client ID de l'application Twitch
            client_secret: Client Secret de l'application Twitch
            twitch_username: Nom d'utilisateur Twitch à surveiller
            notification_channel_id: ID du salon Discord où envoyer les notifications
            role_id: ID du rôle Discord à mentionner (None pour @everyone)
        """
        self.bot = bot
        self.client_id = client_id
        self.client_secret = client_secret
        self.twitch_username = twitch_username.lower()
        self.notification_channel_id = notification_channel_id
        self.role_id = role_id
        self.access_token = None
        self.is_live = False
        self.stream_data = None
        
    async def get_app_access_token(self):
        """Obtient un token d'accès OAuth pour l'API Twitch"""
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.access_token = data["access_token"]
                        print(f"✅ Token Twitch obtenu avec succès")
                        return True
                    else:
                        print(f"❌ Erreur lors de l'obtention du token Twitch: {response.status}")
                        return False
        except Exception as e:
            print(f"❌ Erreur lors de l'obtention du token Twitch: {e}")
            return False
    
    async def get_user_id(self):
        """Récupère l'ID utilisateur Twitch à partir du nom d'utilisateur"""
        if not self.access_token:
            await self.get_app_access_token()
        
        url = f"https://api.twitch.tv/helix/users?login={self.twitch_username}"
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data["data"]:
                            return data["data"][0]["id"]
                    return None
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de l'ID utilisateur: {e}")
            return None
    
    async def check_stream_status(self):
        """Vérifie si le stream est en ligne"""
        if not self.access_token:
            await self.get_app_access_token()
        
        url = f"https://api.twitch.tv/helix/streams?user_login={self.twitch_username}"
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 401:  # Token expiré
                        await self.get_app_access_token()
                        return await self.check_stream_status()
                    
                    if response.status == 200:
                        data = await response.json()
                        return data["data"][0] if data["data"] else None
                    return None
        except Exception as e:
            print(f"❌ Erreur lors de la vérification du statut du stream: {e}")
            return None
    
    async def send_stream_notification(self, stream_data):
        """Envoie une notification Discord quand le stream démarre"""
        channel = self.bot.get_channel(self.notification_channel_id)
        if not channel:
            print(f"❌ Canal de notification introuvable (ID: {self.notification_channel_id})")
            return
        
        embed = discord.Embed(
            title=f"🔴 {stream_data['user_name']} est en live !",
            description=stream_data['title'],
            color=discord.Color.purple(),
            url=f"https://twitch.tv/{self.twitch_username}"
        )
        
        embed.add_field(name="🎮 Jeu", value=stream_data.get('game_name', 'Non spécifié'), inline=True)
        embed.add_field(name="👥 Spectateurs", value=str(stream_data.get('viewer_count', 0)), inline=True)
        
        # Thumbnail du stream
        thumbnail_url = stream_data['thumbnail_url'].replace('{width}', '320').replace('{height}', '180')
        embed.set_image(url=thumbnail_url)
        
        # Avatar du streamer
        user_data = await self.get_user_info()
        if user_data and user_data.get('profile_image_url'):
            embed.set_thumbnail(url=user_data['profile_image_url'])
        
        embed.set_footer(text="Twitch", icon_url="https://static.twitchcdn.net/assets/favicon-32-e29e246c157142c94346.png")
        embed.timestamp = datetime.utcnow()
        
        # Déterminer la mention à utiliser
        if self.role_id:
            mention = f"<@&{self.role_id}>"
            allowed_mentions = discord.AllowedMentions(roles=True)
        else:
            mention = "@everyone"
            allowed_mentions = discord.AllowedMentions(everyone=True)
        
        await channel.send(
            content=mention,
            embed=embed,
            allowed_mentions=allowed_mentions
        )
        print(f"✅ Notification de stream envoyée pour {self.twitch_username}")
    
    async def get_user_info(self):
        """Récupère les informations de profil de l'utilisateur Twitch"""
        if not self.access_token:
            await self.get_app_access_token()
        
        url = f"https://api.twitch.tv/helix/users?login={self.twitch_username}"
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data["data"][0] if data["data"] else None
                    return None
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des infos utilisateur: {e}")
            return None
    
    @tasks.loop(minutes=2)  
    async def monitor_stream(self):
        """Tâche périodique pour surveiller le statut du stream"""
        stream_data = await self.check_stream_status()
        
        # Si le stream vient de démarrer
        if stream_data and not self.is_live:
            self.is_live = True
            self.stream_data = stream_data
            await self.send_stream_notification(stream_data)
        
        # Si le stream s'est arrêté
        elif not stream_data and self.is_live:
            self.is_live = False
            self.stream_data = None
            print(f"ℹ️ Stream terminé pour {self.twitch_username}")
    
    @monitor_stream.before_loop
    async def before_monitor_stream(self):
        """Attend que le bot soit prêt avant de démarrer la surveillance"""
        await self.bot.wait_until_ready()
        print(f"🔍 Surveillance du stream Twitch de {self.twitch_username} démarrée")
    
    def start(self):
        """Démarre la surveillance du stream"""
        self.monitor_stream.start()
    
    def stop(self):
        """Arrête la surveillance du stream"""
        self.monitor_stream.cancel()
