import discord
from discord.ext import commands
import logging
import asyncio
from bot_token import BAYESIAN_BOT_TOKEN
from bot_globals import *
from process_input import poll_input_to_string
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

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.remove_command('help')
@bot.command(name="bot-help", aliases=["poll-help", "help-poll", "help-bot", "help"])
async def custom_help(ctx):
    help_message = "Hey there! This is a bot by John and here are a few things I can do for you:\n\n"
    
    poll_descr = f'''type !poll "_body in quotes_" "_option nofacemoon_" "_option smilemoon_"
    Poll body: describe what you want public opinion on.
    Emojis: {REACT_EMOJIS[0]} >>> {REACT_EMOJIS[-1]} are strengths of opinion, 🌑 is neutral
    Command examples (don't forget quotes):
    `!poll "best pet" "dogs" "cats"`
    `!poll "should I eat donut" "nah" "bet"`
    `!poll "age" "0" "90"`
    these are the  for voting, first option is left, second option is right
    {''.join(REACT_EMOJIS)}'''
    # List of commands and their descriptions
    commands = [
        ("!ping", "Check if I'm alive and kicking!"),
        ("!poll", poll_descr),
        # Add more commands and descriptions here
    ]
    
    for command, description in commands:
        help_message += f"**{command}**: {description}\n\n"
    
    help_embed = discord.Embed(title="Bayesian Polling Bot Help", description=help_message, color=0x3498db)
    help_embed.set_author(name="Bot Commands", icon_url=bot.user.avatar.url)
    help_embed.set_footer(text="_Feel free to ask for help anytime!_")

    await ctx.send(embed=help_embed)


@bot.command()
async def poll(ctx, *options):
    # Create poll message
    poll_message, question, o1, o2, timeout_time = poll_input_to_string(options)

    # Send poll message
    poll_embed = discord.Embed(description=poll_message)
    poll_embed.set_author(name="Bayesian Preference Poll")
    poll_msg = await ctx.send(embed=poll_embed)

    # Add emoji reactions for voting
    for emoji in REACT_EMOJIS:
        await poll_msg.add_reaction(emoji)

    # Define a check function to ensure the reaction is valid
    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) in REACT_EMOJIS

    try:
        # Get the list of all users in the server
        server_members = list(ctx.guild.members)
        server_members_react_dict = {}

        # Wait for reactions from users
        while server_members:
            reaction, user = await bot.wait_for('reaction_add', timeout=timeout_time, check=check)
            await reaction.remove(user)  # Remove user's reaction

            # Check if the user is a member of the server
            if user in server_members:
                server_members.remove(user)
            server_members_react_dict[user] = reaction

    except asyncio.TimeoutError:
        await ctx.send("Voting Closed")

    # Fetch the poll message again
    poll_msg = await ctx.channel.fetch_message(poll_msg.id)

    result_text = f"**{question}**\n\n{o1}\nvs\n{o2}\n\n--------------------------"
    result_text += get_result_text(server_members_react_dict, o1, o2)

    # Send the poll results
    await ctx.send(result_text)


# Run the bot with your token
bot.run(token)
