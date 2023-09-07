import discord
from discord.ext import commands
import logging
import asyncio
import time
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
from custom_getters import get_channel_or_default

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
    commands = COMMANDS_AND_DESCRIPTIONS

    help_embed = discord.Embed(title="Bayesian Polling Bot Help", description=f"Hey there! This is a bot by John and here are a few things I can do for you:", color=0x3498db)

    for command, description in commands:
        help_embed.add_field(name=f"**{command}**", value=f"{description}\n", inline=False)
    
    help_embed.set_author(name=f"Hey {ctx.author}", icon_url=bot.user.avatar.url)
    help_embed.set_footer(text="Feel free to ping John for help anytime!")

    await ctx.send(embed=help_embed)

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert to milliseconds and round
    await ctx.send(f"Pong! Latency is {latency}ms")

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

@bot.command(name="poll", aliases=["pol", "makepoll", "polls", "ask"])
async def poll(ctx, *options):
    SERVER_SETTINGS = get_server_settings_pkl()
    server_id = ctx.guild.id

    if not options:
        error_msg = discord.Embed(title="Bayesian Polling Bot Help", description=f"Hey there! This is a bot by John and here are a few things I can do for you:", color=0x3498db)
        for command, description in COMMANDS_AND_DESCRIPTIONS:
            if command == "!poll":
                error_msg.add_field(name=f"**{command}**", value=f"{description}\n", inline=False)
                break
        else:
            error_msg.add_field(f"somehow `!poll` is not in the help list at all :(")
        error_msg.set_author(name=f"Hey {ctx.author}", icon_url=bot.user.avatar.url)
        error_msg.set_footer(text="Feel free to ping John for help anytime!")
        await ctx.send(embed=error_msg)
        return

    # check if post poll and post result channels are configured
    if server_id in SERVER_SETTINGS \
        and 'post_poll_channel' in SERVER_SETTINGS[server_id] \
        and 'post_results_channel' in SERVER_SETTINGS[server_id]:

        # Create poll message
        poll_embed, question, o1, o2, timeout_time = poll_input_to_string(options, ctx.author)

        # Get Poll Channel
        poll_channel, pc_message = get_channel_or_default(SERVER_SETTINGS, bot, ctx, 'post_poll_channel')
        if pc_message:
            await poll_channel.send(pc_message)

        # Poll channel members
                # Get the list of all users in the server
        poll_channel_members = []
        for member in ctx.guild.members:
            # Check if the member has permission to view the channel
            permissions = poll_channel.permissions_for(member)
            if permissions.view_channel:
                poll_channel_members.append(member)
        
        # Get Results Channel
        results_channel, rc_message = get_channel_or_default(SERVER_SETTINGS, bot, poll_channel, 'post_results_channel')
        if rc_message:
            await poll_channel.send(rc_message)
        
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
        # Wait for reactions from users
        brief_timeout = min(MAX_TIME_WAIT, timeout_time)
        break_now = False
        start_time = time.time()
        real_timeout_time = timeout_time
        while poll_channel_members:
            try:
                # print(f"brief_timeout {brief_timeout}\t timeout_time {timeout_time}")
                reaction, user = await bot.wait_for('reaction_add', timeout=brief_timeout, check=check)
                await reaction.remove(user)  # Remove user's reaction
                brief_timeout = min(MAX_TIME_WAIT, (real_timeout_time - (time.time() - start_time)))
                # Check if the user is a member of the server
                if user in poll_channel_members:
                    poll_channel_members.remove(user)
                poll_channel_members_react_dict[user] = reaction

            except asyncio.TimeoutError:
                if break_now:
                    break
                timeout_time = real_timeout_time - (time.time() - start_time)
                if timeout_time > MAX_TIME_WAIT:
                    timeout_time -= MAX_TIME_WAIT
                    brief_timeout = MAX_TIME_WAIT
                else:
                    break_now = True
                    brief_timeout = timeout_time
                #await poll_channel.send(f"`{o1}`\nor\n`{o2}`?\nVoting Closed, check {results_channel.mention} for results")
        end_time = time.time()
        print(f"end - start time: {end_time - start_time} ... {float(end_time - start_time) / 60.0} minutes")

        # edit poll message footer to display that the voting has ended
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
