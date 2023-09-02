import discord
from discord.ext import commands
import logging
import asyncio
from bot_globals import *
from bot_token import BAYESIAN_BOT_TOKEN
from command_constants import COMMANDS_AND_DESCRIPTIONS
from process_input import (
    get_server_settings_pkl,
    save_server_settings_pkl,
    poll_input_to_string,
    configure_channel
)
from process_output import get_result_text

# Configure logging to display debug messages
logging.basicConfig(level=logging.DEBUG)

token = BAYESIAN_BOT_TOKEN

intents = discord.Intents.default()
intents.typing = False
intents.message_content = True
intents.presences = True  # Add this line for Presence Intent
intents.members = True  # Add this line for Server Members Intent

bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')
@bot.command(name="bot-help", aliases=["poll-help", "help-poll", "help-bot", "help"])
async def custom_help(ctx):
    help_message = "Hey there! This is a bot by John and here are a few things I can do for you:\n\n"
    
    commands = COMMANDS_AND_DESCRIPTIONS

    for command, description in commands:
        help_message += f"**{command}**: {description}\n\n"
    
    help_embed = discord.Embed(title="Bayesian Polling Bot Help", description=help_message, color=0x3498db)
    help_embed.set_author(name="Bot Commands", icon_url=bot.user.avatar.url)
    help_embed.set_footer(text="_Feel free to ping John for help anytime!_")

    await ctx.send(embed=help_embed)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name="pollchannel", aliases=["postpoll", "post-poll", "postpolls", "post-polls", "pollschannel", "poll-channel", "polls-channel", "channelpoll", "channelpolls"])
async def pollchannel(ctx, channel: discord.TextChannel):
    ret_message = configure_channel(ctx, 'post_poll_channel', channel)
    SERVER_SETTINGS = get_server_settings_pkl()
    save_server_settings_pkl(SERVER_SETTINGS)
    print("User entered Polling channel:\n",SERVER_SETTINGS)
    await ctx.send(ret_message)

@bot.command(name="resultchannel", aliases=["postresult", "post-result", "postresults", "post-results", "resultschannel", "result-channel", "results-channel", "channelresult", "channelresults"])
async def resultschannel(ctx, channel: discord.TextChannel):
    ret_message = configure_channel(ctx, 'post_results_channel', channel)
    SERVER_SETTINGS = get_server_settings_pkl()
    save_server_settings_pkl(SERVER_SETTINGS)
    print("User entered Results channel:\n",SERVER_SETTINGS)
    await ctx.send(ret_message)

@bot.command()
async def poll(ctx, *options):
    SERVER_SETTINGS = get_server_settings_pkl()
    server_id = ctx.guild.id

    # check if post poll and post result channels are configured
    if server_id in SERVER_SETTINGS \
        and 'post_poll_channel' in SERVER_SETTINGS[server_id] \
        and 'post_results_channel' in SERVER_SETTINGS[server_id]:

        # Create poll message
        poll_embed, question, o1, o2, timeout_time = poll_input_to_string(options, ctx.author)

        # Get Poll Channel
        poll_channel_id = SERVER_SETTINGS[server_id]['post_poll_channel']
        poll_channel = bot.get_channel(poll_channel_id)
        if not poll_channel:
            poll_channel = ctx
            await poll_channel.send("The configured poll channel doesn't exist. posting poll here")
        elif not poll_channel.permissions_for(poll_channel.guild.me).send_messages:
            await ctx.send(f"I guess this bot cannnot post in {poll_channel.mention}")
            poll_channel = ctx

        # Poll channel members
                # Get the list of all users in the server
        poll_channel_members = []
        for member in ctx.guild.members:
            # Check if the member has permission to view the channel
            permissions = poll_channel.permissions_for(member)
            if permissions.view_channel:
                poll_channel_members.append(member)
        

        # Get Results Channel
        results_channel_id = SERVER_SETTINGS[server_id]['post_results_channel']
        results_channel = bot.get_channel(results_channel_id)
        if not results_channel:
            results_channel = ctx
            await results_channel.send("The configured result channel doesn't exist. posting poll results here")
        elif not results_channel.permissions_for(results_channel.guild.me).send_messages:
            await ctx.send(f"I guess this bot cannnot post in {results_channel.mention}")
            results_channel = poll_channel
        
        # Post the poll, keep poll_msg variable to keep interacting with it
        poll_msg = await poll_channel.send(embed=poll_embed)

        # Add emoji reactions for voting
        for emoji in REACT_EMOJIS:
            await poll_msg.add_reaction(emoji)

        # Define a check function to ensure the reaction is valid
        def check(reaction, user):
            return user != bot.user and str(reaction.emoji) in REACT_EMOJIS

        # THE MEAT OF THE OPERATION
        poll_channel_members_react_dict = {}
        try:
            # Wait for reactions from users
            while poll_channel_members:
                reaction, user = await bot.wait_for('reaction_add', timeout=timeout_time, check=check)
                await reaction.remove(user)  # Remove user's reaction

                # Check if the user is a member of the server
                if user in poll_channel_members:
                    poll_channel_members.remove(user)
                poll_channel_members_react_dict[user] = reaction

        except asyncio.TimeoutError:
            #await poll_channel.send(f"`{o1}`\nor\n`{o2}`?\nVoting Closed, check {results_channel.mention} for results")
            pass #TODO what to do after timeout

        if poll_msg.embeds:
            embed = poll_msg.embeds[0]
            if embed.footer:
                embed.set_footer(text=f"Voting ended, see results in #{results_channel.name}")
                await poll_msg.edit(embed=embed)
        
        result_embed = get_result_text(poll_channel_members_react_dict, ctx.author, question, o1, o2)

        # Send the poll results
        await results_channel.send(embed=result_embed)
    else:
        print(f"server id {server_id}")
        print(f"server settings dict {SERVER_SETTINGS}")
        await ctx.send("No poll or result channel has been configured for this server.\n!pollchannel #channel and !resultchannel #channel")
        return


# Run the bot with your token
bot.run(token)
