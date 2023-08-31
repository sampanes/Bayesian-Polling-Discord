import discord
from discord.ext import commands
import logging
import asyncio

# Configure logging to display debug messages
logging.basicConfig(level=logging.DEBUG)

token = 'MTE0NjA3MzkzNzYyOTk0NTg4Ng.GJTZhx.ePcD5sIqKKT0i4-FAvCbO2NhsxfH-kH2o682fc'

REACT_EMOJIS = ["🌕", "🌖", "🌗", "🌘", "🌑", "🌒", "🌓", "🌔", "🌝"]
MAX_STARS = 15
MINUTES = 60 * 1
HOURS = 60 * MINUTES
DEFAULT_TIMEOUT_TIME = 24 * HOURS

intents = discord.Intents.default()
intents.typing = False
intents.message_content = True
intents.presences = True  # Add this line for Presence Intent
intents.members = True  # Add this line for Server Members Intent

bot = commands.Bot(command_prefix='!', intents=intents)

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def poll_input_to_string(options):
    if len(options) == 3:
        ret_timeout = DEFAULT_TIMEOUT_TIME
    elif len(options) == 4 and is_float(options[3]):
        ret_timeout = float(options[3])
    elif len(options) == 4 and options[3].lower() == "none":
        ret_timeout = None
    else:
        poll_message = f"**Poll:** did you format this correctly?\n{' | '.join(options)}\n"
        return poll_message, "question", "No", "Yes", DEFAULT_TIMEOUT_TIME/2
    
    # Create poll message
    o1 = "🌕: {}".format(options[1])
    o2 = "🌝: {}".format(options[2])
    poll_message = f"**Poll:** {options[0]}\n\n{o1}\n{o2}"
    return poll_message, options[0], options[1], options[2], ret_timeout

def get_result_text(server_members_react_dict, o1, o2):
    # Process the poll results
    result_text = f"Poll Results:\n"
    # Create a dictionary to store reaction counts
    reaction_counts_dict = {emoji: 0 for emoji in REACT_EMOJIS}

    percent_dict = {emoji: 0.0 for emoji in REACT_EMOJIS}
    for step in range(len(REACT_EMOJIS)):
        percent_dict[REACT_EMOJIS[step]] = (100.0 / (float(len(REACT_EMOJIS)-1)) * step)

    total_voters = 0
    max_count = 0
    for user_key, reaction_value in server_members_react_dict.items():
        reaction_counts_dict[reaction_value.emoji] += 1
        max_count = max(max_count, reaction_counts_dict[reaction_value.emoji])
        total_voters+=1
    total_percent = 0
    star_per_count = float(MAX_STARS) / float(max_count)
    for emoji_key, percent_value in percent_dict.items():
        total_percent+=percent_value * reaction_counts_dict[emoji_key]
        result_text+=f"`{'~{:6.2f}:'.format(percent_value)}"
        result_text+="#"*(int(star_per_count * reaction_counts_dict[emoji_key]))+"`\n"
    final_p = total_percent/total_voters
    result_text+=f"{'{:6.2f}%'.format(final_p if final_p > 50 else 100 - final_p)}"
    result_text+=" so a dead tie" if final_p == 50.0 else (f" favorability for \"{o2 if final_p > 50.0 else o1}\"")
    return result_text


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
