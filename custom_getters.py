import discord

def get_channel_or_default(SERVER_SETTINGS, bot, ctx, channel_string):
    message = ""
    poll_channel_id = SERVER_SETTINGS[ctx.guild.id][channel_string]
    poll_channel = bot.get_channel(poll_channel_id)
    if not poll_channel:
        poll_channel = ctx
        message = f"{channel_string} error: The configured channel doesn't exist. posting here"
    elif not poll_channel.permissions_for(poll_channel.guild.me).send_messages:
        message = f"{channel_string} error: I guess this bot cannnot post in {poll_channel.mention}"
        poll_channel = ctx
    return poll_channel, message