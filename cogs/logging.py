import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

blurple = discord.Color.blurple()


class LoggyBot(commands.Cog, name="Loggy Main"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_join FROM main WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {member.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                embed = discord.Embed(description=f"<:LoggyMemberJoin:854384221475700737> {member.mention} has joined the server.\n"
                                                                                            f"\n"
                                                                                            f"**Account Created:**\n"
                                                                                            f"{member.created_at.__format__('%A, %d. %B %Y at %H:%M:%S')}", color=discord.Color.green())
                embed.set_footer(text=f"User ID: {member.id} | Members: {member.guild.member_count}")
                embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                embed.timestamp = datetime.utcnow()

                channel = self.bot.get_channel(id=int(result1[0]))

                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_leave FROM main WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {member.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                embed = discord.Embed(
                    description=f"<:LoggyMemberLeave:854397294001913916> {member.mention} left the server.\n"
                                f"\n"
                                f"**Left Date:**\n"
                                f"{datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S')}",
                    color=discord.Color.red())
                embed.set_footer(text=f"User ID: {member.id} | Members: {member.guild.member_count}")
                embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                embed.timestamp = datetime.utcnow()

                channel = self.bot.get_channel(id=int(result1[0]))

                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_update FROM main WHERE guild_id = {before.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {before.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                if before.nick != after.nick:
                    embed = discord.Embed(description=f"{before.mention} nickname changed", color=discord.Color.green())
                    embed.add_field(name="Nickname Before", value=before.nick)
                    embed.add_field(name="Nickname After", value=after.nick)
                    embed.set_footer(text=f"User ID: {before.id}")
                    embed.set_author(name=f"{before}", icon_url=before.avatar_url)
                    embed.timestamp = datetime.utcnow()
                    channel = self.bot.get_channel(id=int(result1[0]))

                    await channel.send(embed=embed)
                channel = self.bot.get_channel(id=int(result1[0]))
                for roles in before.roles:
                    if roles not in after.roles:
                        embed = discord.Embed(description=f"{after.mention} was removed the **{roles.mention}** role.",
                                              color=discord.Color.red())
                        embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'))
                        embed.set_footer(text=f"User ID: {before.id}")
                        embed.set_author(name=before, icon_url=before.avatar_url)
                        embed.timestamp = datetime.utcnow()
                        await channel.send(embed=embed)
                for roles in after.roles:
                    if roles not in before.roles:
                        embed = discord.Embed(description=f"{before.mention} was given the **{roles.mention}** role.", color=discord.Color.green())
                        embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'))
                        embed.set_footer(text=f"User ID: {before.id}")
                        embed.set_author(name=before, icon_url=before.avatar_url)
                        embed.timestamp = datetime.utcnow()
                        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_ad FROM main WHERE guild_id = {channel.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {channel.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                embed = discord.Embed(description=f"Channel {channel.mention} has been created.", color=discord.Color.orange())
                embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'))
                embed.set_footer(text=f"Channel ID: {channel.id}")
                embed.set_author(name=f"{channel}", icon_url=channel.guild.icon_url)
                embed.timestamp = datetime.utcnow()
                channel1 = self.bot.get_channel(id=int(result1[0]))
                await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_del FROM main WHERE guild_id = {channel.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {channel.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                embed = discord.Embed(description=f"Channel **#{channel.name}** has been deleted.", color=discord.Color.red())
                embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'))
                embed.set_footer(text=f"Channel ID: {channel.id}")
                embed.set_author(name=f"{channel}", icon_url=channel.guild.icon_url)
                embed.timestamp = datetime.utcnow()
                channel1 = self.bot.get_channel(id=int(result1[0]))
                await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_update FROM main WHERE guild_id = {before.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {before.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                if before.name != after.name:
                    embed = discord.Embed(description=f"", color=discord.Color.orange())
                    embed.add_field(name="Channel Edited", value=f"{after.mention}", inline=False)
                    embed.add_field(name="Channel Name Before", value=before.name)
                    embed.add_field(name="Channel Name After", value=after.name)
                    embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'), inline=False)
                    embed.set_footer(text=f"Channel ID: {before.id}")
                    embed.set_thumbnail(url=before.guild.icon_url)
                    embed.set_author(name=f"{before.guild}", icon_url=before.guild.icon_url)
                    embed.timestamp = datetime.utcnow()
                    channel1 = self.bot.get_channel(id=int(result1[0]))
                    await channel1.send(embed=embed)
                if before.topic != after.topic:
                    embed = discord.Embed(description=f"", color=discord.Color.orange())
                    embed.add_field(name="Channel Edited", value=f"{after.mention}", inline=False)
                    embed.add_field(name="Channel Topic Before", value=before.topic)
                    embed.add_field(name="Channel Topic After", value=after.topic)
                    embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'), inline=False)
                    embed.set_footer(text=f"Channel ID: {before.id}")
                    embed.set_thumbnail(url=before.guild.icon_url)
                    embed.set_author(name=f"{before.guild}", icon_url=before.guild.icon_url)
                    embed.timestamp = datetime.utcnow()
                    channel1 = self.bot.get_channel(id=int(result1[0]))
                    await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_create FROM main WHERE guild_id = {role.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {role.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                    embed = discord.Embed(description=f"Role {role.mention} has been created.", color=discord.Color.green())
                    embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'), inline=False)
                    embed.set_footer(text=f"Role ID: {role.id}")
                    embed.set_author(name=f"{role.guild}", icon_url=role.guild.icon_url)
                    embed.timestamp = datetime.utcnow()
                    channel1 = self.bot.get_channel(id=int(result1[0]))
                    await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_del FROM main WHERE guild_id = {role.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {role.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                    embed = discord.Embed(description=f"Role **@{role.name}** has been deleted.", color=discord.Color.red())
                    embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'), inline=False)
                    embed.set_footer(text=f"Role ID: {role.id}")
                    embed.set_author(name=f"{role.guild}", icon_url=role.guild.icon_url)
                    embed.timestamp = datetime.utcnow()
                    channel1 = self.bot.get_channel(id=int(result1[0]))
                    await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT role_update FROM main WHERE guild_id = {before.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {before.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                if before.name != after.name:
                    embed = discord.Embed(description=f"", color=discord.Color.green())
                    embed.add_field(name="Role Edited", value=f"{before.mention} ({before.id})", inline=False)
                    embed.add_field(name="Role Name Before", value=before.name)
                    embed.add_field(name="Role Name After", value=after.name)
                    embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'), inline=False)
                    embed.set_footer(text=f"Role ID: {before.id}")
                    embed.set_author(name=f"{before.guild}", icon_url=before.guild.icon_url)
                    embed.timestamp = datetime.utcnow()
                    channel1 = self.bot.get_channel(id=int(result1[0]))
                    await channel1.send(embed=embed)
                if before.mentionable != after.mentionable:
                    embed = discord.Embed(description=f"", color=discord.Color.green())
                    embed.add_field(name="Role Edited", value=f"{before.mention} ({before.id})", inline=False)
                    embed.add_field(name="Role Mentionable Before", value=f"{':white_check_mark:' if before.mentionable else ':x:'}")
                    embed.add_field(name="Role Mentionable After", value=f"{':white_check_mark:' if after.mentionable else ':x:'}")
                    embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'),
                                    inline=False)
                    embed.set_footer(text=f"Role ID: {before.id}")
                    embed.set_author(name=f"{before.guild}", icon_url=before.guild.icon_url)
                    embed.timestamp = datetime.utcnow()
                    channel1 = self.bot.get_channel(id=int(result1[0]))
                    await channel1.send(embed=embed)
                if before.hoist != after.hoist:
                    embed = discord.Embed(description=f"", color=discord.Color.orange())
                    embed.add_field(name="Role Edited", value=f"{before.mention} ({before.id})", inline=False)
                    embed.add_field(name="Role Hoist Before",
                                    value=f"{':white_check_mark:' if before.hoist else ':x:'}")
                    embed.add_field(name="Role Hoist After",
                                    value=f"{':white_check_mark:' if after.hoist else ':x:'}")
                    embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'),
                                    inline=False)
                    embed.set_footer(text=f"Role ID: {before.id}")
                    embed.set_author(name=f"{before.guild}", icon_url=before.guild.icon_url)
                    embed.timestamp = datetime.utcnow()
                    channel1 = self.bot.get_channel(id=int(result1[0]))
                    await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT message_del FROM main WHERE guild_id = {message.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {message.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                embed = discord.Embed(title="",
                                      description=f":wastebasket: **Message sent by** {message.author.mention} **deleted in** <#{message.channel.id}>\n"
                                                  f"{message.content}\n"
                                                  f"\n"
                                                  f"**Message Date**\n"
                                                  f"{datetime.utcnow().__format__('%b %d, %Y %H:%M:%S')}",
                                      color=discord.Color.red())
                embed.set_footer(text=f"Author ID: {message.author.id} | Message ID: {message.id}")
                embed.set_author(name=f"{message.author}", icon_url=message.author.avatar_url)
                embed.timestamp = datetime.utcnow()

                channel = self.bot.get_channel(int(result1[0]))

                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT message_edit FROM main WHERE guild_id = {before.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {before.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                editembed = discord.Embed(
                    description=f":keyboard: **[Message](https://canary.discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}) sent by** {before.author.mention} **was edited in** <#{before.channel.id}>",
                    color=discord.Color.orange())
                editembed.add_field(name='Old message', value=before.content or "No content.", inline=False)
                editembed.add_field(name="New message", value=after.content or "No content.", inline=False)
                editembed.set_author(name=f'{before.author.name}#{before.author.discriminator}',
                                     icon_url=before.author.avatar_url)
                editembed.set_footer(text=f"Author ID: {before.author.id} • Message ID: {before.id}")
                editembed.timestamp = datetime.utcnow()

                channel = self.bot.get_channel(int(result1[0]))

                await channel.send(embed=editembed)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT emoji FROM main WHERE guild_id = {guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                for emoji in guild.before.emojis:
                    if emoji not in guild.after.emojis:
                        embed = discord.Embed(description=f"Emoji {emoji} has been removed.",
                                              color=discord.Color.red())
                        embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'))
                        embed.set_footer(text=f"Emoji ID: {emoji.id}")
                        embed.set_author(name=emoji, icon_url=guild.avatar_url)
                        embed.timestamp = datetime.utcnow()
                        channel1 = self.bot.get_channel(id=int(result1[0]))
                        await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_ban FROM main WHERE guild_id = {guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
                logs = logs[0]
                if logs.target == member:
                    embed = discord.Embed(color=discord.Color.red(), description=f"{member.mention} has been banned from {logs.user.mention}.")
                    embed.add_field(name="Reason", value=f"{logs.reason}", inline=False)
                    embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'))
                    embed.timestamp = datetime.utcnow()
                    embed.set_footer(text=f"Member ID: {member.id}")
                    embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                    channel1 = self.bot.get_channel(id=int(result1[0]))
                    await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT member_unban FROM main WHERE guild_id = {guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                    embed = discord.Embed(color=discord.Color.blurple(), description=f"{user} has been unbanned.")
                    embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'))
                    embed.timestamp = datetime.utcnow()
                    embed.set_footer(text=f"User ID: {user.id}")
                    embed.set_thumbnail(url=guild.icon_url)
                    embed.set_author(name=f"{user}", icon_url=user.avatar_url)
                    channel1 = self.bot.get_channel(id=int(result1[0]))
                    await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT invite_create FROM main WHERE guild_id = {invite.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {invite.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                embed = discord.Embed(description="", color=discord.Color.blurple())
                embed.add_field(name="Invite Details", value=f"Invite {invite}\n"
                                                             f"Invite Author: {invite.inviter.mention}\n"
                                                             f"Invite for Channel: {invite.channel.mention}\n"
                                                             f"Invite Max uses: {'No Limit' if invite.max_uses == 0 else f'{invite.max_uses}'}\n", inline=False)
                embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'))
                embed.set_author(name=f"{invite.guild}", icon_url=invite.guild.icon_url)
                embed.set_footer(text=f"URL: {invite.url}")
                embed.set_thumbnail(url=invite.guild.icon_url)
                embed.timestamp = datetime.utcnow()
                channel1 = self.bot.get_channel(id=int(result1[0]))
                await channel1.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        db = sqlite3.connect('./db/loggy.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT invite_del FROM main WHERE guild_id = {invite.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        if str(result[0]) == "on":
            db1 = sqlite3.connect('./db/loggy.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT logchannel FROM main WHERE guild_id = {invite.guild.id}")
            result1 = cursor1.fetchone()
            if result1 is None:
                return
            else:
                embed = discord.Embed(description="", color=discord.Color.blurple())
                embed.add_field(name="Deleted Invite Details", value=f"Invite {invite}\n"
                                                             f"Invite Author: {invite.inviter.mention}\n"
                                                             f"Invite Channel: {invite.channel.mention}\n"
                                                             f"Invite Created At: {invite.created_at}", inline=False)
                embed.add_field(name="Date", value=datetime.utcnow().__format__('%A, %d. %B %Y at %H:%M:%S'))
                embed.set_author(name=f"{invite.guild}", icon_url=invite.guild.icon_url)
                embed.set_footer(text=f"URL: {invite.url}")
                embed.set_thumbnail(url=invite.guild.icon_url)
                embed.timestamp = datetime.utcnow()
                channel1 = self.bot.get_channel(id=int(result1[0]))
                await channel1.send(embed=embed)


def setup(bot):
    bot.add_cog(LoggyBot(bot))
    print("Loggy Logging Cog loaded!")
