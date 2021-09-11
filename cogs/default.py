import sqlite3
from datetime import datetime
import discord
import psutil
from discord.ext import commands
from discord.ext.commands import BucketType


class DefaultCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 6, BucketType.user)
    async def help(self, ctx):
        embed = discord.Embed(title="Loggy Commands", description=f"Loggy's prefix for the server is `{ctx.prefix}`", color=0x6e89d8)
        embed.add_field(name="Logging — 2", value="`event`, `disable-event`", inline=False)
        embed.add_field(name="Configuration — 4", value="`setup`, `configure`, `remove logchannel`, `remove modrole`", inline=True)
        embed.add_field(name="Settings — 3", value="`configurations`, `prefix`, `resetprefix`", inline=False)
        embed.add_field(name="General — 4", value="`ping`, `botinfo`, `invite`, `privacy`", inline=False)
        embed.set_footer(text=f"Learn more about commands by typing {ctx.prefix}help <command>")
        await ctx.send(embed=embed)

    # help for commands

    @help.command(name="ping")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _ping(self, ctx):
        embed = discord.Embed(title="Ping command", description=f"Gets the Loggy's latency.\n"
                                                                f"\n"
                                                                f"**Aliases**: *None*\n"
                                                                f"**Usage**: `{ctx.prefix}ping`", color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="invite")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _invite(self, ctx):
        embed = discord.Embed(title="Invite command", description=f"Sends an link where you can invite Loggy.\n"
                                                                f"\n"
                                                                f"**Aliases**: Invite, bot-invite, , botinv\n"
                                                                f"**Usage**: `{ctx.prefix}invite`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="botinfo")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _botinfo(self, ctx):
        embed = discord.Embed(title="Botinfo command", description=f"Shows information about the bot.\n"
                                                                f"\n"
                                                                f"**Aliases**: info\n"
                                                                f"**Usage**: `{ctx.prefix}botinfo`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="prefix")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _prefix(self, ctx):
        embed = discord.Embed(title="Prefix command", description=f"Sets a custom prefix for the current guild.\n"
                                                                   f"\n"
                                                                   f"**Aliases**: setprefix, changeprefix\n"
                                                                   f"**Usage**: `{ctx.prefix}prefix <prefix>`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="resetprefix")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _resetprefix(self, ctx):
        embed = discord.Embed(title="Reset prefix command", description=f"Resets the current custom prefix to the default one (if there is one).\n"
                                                                  f"\n"
                                                                  f"**Aliases**: rprefix, defaultprefix\n"
                                                                  f"**Usage**: `{ctx.prefix}resetprefix`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="setup")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _setup(self, ctx):
        embed = discord.Embed(title="Setup command",
                              description=f"Set ups Loggy on this server. Loggy will create a new category with a channel where it logs the events.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"**Usage**: `{ctx.prefix}setup`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="configure")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _configure(self, ctx):
        embed = discord.Embed(title="Configure command",
                              description=f"Configures an configuration/option.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"**Usage**: `{ctx.prefix}configure <configuration>`\n"
                                          f"\n"
                                          f"**Available Configurations**:\n"
                                          f"Logging Channel",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="configurations")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _configurations(self, ctx):
        embed = discord.Embed(title="Configurations command",
                              description=f"Lists all configurations and if they are enabled or not.\n"
                                          f"\n"
                                          f"**Aliases**: configs, config\n"
                                          f"**Usage**: `{ctx.prefix}configurations`\n",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="remove")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _remove(self, ctx):
        embed = discord.Embed(title="Remove command",
                              description=f"Removes/Disables a configuration.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"**Usage**: `{ctx.prefix}remove <configuration>`\n"
                                          f"\n"
                                          f"**Available Configurations**:\n"
                                          f"Logging Channel",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    # event help

    @help.command(name="member_join")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _member_join(self, ctx):
        embed = discord.Embed(title="Member Join Event", description=f"Logs whenever a member joins the server.\n"
                                                                   f"\n"
                                                                   f"**Aliases**: *None*\n"
                                                                     f"To enable the event type `{ctx.prefix}event member_join`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="member_leave")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _member_leave(self, ctx):
        embed = discord.Embed(title="Member Leave Event", description=f"Logs whenever a member leaves the server.\n"
                                                                     f"\n"
                                                                     f"**Aliases**: *None*\n"
                                                                     f"To enable the event type `{ctx.prefix}event member_leave`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="member_update")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _member_update(self, ctx):
        embed = discord.Embed(title="Member Update Event", description=f"Logs whenever a member changes the following things:\n"
                                                                       f"• nickname"
                                                                       f"• roles"
                                                                     f"\n"
                                                                     f"**Aliases**: *None*\n"
                                                                     f"To enable the event type `{ctx.prefix}event member_update`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="member_ban")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _member_ban(self, ctx):
        embed = discord.Embed(title="Member Ban Event",
                              description=f"Logs whenever a member has been banned.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event member_ban`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="member_unban")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _member_unban(self, ctx):
        embed = discord.Embed(title="Member Unban Event",
                              description=f"Logs whenever a member has been unbanned.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event member_unban`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="channel_create")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _channel_create(self, ctx):
        embed = discord.Embed(title="Channel Create Event",
                              description=f"Logs whenever a channel has been created.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event channel_create`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="channel_delete")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _channel_del(self, ctx):
        embed = discord.Embed(title="Channel Delete Event",
                              description=f"Logs whenever a channel has been deleted.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event channel_delete`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="channel_update")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _channel_upd(self, ctx):
        embed = discord.Embed(title="Channel Update Event",
                              description=f"Logs the following things when a channel is updated:\n"
                                          f"• name\n"
                                          f"• topic"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event channel_update`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="invite_create")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _invite_create(self, ctx):
        embed = discord.Embed(title="Invite Create Event",
                              description=f"Logs whenever an invite is created.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event invite_create`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="invite_delete")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _invite_delete(self, ctx):
        embed = discord.Embed(title="Invite Delete Event",
                              description=f"Logs whenever an invite is deleted.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event invite_delete`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="message_delete")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _message_delete(self, ctx):
        embed = discord.Embed(title="Message Delete Event",
                              description=f"Logs whenever a message is deleted.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event message_delete`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="message_edit")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _message_edit(self, ctx):
        embed = discord.Embed(title="Message Edit Event",
                              description=f"Logs whenever a message is edited.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event message_edit`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="role_create")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _role_create(self, ctx):
        embed = discord.Embed(title="Role Create Event",
                              description=f"Logs whenever a role is created.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event role_create`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="role_delete")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _role_delete(self, ctx):
        embed = discord.Embed(title="Role Delete Event",
                              description=f"Logs whenever a role is deleted.\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event role_delete`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @help.command(name="role_update")
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def _role_update(self, ctx):
        embed = discord.Embed(title="Role Update Event",
                              description=f"Logs the following things when a role is updated:\n"
                                          f"• hoist\n"
                                          f"• mentionable\n"
                                          f"• name\n"
                                          f"\n"
                                          f"**Aliases**: *None*\n"
                                          f"To enable the event type `{ctx.prefix}event role_update`",
                              color=discord.Color.blurple())
        await ctx.send(embed=embed)

    # event help

    # help to commands

    @commands.command(aliases=['PING', 'Ping'])
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed(title="Pong! :ping_pong:", description=f"Loggy's Latency: {round(self.bot.latency * 1000)}ms", color=discord.Color.blurple())
        await ctx.send(embed=embed)

    @commands.command(aliases=['Invite', 'bot-invite', 'Bot-invite', 'Botinv', 'botinv'])
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite Loggy", description="Click [here](https://discord.com/api/oauth2/authorize?client_id=854053068668403753&permissions=8&scope=bot) to invite Loggy in your server!", color=discord.Color.blurple())
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['Botinfo', 'BOTINFO', 'Info', 'info'])
    @commands.guild_only()
    @commands.cooldown(1, 3, BucketType.user)
    async def botinfo(self, ctx):
        users = 0
        for guild in self.bot.guilds:
            users += len(guild.members)
        embed = discord.Embed(color=0x7289da)
        embed.set_author(name="Loggy's Information", icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Prefix", value=f"{ctx.prefix}", inline=False)
        embed.add_field(name="Developer", value="V8 hris#0002", inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Memory", value=f"`{round(psutil.virtual_memory().used / 1048576)} MB`", inline=True)
        embed.add_field(name="Servers", value=f"{len(self.bot.guilds)}", inline=True)
        embed.add_field(name="Users", value=f"{users}", inline=True)
        embed.add_field(name=":link: Links", value="[Invite Loggy](https://discord.com/api/oauth2/authorize?client_id=854053068668403753&permissions=8&scope=bot)", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DefaultCommands(bot))
    print("Loggy Default Cog loaded!")
