import discord
from discord.ext import commands


class OwnerCommands(commands.Cog, name="Owner Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['gg', 'guildinfo', 'guild'])
    @commands.is_owner()
    async def getguild(self, ctx, guild_id: int):
        try:
            guild = self.bot.get_guild(guild_id)
            members = set(guild.members)
            bots = filter(lambda m: m.bot, members)
            bots = set(bots)
            embed = discord.Embed(title="", description="")
            embed.add_field(name="guild name", value=guild.name)
            embed.add_field(name="guild member count", value=guild.member_count, inline=False)
            embed.add_field(name="guild owner", value=guild.owner, inline=False)
            embed.add_field(name="guild created at", value=guild.created_at.__format__('%A, %d. %B %Y at %H:%M:%S'),
                            inline=False)
            embed.add_field(name="guild region", value=guild.region, inline=False)
            embed.add_field(name="guild all bots", value=f"{len(bots)}", inline=False)
            embed.add_field(name="guild boost stats",
                            value="{} (Level {})".format(guild.premium_subscription_count, guild.premium_tier))

            await ctx.send(embed=embed)
        except:
            await ctx.send(f"Failed to get information about guild ({guild_id})")

    @commands.command()
    @commands.is_owner()
    async def dm(self, ctx, userid: int = None, message: str = None):
        try:
            user = self.bot.get_user(id=userid)
            await user.send(message)
            msg1 = await ctx.send(f"Message sent to {user} ({userid})")
            await msg1.add_reaction("✅")
        except:
            msg = await ctx.send("User not found or DMs are off.")
            await msg.add_reaction("❌")


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
    print("Loggy Owner Cog loaded!")