import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

from discord.ext.commands import BucketType


class Misc(commands.Cog, name="Miscellaneous"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['setprefix', 'changeprefix'])
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix=None):
        db = sqlite3.connect('./db/prefix.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result:
            if prefix == result[0]:
                return await ctx.send("You already have this custom prefix.")
        if prefix is None:
            embed = discord.Embed(title="", description=f"Current prefix is `{ctx.prefix}`\n"
                                                        f"If you want to change the prefix enter `{ctx.prefix}prefix <prefix>`",
                                  color=discord.Color.blue())
            embed.timestamp = datetime.utcnow()
            embed.set_author(name=f"Loggy",
                             icon_url=f"{self.bot.user.avatar_url}")
            embed.set_footer(text=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            return await ctx.send(embed=embed)
        if len(prefix) > 8:
            return await ctx.send("Your prefix cannot be longer than 8 characters.")
        if result is not None:
            sql = "UPDATE main SET prefix = ? WHERE guild_id = ?"
            val = (prefix, ctx.guild.id)
            embed = discord.Embed(description=f"Loggy's prefix has been updated set to `{prefix}`", color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            sql = "INSERT INTO main(guild_id, prefix) VALUES(?,?)"
            val = (ctx.guild.id, prefix)
            embed = discord.Embed(description=f"Loggy's prefix has been set to `{prefix}`", color=discord.Color.blue())
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @commands.command(aliases=['rprefix', 'defaultprefix'])
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    async def resetprefix(self, ctx):
        db = sqlite3.connect('./db/prefix.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is not None:
            cursor.execute("DELETE FROM main WHERE guild_id = '{}' and prefix = '{}'".format(ctx.guild.id, result[0]))
            embed = discord.Embed(description=f"Loggy's prefix has been reset.",
                                  color=discord.Color.blue())
            await ctx.send(embed=embed)
        if result is None:
            await ctx.send("You don't had a custom prefix before.")
        db.commit()
        db.close()

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def privacy(self, ctx):
        embed = discord.Embed(title="Loggy Privacy Policy",
                              description="> **By having Loggy in your server, you agree to the following privacy policy.**\n"
                                          "\n"
                                          "> What information is stored?\n"
                                          "Role ID is stored for Loggy moderator role.\n"
                                          "Guild ID is stored that the bot know in which guild you had the configurations and else.\n"
                                          "Channel ID for the logging channel."
                                          "\n"
                                          "> Why we store the information and how we use it.\n"
                                          "We store the information because to save configurations on your server.\n"
                                          "\n"
                                          "> Who gets this data?\n"
                                          "This data is only available for the developer.\n"
                                          "\n"
                                          "> Questions and Concerns.\n"
                                          "If you have questions and/or concerns about the data stored, please contact [hris#0002](https://discord.com/users/675280674994782208).\n"
                                          "\n"
                                          "> How to Remove your data.\n"
                                          "If you would like us to remove your data, please contact [hris#0002](https://discord.com/users/675280674994782208)."
                                          "\n"
                                          "> **Note:** We reserve the right to change this without notifying our users.",
                              color=discord.Color.blurple())
        embed.set_footer(text="This policy was last updated june 20th, 2021")
        await ctx.send(embed=embed)

    @privacy.command()
    @commands.cooldown(1, 3, BucketType.user)
    @commands.guild_only()
    async def policy(self, ctx):
        embed = discord.Embed(title="Loggy Privacy Policy",
                              description="> **By having Loggy in your server, you agree to the following privacy policy.**\n"
                                          "\n"
                                          "> What information is stored?\n"
                                          "Role ID is stored for Loggy moderator role.\n"
                                          "Guild ID is stored that the bot know in which guild you had the configurations and else.\n"
                                          "Channel ID for the logging channel."
                                          "\n"
                                          "> Why we store the information and how we use it.\n"
                                          "We store the information because to save configurations on your server.\n"
                                          "\n"
                                          "> Who gets this data?\n"
                                          "This data is only available for the developer.\n"
                                          "\n"
                                          "> Questions and Concerns.\n"
                                          "If you have questions and/or concerns about the data stored, please contact [hris#0002](https://discord.com/users/675280674994782208).\n"
                                          "\n"
                                          "> How to Remove your data.\n"
                                          "If you would like us to remove your data, please contact [hris#0002](https://discord.com/users/675280674994782208).\n"
                                          "\n"
                                          "> **Note:** We reserve the right to change this without notifying our users.",
                              color=discord.Color.blurple())
        embed.set_footer(text="This policy was last updated june 20th, 2021")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
    print("Loggy Miscellaneous Cog loaded!")
