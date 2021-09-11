import asyncio

import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

from discord.ext.commands import BucketType

blurple = discord.Color.blurple()


class LoggyConfigurations(commands.Cog, name="Loggy Configurations"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def remove(self, ctx):
        pass

    @commands.command(aliases=['Setup', 'SETUP'])
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    @commands.cooldown(1, 15, BucketType.user)
    async def setup(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT logchannel, modrole FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result[1] is None:
            embed = discord.Embed(description=f"To setup Loggy you must first set a moderator role.\n"
                                              f"Do this by typing `{ctx.prefix}configure modrole <role>`", color=blurple)
            embed.timestamp = datetime.utcnow()
            return await ctx.send(embed=embed)

        def check(m):
            return m.author.id == ctx.author.id

        embed = discord.Embed(
            description="Alright, let's begin the setup. Enter a name you want, to create a category.", color=blurple)
        msg = await ctx.send(embed=embed)
        try:
                category1 = await self.bot.wait_for('message', check=check, timeout=60.0)
                category2 = await ctx.guild.create_category_channel(category1.content)
                embed = discord.Embed(
                    description="Provide a channel name where Loggy sends the logs in!",
                    color=blurple)
                msg = await ctx.send(embed=embed)
                channel = await self.bot.wait_for('message', check=check, timeout=60.0)
                channel1 = await ctx.guild.create_text_channel(name=channel.content, category=category2)
                role = discord.utils.get(ctx.guild.roles, id=result[1])
                await channel1.set_permissions(self.bot.user, view_channel=True, send_messages=True, read_message_history=True)
                await channel1.set_permissions(role, view_channel=True, send_messages=True, read_message_history=True)
                await channel1.set_permissions(ctx.guild.default_role, view_channel=False)
                #
                if result is None:
                    cursor.execute(f"INSERT INTO main(guild_id, logchannel) VALUES({ctx.guild.id},{channel1.id})")
                if result is not None:
                    cursor.execute(f"UPDATE main SET logchannel = {channel1.id} WHERE guild_id = {ctx.guild.id}")
                    embed = discord.Embed(description=f"Loggy has been successfully set up. Configure Loggy by typing `{ctx.prefix}configure`", color=blurple)
                    await ctx.send(embed=embed)
                    logembed = discord.Embed(title="Loggy Logs", description="Loggy's logging channel has been successfully set up.\n"
                                                                             f"\n"
                                                                             f"You can now configure which events will be logged.\n"
                                                                             f"Enable/Disable the events by typing `{ctx.prefix}event <event>`\n"
                                                                             f"Learn more by entering `{ctx.prefix}event`", color=blurple)
                    await channel1.send(embed=logembed)
                    await channel1.edit(topic="Loggy Logs - every event that you enable will be logged here | For help: https://discord.gg/wQbSAddZd2 | Invite Loggy: https://loggy.gg ")
        except asyncio.TimeoutError:
            embed1 = discord.Embed(title="Setup has failed. Timeouted", color=blurple)
            await msg.edit(embed=embed1)
        db.commit()
        db.close()

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def configure(self, ctx):
        embed = discord.Embed(title="Loggy Available Config Options", color=blurple, description="With Loggy you can configure many things.\n"
                                                                                                 f"You can see all configurations below.")
        embed.add_field(name="General\n",
                        value=f"Moderator Role (**{ctx.prefix}configure modrole <role>**)\n"
                              f"Logging channel (**{ctx.prefix}setup**)\n"
                              f"Custom prefix (**{ctx.prefix}prefix <prefix>**)", inline=False)
        embed.add_field(name="Logging", value=f"Enable and disable each event that Loggy can log.\n"
                                              f"See `{ctx.prefix}event` for more information.\n"
                                              f"You can also enable or disable all events at once!\n")
        embed.set_footer(text=f"for more info on a command type {ctx.prefix}help (command)")
        await ctx.send(embed=embed)

    @remove.command(aliases=['modrole', 'Moderatorrole', 'MR', 'MODROLE', 'Modrole', 'MODERATORROLE'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def mr(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT modrole FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't had a moderator role before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET modrole = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Moderator role has been removed.")
        db.commit()
        db.close()

    @configure.command(aliases=['modrole', 'mr', 'Moderatorrole', 'MR', 'MODROLE', 'Modrole', 'MODERATORROLE'])
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def moderatorrole(self, ctx, role: discord.Role = None):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT modrole FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result:
            if role.id == result[0]:
                return await ctx.send("The provided role is currently your moderator role.")
        if result is None:
            try:
                sql = "INSERT INTO main(guild_id, modrole) VALUES(?,?)"
                val = (ctx.guild.id, role.id)
                embed = discord.Embed(title="",
                                      description=f"Alright, moderator role has been set to {role.mention}!\n",
                                      color=discord.Color.blurple())
                await ctx.send(embed=embed)
            except:
                await ctx.send("Configuration has failed. Please try again.")
        if role is None:
            return await ctx.send("Please provide a role.")
        elif result is not None:
            try:
                sql = "UPDATE main SET modrole = ? WHERE guild_id = ?"
                val = (role.id, ctx.guild.id,)
                embed = discord.Embed(title="", description=f"Moderator role has been updated to {role.mention}\n",
                                      color=discord.Color.blurple())
                await ctx.send(embed=embed)
            except:
                await ctx.send("Updating the moderator role has been failed. Please try again.")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases=['Configurations', 'CONFIGURATIONS', 'configs', 'Configs', 'Config', 'config'])
    @commands.cooldown(1, 2, BucketType.user)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def configurations(self, ctx):
        prefix = sqlite3.connect("./db/prefix.sqlite")
        c = prefix.cursor()
        c.execute(f"SELECT prefix FROM main WHERE guild_id = {ctx.guild.id}")
        res = c.fetchone()
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            embed = discord.Embed(title="Loggy Configurations", color=discord.Color.blurple())
            embed.add_field(name="General Settings",
                            value=f"Custom Prefix: not set\n"
                                  f"Logging Channel: not set\n"
                                  f"Moderator Role: not set",
                            inline=False)
            embed.add_field(name="Logging", value=f"Member Joins <:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104>")
            await ctx.send(embed=embed)
        embed = discord.Embed(title="Loggy Configurations", color=discord.Color.blurple())
        embed.add_field(name="Member & Channel logs",
                        value=f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Member Join' if str(result[3]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Member Join')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Member Leave' if str(result[4]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Member Leave')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Member Update' if str(result[5]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Member Update')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Member Ban' if str(result[18]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Member Ban')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Member Unban' if str(result[19]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Member Unban')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Channel Create' if str(result[6]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Channel Create')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Channel Delete ' if str(result[7]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Channel Delete')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Channel Update' if str(result[8]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Channel Update')}\n", inline=True)
        embed.add_field(name="Other logs", value=f"\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Invite Create' if str(result[10]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Invite Create')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Invite Delete' if str(result[11]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Invite Delete')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Message Delete' if str(result[12]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Message Delete')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Message Edit' if str(result[14]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Message Edit')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Role Create' if str(result[15]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Role Create')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Role Delete' if str(result[16]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Role Delete')}\n"
                              f"{(f'<:LoggyDisabledFalse:854100541105373214><:LoggyEnabled:854100674537848903> Role Update' if str(result[17]) == 'on' else '<:LoggyDisabledTrue:854100540669427793><:LoggyEnabledFalse:854100541134209104> Role Update')}\n")
        embed.add_field(name="General Settings",
                        value=f"{(f'Custom Prefix: not set' if not res else f'Custom Prefix: `{res[0]}`')}\n"
                              f"{(f'Logging Channel: <#{result[1]}>' if result[1] else 'Logging Channel: not set')}\n"
                              f"{(f'Moderator Role: <@&{result[0]}>' if result[0] else 'Moderator Role: not set')}")
        await ctx.send(embed=embed)

    @remove.command(aliases=['Logchannel', 'lc', 'LOGCHANNEL', 'LC', 'modlogchannel', 'Modlogchannel'])
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def logchannel(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT logchannel FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't had a log channel before.")
        if result[0] is not None:
            channel = self.bot.get_channel(result[0])
            await channel.delete()
            cursor.execute(f"UPDATE main SET logchannel = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Logging channel has been removed.")
        db.commit()
        db.close()

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def event(self, ctx):
        embed = discord.Embed(title="Loggy Event Configuration", color=blurple, description="Here is a list which events Loggy can log.\n"
                                                                                            f"To enable an event type `{ctx.prefix}event <event>`\n"
                                                                                            f"To disable an event type `{ctx.prefix}disable-event <event>`\n"
                                                                                            f"You can enable all events at once by entering `{ctx.prefix}event all`\n"
                                                                                            f"Or disable all events by entering `{ctx.prefix}disable-event all`\n"
                                                                                            f"\n"
                                                                                            f"**Events:**\n"
                                                                                            f"member_join\n"
                                                                                            f"member_leave\n"
                                                                                            f"member_update\n"
                                                                                            f"member_ban\n"
                                                                                            f"member_unban\n"
                                                                                            f"channel_create\n"
                                                                                            f"channel_delete\n"
                                                                                            f"channel_update\n"
                                                                                            f"invite_create\n"
                                                                                            f"invite_delete\n"
                                                                                            f"message_delete\n"
                                                                                            f"message_edit\n"
                                                                                            f"role_create\n"
                                                                                            f"role_delete\n"
                                                                                            f"role_update\n")
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f"for more info on events type {ctx.prefix}help (event)")
        await ctx.send(embed=embed)

    # disable events

    @commands.group(invoke_without_command=True, name="disable-event")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def disable_event(self, ctx):
        embed = discord.Embed(title="Disable Events", description=f"Disable events by typing `{ctx.prefix}disable-event <event>`\n"
                                                                  f"Or disable all events by entering `{ctx.prefix}disable-event all`\n"
                                                                  f"You can also find all events by entering `{ctx.prefix}event`\n", color=discord.Color.blurple())
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @disable_event.command(name="member_join")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _member_join(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_join FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Member Join event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET member_join = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Member Join event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="all")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _all(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            await ctx.send("You already disabled all events.")
        if result is not None:
            cursor.execute(f"UPDATE main SET member_join = null, member_leave = null, member_update = null, channel_ad = null, channel_del = null, channel_update = null, invite_create = null, invite_del = null, message_del = null, message_delbulk = null, message_edit = null, role_create = null, role_del = null, role_update = null, member_ban = null, member_unban = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("All events have been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="member_leave")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _member_leave(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_leave FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Member Leave event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET member_leave = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Member Leave event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="member_update")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _member_update(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_update FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Member Update event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET member_update = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Member Update event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="channel_create")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _channel_create(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_ad FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Channel Create event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET channel_ad = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Channel Create event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="channel_delete")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _channel_delete(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_del FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Channel Delete event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET channel_del = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Channel Delete event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="channel_update")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _channel_update(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_update FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Channel Update event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET channel_update = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Channel Update event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="role_create")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _role_create(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_create FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Role Create event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET role_create = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Role Create event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="role_delete")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _role_delete(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_del FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Role Delete event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET role_del = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Role Delete event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="role_update")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _role_update(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_update FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Role Update event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET role_update = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Role Update event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="emoji")
    @commands.guild_only()
    @commands.is_owner()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _emoji(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT emoji FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Emoji event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET emoji = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Emoji event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="invite_create")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _invite_create(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT invite_create FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Invite Create event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET invite_create = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Invite Create event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="invite_delete")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _invite_del(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT invite_del FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Invite Delete event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET invite_del = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Invite Delete event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="message_delete")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _message_del(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT message_del FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Message Delete event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET message_del = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Message Delete event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="message_edit")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _message_edit(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT message_edit FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Message Edit event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET message_edit = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Message Edit event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="member_ban")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _member_ban(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_ban FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Member Ban event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET member_ban = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Member Ban event has been disabled.")
        db.commit()
        db.close()

    @disable_event.command(name="member_unban")
    @commands.guild_only()
    @commands.cooldown(1, 2, BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def _member_unban(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_unban FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if not result[0]:
            return await ctx.send("You didn't enable the Member Unban event before.")
        if result[0] is not None:
            cursor.execute(f"UPDATE main SET member_unban = null WHERE guild_id = {ctx.guild.id}")
            await ctx.send("Member Unban event has been disabled.")
        db.commit()
        db.close()

    # enable events

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 7, BucketType.user)
    async def all(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = "INSERT INTO main(guild_id, member_join, member_leave, member_update, channel_ad, channel_del, channel_update, invite_create, invite_del, message_del, message_delbulk, message_edit, role_create, role_del, role_update, member_ban, member_unban) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            val = (ctx.guild.id, str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"))
            embed = discord.Embed(description="All events has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET member_join = ?, member_leave = ?, member_update = ?, channel_ad = ?, channel_del = ?, channel_update = ?, invite_create = ?, invite_del = ?, message_del = ?, message_delbulk = ?, message_edit = ?, role_create = ?, role_del = ?, role_update = ?, member_ban = ?, member_unban = ? WHERE guild_id = ?"
            val = (str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), str("on"), ctx.guild.id)
            embed = discord.Embed(description="All events has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def member_join(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_join FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event member_join` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, member_join) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Member Join event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET member_join = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Member Join event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def member_leave(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_leave FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event member_leave` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, member_leave) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Member Leave event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET member_leave = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Member Leave event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def member_update(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_update FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event member_update` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, member_update) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Member Update event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET member_update = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Member Update event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command(name="channel_create")
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def _channel_add(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_ad FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event channel_create` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, channel_ad) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Channel Create event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET channel_ad = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Channel Create event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def channel_delete(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_del FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event channel_delete` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, channel_del) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Channel Delete event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET channel_del = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Channel Delete event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def channel_update(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_update FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event channel_update` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, channel_update) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Channel Update event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET channel_update = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Channel Update event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def role_create(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_create FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event role_create` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, role_create) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Role Create event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET role_create = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Role Create event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def role_delete(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_del FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event role_delete` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, role_del) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Role Delete event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET role_del = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Role Delete event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def role_update(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_update FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event role_update` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, role_update) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Role Update event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET role_update = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Role Update event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.is_owner()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def emoji(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT emoji FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event emoji` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, emoji) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Role Update event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET emoji = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Emoji event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def invite_create(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT invite_create FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event invite_create` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, invite_create) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Invite Create event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET invite_create = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Invite Create event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def invite_delete(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT invite_del FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event invite_delete` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, invite_del) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Invite Delete event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET invite_del = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Invite Delete event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def message_delete(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT message_del FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event message_delete` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, message_del) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Invite Delete event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET message_del = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Invite Delete event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def message_edit(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT message_edit FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event message_edit` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, message_edit) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Message Edit event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET message_edit = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Message Edit event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def member_ban(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_ban FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event member_ban` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, member_ban) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Member Ban event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET message_ban = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Member Ban event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    @event.command()
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 2, BucketType.user)
    async def member_unban(self, ctx):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_unban FROM main WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if str(result[0]) == "on":
            embed = discord.Embed(
                description=f"You already enabled this event. Enter `{ctx.prefix}disable-event member_unban` to remove it.",
                color=blurple)
            return await ctx.send(embed=embed)
        if result is None:
            sql = "INSERT INTO main(guild_id, member_unban) VALUES(?,?)"
            val = (ctx.guild.id, str("on"))
            embed = discord.Embed(description="Member Unban event has been successfully enabled.", color=blurple)
            await ctx.send(embed=embed)
        if result is not None:
            sql = "UPDATE main SET member_unban = ? WHERE guild_id = ?"
            val = (str("on"), ctx.guild.id)
            embed = discord.Embed(description="Member Unban event has been enabled.", color=blurple)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    # enable events


def setup(bot):
    bot.add_cog(LoggyConfigurations(bot))
    print("Loggy Configuration Cog loaded!")