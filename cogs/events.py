import discord
from discord.ext import commands
from datetime import datetime
import sqlite3


class LoggyEvents(commands.Cog, name="Loggy Events"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT modrole FROM main WHERE guild_id = {guild.id}")
        result = cursor.fetchone()
        if result is None:
                cursor.execute(f"INSERT INTO main(guild_id) VALUES({guild.id})")
        db.commit()
        db.close()
        members = set(guild.members)
        bots = filter(lambda m: m.bot, members)
        bots = set(bots)
        channel = self.bot.get_channel(854085275407220766)
        embed = discord.Embed(description="Loggy got added on a server!\n"
                                          "\n"
                                          f"Server: `{guild.name} ({guild.id})`\n"
                                          f"Owner: `{guild.owner} ({guild.owner.id})`\n"
                                          f"\n"
                                          f"> Total Members: {guild.member_count}\n"
                                          f"> Total Bots: {len(bots)}", color=discord.Color.blurple())
        embed.timestamp = datetime.utcnow()
        embed.set_author(name="New Server!")
        embed.set_footer(text=f"Loggy is now in {str(len(self.bot.guilds))} server!")
        await channel.send(embed=embed)
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                em = discord.Embed(title="",
                                   description="Thank you for inviting Loggy!\n"
                                               "\n"
                                               "Loggy is an advanced logging bot! You can highly configure Loggy.\n"
                                               "To set up Loggy type `log setup`\n"
                                               "\n"
                                               "**About Loggy**:\n"
                                               "• Loggy's Prefix: `log `\n"
                                               "• Configure your log channel and disable or enable events.\n"
                                               "• Configure a moderator role, only the people with the role can see the logs.\n"
                                               "\n"
                                               "> `log help` to learn more.\n"
                                               "\n"
                                               "for further support join [loggy's support server.](https://discord.gg/nxBGYuxs)",
                                   color=discord.Color.blurple())
                em.set_thumbnail(url=f"{self.bot.user.avatar_url}")
                em.timestamp = datetime.utcnow()
                await channel.send(embed=em)
            break


def setup(bot):
    bot.add_cog(LoggyEvents(bot))
    print("Loggy Owner Events Cog loaded!")