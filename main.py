import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime

load_dotenv()
normalprefix = "log "


async def get_prefix(prefix):
    client.command_prefix = prefix

intents = discord.Intents.all()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix=get_prefix, intents=intents, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="the logs"))
client.remove_command('help')


@client.event
async def on_ready():
    print("Loggy has been started!\n"
          "-----------------------\n"
          f"Loggy latency: {round(client.latency * 1000)}ms")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Hey, slow a bit down!", description=f"You can use this command again in {error.retry_after:.2f} seconds!", color=discord.Color.blurple())
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


@client.event
async def on_message(message):
        db = sqlite3.connect('./db/prefix.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {message.guild.id}")
        result = cursor.fetchone()

        if result is None:
            client.command_prefix = normalprefix
            await client.process_commands(message)
        else:
            client.command_prefix = result[0]
            await client.process_commands(message)

        db.commit()
        if result is None:
            if message.content.startswith("<@!854053068668403753>") or message.content.startswith(
                        "<@854053068668403753>"):
                    embed = discord.Embed(title="",
                                          description="Hello, thank you for using Loggy!\n"
                                                      "\n"
                                                      "Loggy's default prefix is `log `\n"
                                                      "Configure your new prefix with `log prefix <prefix>`\n"
                                                      "\n"
                                                      "What are you waiting for?\n"
                                                      "Start configuring with Loggy! Keep track what's happening in your server!\n"                                    
                                                      "Use `log help` to learn more.\n",
                                          color=discord.Color.blurple())
                    embed.set_thumbnail(url=client.user.avatar_url)
                    embed.timestamp = datetime.utcnow()
                    await message.channel.send(embed=embed)
        else:
                if message.content.startswith("<@!854053068668403753>") or message.content.startswith(
                        "<@854053068668403753>"):
                    embed = discord.Embed(title="",
                                          description="Hello, thank you for using Loggy!\n"
                                                      "\n"
                                                      f"What are you waiting for?\n"
                                                      f"Start configuring with Loggy! Keep track what's happening in your server!\n"
                                                      f"Use `{result[0]}help` to learn more.\n",
                                          color=discord.Color.blurple())
                    embed.set_thumbnail(url=client.user.avatar_url)
                    embed.timestamp = datetime.utcnow()
                    await message.channel.send(embed=embed)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


token = os.getenv("TOKEN")
client.run(token)
