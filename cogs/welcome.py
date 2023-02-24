import discord
from discord.ext import commands
import datetime
import time
import messages
import cache
import config
from config import Color

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['welcome', 'welcomechannel', 'welcome-channel'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def welcome_channel(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=Color.primary)
            embed.title = "📝 | Канал приветствий"
            embed.add_field(name="Команды", inline=False, value=f"""
`{ctx.prefix}log-channel set` – указать канал для приветствия
`{ctx.prefix}log-channel remove` – удалить канал для приветствия
            """)
            try:
                channel = self.bot.get_channel(cache.greetings_data[ctx.guild.id]["welcome-channel"]).mention
            except AttributeError:
                channel = None
            except KeyError:
                channel = None

            if channel:
                embed.add_field(name="Текущий канал приветсвия", value=channel)

            await ctx.send(embed=embed)

    @welcome_channel.command(aliases=['set'])
    async def __set(self, ctx, channel1: discord.TextChannel):
        try:
            channel = cache.greetings_data[ctx.guild.id]["welcome-channel"]
        except KeyError:
            channel = None

        if channel:
            if channel1.id == channel:
                return await messages.err(ctx, "Новый канал для логов не может совпадать со старым.")

        cache.greetings.add(ctx.guild.id, {"welcome-channel": channel1.id})
        embed = discord.Embed(
            title="✅ | Готово", 
            description=f"Канал {channel1.mention} указан как канал для приветствия.", 
            color=Color.success
        )
        await ctx.send(embed=embed)

    @welcome_channel.command(aliases=['delete', 'remove'])
    async def __remove(self, ctx):
        try:
            channel = self.bot.get_channel(cache.greetings_data[ctx.guild.id]["welcome-channel"])
        except KeyError:
            channel = None

        if not channel:
            return await messages.err(ctx, "Канал приветствия не был указан ранее!")
        
        cache.greetings.add(ctx.guild.id, {"welcome-channel": None})

        embed = discord.Embed(
            title="✅ | Готово", 
            description=f"Канал {channel.mention} больше не является каналом для приветствия.", 
            color=Color.success
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel1 = self.bot.get_channel(cache.greetings_data[member.guild.id]["welcome-channel"])
        embed = discord.Embed()
        embed.description = f'''
        {member.mention}, добро пожаловать на сервер {member.guild.name}'''
        embed.set_image(url=f"{member.avatar_url}")
        await channel1.send(embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))