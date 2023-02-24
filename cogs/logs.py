import re
import discord
from discord.ext import commands
from discord.ext.commands.core import cooldown
from dislash.interactions.message_components import ActionRow, Button, ButtonStyle, SelectMenu, SelectOption
from discord import utils
from discord.utils import get
from config import Color
import messages
import word
import punishments
import asyncio
import mongo
import time
import datetime
import typing
import random
import cache
from profilactic import measures
from word import ago
import aiohttp
import time
import datetime

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['log', 'logchannel', 'log-channel', 'lc'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def log_channel(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=Color.primary)
            embed.title = "📝 | Канал логов"
            embed.add_field(name="Команды", inline=False, value=f"""
`{ctx.prefix}log-channel set` – указать канал для логов
`{ctx.prefix}log-channel remove` – удалить канал для логов
            """)
            try:
                channel = self.bot.get_channel(cache.logs_data[ctx.guild.id]["default-channel"]).mention
            except AttributeError:
                channel = None
            except KeyError:
                channel = None

            if channel:
                embed.add_field(name="Текущий канал логов", value=channel)

            await ctx.send(embed=embed)

    @log_channel.command(aliases=['set'])
    async def __set(self, ctx, channel1: discord.TextChannel):
        try:
            channel = cache.logs_data[ctx.guild.id]["default-channel"]
        except KeyError:
            channel = None

        if channel:
            if channel1.id == channel:
                return await messages.err(ctx, "Новый канал для логов не может совпадать со старым.")

        webhook = await channel1.create_webhook(name="Regular Defender Logs")
        await webhook.send("Этот канал указан в качестве канала для логов. Пожалуйста, не удаляйте этот вебхук. Спасибо!")
        cache.logs.add(ctx.guild.id, {"default-channel": channel1.id, "default-webhook": webhook.id})
        embed = discord.Embed(
            title="✅ | Готово", 
            description=f"Канал {channel1.mention} указан как канал для логов.", 
            color=Color.success
        )
        await ctx.send(embed=embed)

    @log_channel.command(aliases=['delete', 'remove'])
    async def __remove(self, ctx):
        try:
            channel = self.bot.get_channel(cache.logs_data[ctx.guild.id]["default-channel"])
        except KeyError:
            channel = None

        if not channel:
            return await messages.err(ctx, "Канал логов не был указан ранее!")
        
        cache.logs.add(ctx.guild.id, {"default-channel": None})

        embed = discord.Embed(
            title="✅ | Готово", 
            description=f"Канал {channel.mention} больше не является каналом для логов.", 
            color=Color.success
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        channel1 = self.bot.get_channel(cache.logs_data[channel.guild.id]["default-channel"])
        embed = discord.Embed(title="Создан новый канал", description=f'''**Название канала:** `{channel.name}`\n\n**Тип канала:** `{str(channel.type).replace("text", "Текстовый").replace("voice", "Голосовой").replace("category", "Категория")}`\n\n**ID канала:** `{channel.id}`\n\n**Находится в категории:** `{channel.category}`''')
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_footer(text=f'''{channel.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{channel.guild.icon_url}")
        embed.set_author(name=f"{channel.guild.name}", icon_url=f"{channel.guild.icon_url}")
        await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        channel1 = self.bot.get_channel(cache.logs_data[channel.guild.id]["default-channel"])
        embed = discord.Embed(title="Удален канал", description=f'''**Название канала:** `{channel.name}`\n\n**Тип канала:** `{str(channel.type).replace("text", "Текстовый").replace("voice", "Голосовой").replace("category", "Категория")}`\n\n**ID канала:** `{channel.id}`\n\n**Находился в категории:** `{channel.category}`''')
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_footer(text=f'''{channel.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{channel.guild.icon_url}")
        embed.set_author(name=f"{channel.guild.name}", icon_url=f"{channel.guild.icon_url}")
        await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel1 = self.bot.get_channel(cache.logs_data[message.guild.id]["default-channel"])
        embed = discord.Embed(title="Удаленное сообщение", description=f'''
        **Автор сообщения:** {message.author.mention}\n
        **Удалено в канале:** {message.channel.mention}\n
        **Сообщение:** `{message.content}`
        ''')
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=f"{message.author.avatar_url}")
        embed.set_footer(text=f'''{message.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{message.guild.icon_url}")
        await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        row = ActionRow(
            Button(
                style=ButtonStyle.link,
                label="Перейти к сообщению",
                url=f"{before.jump_url}"
            )
        )
        channel1 = self.bot.get_channel(cache.logs_data[before.guild.id]["default-channel"])
        embed = discord.Embed()
        embed.add_field(name="До изменения: ", value=f"`{before.content}`", inline=False)
        embed.add_field(name="После изменения: ", value=f"`{after.content}`", inline=False)
        embed.add_field(name="В канале: ", value=f"{after.channel.mention}", inline=False)
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_author(name=f"{before.author.name}#{before.author.discriminator}", icon_url=f"{before.author.avatar_url}")
        embed.set_footer(text=f'''{before.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{before.guild.icon_url}")
        await channel1.send(embed=embed, components=[row])

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        channel1 = self.bot.get_channel(cache.logs_data[role.guild.id]["default-channel"])
        embed = discord.Embed(
            title="Создана новая роль",
            description=f'''
            **Название роли:** `{role.name}`\n
            **ID роли:** `{role.id}`
            '''
        )
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_footer(text=f'''{role.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{role.guild.icon_url}")
        embed.set_author(name=f"{role.guild.name}", icon_url=f"{role.guild.icon_url}")
        await channel1.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        channel1 = self.bot.get_channel(cache.logs_data[before.guild.id]["default-channel"])
        embed = discord.Embed(
            title="Была обновлена роль",
            description=f'''
            **Старое название роли:** `{before.name}`
            **Новое название роли:** `{after.name}`\n
            **Старый цвет роли:** `{before.color}`
            **Новый цвет роли:** `{after.color}`\n
            **Отображается ли отдельно от других участников:** `{str(after.hoist).replace("True", "Да").replace("False", "Нет").replace("category", "Категория")}`
            ''')
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_footer(text=f'''{before.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{after.guild.icon_url}")
        embed.set_author(name=f"{before.guild.name}", icon_url=f"{after.guild.icon_url}")
        await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        channel1 = self.bot.get_channel(cache.logs_data[role.guild.id]["default-channel"])
        embed = discord.Embed(
            title="Удалена роль",
            description=f'''
            **Название роли:** `{role.name}`\n
            **ID роли:** `{role.id}`
            '''
        )
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_footer(text=f'''{role.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{role.guild.icon_url}")
        embed.set_author(name=f"{role.guild.name}", icon_url=f"{role.guild.icon_url}")
        await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        channel1 = self.bot.get_channel(cache.logs_data[before.guild.id]["default-channel"])
        embed = discord.Embed(
            title="Был обновлен канал",
            description=f'''
            **Старое название канала:** {before.name}
            **Новое название канала:** {after.name}\n
            **Старая категория, где находился канал:** {before.category}
            **Новая категория, где находится канал:** {after.category}
            '''
        )
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_footer(text=f'''{before.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{after.guild.icon_url}")
        embed.set_author(name=f"{before.guild.name}", icon_url=f"{after.guild.icon_url}")
        await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel1 = self.bot.get_channel(cache.logs_data[before.guild.id]["default-channel"])
        embed = discord.Embed()
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_footer(text=f'''{before.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{after.guild.icon_url}")
        embed.set_author(name=f"{before.name}", icon_url=f"{after.avatar_url}")
        if before.nick != after.nick:
            embed.title = f"Пользователь {before.name}#{before.discriminator} был обновлен"
            embed.description = f'''
            **Старый ник пользователя:** {str(before.nick).replace("None", f"{before.name}")}
            **Новый ник пользователя:** {str(after.nick).replace("None", f"{after.name}")}'''
        elif before.roles != after.roles:
            embed.title = f"У пользователя {before.name}#{before.discriminator} были обновлены роли"
            embed.description = f'''
            **Старые роли пользователя:** {before.roles[1]}
            **Новые роли пользователя:** {after.roles[1]}'''
        elif before.status != after.status:
            embed.title = f"У пользователя {before.name}#{before.discriminator} был изменен статус"
            embed.description = f'''
            **Старый статус:** {before.status}
            **Новый статус:** {after.status}
            '''
        await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_disconnect(self, channel, member):
        channel1 = self.bot.get_channel(cache.logs_data[channel.guild.id]["default-channel"])
        embed = discord.Embed()
        embed.description = f"Участник **{member.name}** ({member.mention})"
        embed.add_field(name="Время: ", value=f'{datetime.datetime.now().strftime("%d.%m.%Y в %H:%M:%S")}', inline=False)
        embed.set_footer(text=f'''{channel.guild.name} • Сегодня, в {datetime.datetime.now().strftime("%H:%M")}''', icon_url=f"{channel.guild.icon_url}")
        embed.set_author(name=f"{channel.guild.name}", icon_url=f"{channel.guild.icon_url}")
        await channel1.send(embed=embed)


def setup(bot):
    bot.add_cog(Logs(bot))