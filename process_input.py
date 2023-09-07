import pickle
import discord
from bot_globals import *

def printy(*str):
    print(*str)
    pass

####
#   Only used locally
####
def extract_numbers(input_string):
    result = ""
    is_decimal_seen = False
    
    for char in input_string:
        if char.isdigit():
            result += char
        elif char == '.' and not is_decimal_seen:
            result += char
            is_decimal_seen = True
    
    return result

####
#   Only used locally
####
def is_a_time(num):
    num = extract_numbers(num)
    try:
        float(num)
        return True
    except ValueError:
        return False
    
####
#   Only used locally
####
def just_chars(string):
    ret_str = ""
    for character in string:
        if ord(character.lower()) >= ord('a') and ord(character.lower()) <= ord('z'):
            ret_str += character.lower()
    return ret_str

####
#   Only used locally
####
def get_ret_timeout(option3):
    time_char = ""
    extracted_string = just_chars(option3)
    for char_key, list_value in DAY_HOUR_MINUTE.items():
        for substring in list_value:
            if substring.lower() == extracted_string:
                time_char = char_key
                break
        if time_char:
            break
            
    if time_char:
        raw_time = float(extract_numbers(option3))
        if time_char == "d":
            actual_time = raw_time * DAYS
        elif time_char == "h":
            actual_time = raw_time * HOURS
        elif time_char == "m":
            actual_time = raw_time * MINUTES
        else:
            actual_time = raw_time
        ret_timeout = actual_time
    else:
        ret_timeout = DEFAULT_TIMEOUT_TIME
    return ret_timeout

####
#   Only used locally
####
def format_timeout(ret_timeout):
    ret_timeout = int(ret_timeout)
    # Calculate days, hours, minutes, and seconds
    days, remainder = divmod(ret_timeout, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Create a list to hold the time components
    time_components = []

    # Add days to the list if it's greater than zero
    if days > 0:
        time_components.append(f"{days} day{'s' if days > 1 else ''}")

    # Add hours, minutes, and seconds to the list if they are greater than zero
    if hours > 0:
        time_components.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        time_components.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0:
        time_components.append(f"{seconds} second{'s' if seconds > 1 else ''}")

    # Join the time components into a single string
    prefixes = ["", " and ", ", ", ", ", ", ", ", ", ", "]
    formatted_time = ""
    for ii in range(len(time_components)):
        formatted_time = time_components[ii] + prefixes[ii] + formatted_time
    # formatted_time = ' '.join(time_components)

    return formatted_time

'''

Poll Input to String actually returns more than just the string.

input
    options:
        a list of strings

output
    poll_message:
        a string that says **Poll** [question]\n\n[option1]\n[option2]
    options[0]:
        the body of the message that the user sent
    options[1], options[2]:
        the poll options
    ret_timeout:
        seconds to wait until the poll closes, defaults to DEFAULT_TIMEOUT_TIME

'''
def poll_input_to_string(options, author):
    print("len options: ", len(options))
    if len(options) == 3:
        ret_timeout = DEFAULT_TIMEOUT_TIME
    elif len(options) == 4 and is_a_time(options[3]):
        ret_timeout = get_ret_timeout(options[3])
    elif len(options) == 4 and options[3].lower() == "none":
        ret_timeout = None
    else:
        poll_message = discord.Embed(description=f"**Poll:** Hey {author} did you format this correctly?\n{' | '.join(options)}\n")
        return poll_message, "question", "No", "Yes", DEFAULT_TIMEOUT_TIME/2
    
    # Create poll message
    poll_message = discord.Embed(
        title="Bayesian Poll",
        description=f"{options[0]}\n",
        color=0x00FFFF
    )
    how_to_vote = f"*React to this post with your answer\nVoting is anonymous (your vote will disappear after it is recorded, if it doesn't, click any lingering reactions to clear them and then vote again, a little slower)\nAs long as the poll is open you can change your vote*"
    poll_message.add_field(name="How to vote", value=how_to_vote, inline=False)
    poll_message.add_field(name=REACT_EMOJIS[0], value=options[1], inline=True)
    if R_E_ODD:
        poll_message.add_field(name=REACT_EMOJIS[R_E_HALF], value="Neutral", inline=True)
    poll_message.add_field(name=REACT_EMOJIS[-1], value=options[2], inline=True)
    
    poll_message.set_author(name=f"{author} asks...")
    poll_message.set_footer(text=f"Vote now! This poll is open for {format_timeout(ret_timeout)} or until everyone has voted, which never happens :(")

    print("returning a timeout of: ",ret_timeout," which is in seconds")
    return poll_message, options[0], options[1], options[2], ret_timeout


'''

get server settings from pkl
save server settings pkl

'''
# load configuration settings per server
def get_server_settings_pkl():
    try:
        print("Trying to load server settings")
        SERVER_SETTINGS = pickle.load(open("server_settings.pickle", "rb"))
    except (OSError, IOError) as e:
        SERVER_SETTINGS = {}
        pickle.dump(SERVER_SETTINGS, open("server_settings.pickle", "wb"))
    print("server settings:\n",SERVER_SETTINGS)
    return SERVER_SETTINGS
# save configuration settings per server
def save_server_settings_pkl(SERVER_SETTINGS):
    pickle.dump(SERVER_SETTINGS, open("server_settings.pickle", "wb"))


'''

configure a channel

'''
def configure_channel(ctx, post_channel, channel):
    SERVER_SETTINGS = get_server_settings_pkl()
    if ctx.message.author.guild_permissions.administrator:
        server_id = ctx.guild.id
        if server_id in SERVER_SETTINGS:
            SERVER_SETTINGS[server_id][post_channel] = channel.id
        else:
            SERVER_SETTINGS[server_id] = {
                post_channel: channel.id
            }
        pickle.dump(SERVER_SETTINGS, open("server_settings.pickle", "wb"))
        if 'poll' in post_channel:
            stuff = "Polls"
        elif 'result' in post_channel:
            stuff = "Results"
        else:
            stuff = "WHAT IS THIS SHIT"
        ret_message = f"{stuff} will now be posted in {channel.mention}"
    else:
        ret_message = f"You don't have permission to configure settings."
    return ret_message