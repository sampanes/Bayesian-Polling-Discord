from bot_globals import *
import discord

def get_result_text(server_members_react_dict, author, question, o1, o2):
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
    try:
        star_per_count = float(MAX_STARS) / float(max_count)
    except ZeroDivisionError:
        star_per_count = 0
    
    result_text = ""
    for emoji_key, percent_value in percent_dict.items():
        total_percent+=percent_value * reaction_counts_dict[emoji_key]
        result_text+=f"{emoji_key}`{'~{:6.2f}:'.format(percent_value)}"
        result_text+="#"*(int(star_per_count * reaction_counts_dict[emoji_key]))+"`\n"
    try:
        final_p = total_percent/total_voters
    except ZeroDivisionError:
        final_p = 50.0
    outcome1 = f"{'{:6.2f}%'.format(100 - final_p)}%"
    outcome2 = f"{'{:6.2f}%'.format(final_p)}%"

    result_embed = discord.Embed(
        title="Bayesian Poll Results",
        description=question,
        color=0x5900ff   
    )
    result_embed.set_author(name=f"{author} asked:")
    result_embed.add_field(name=f"{REACT_EMOJIS[0]} {outcome1}", value=o1, inline=True)
    if R_E_ODD:
        result_embed.add_field(name=f"{REACT_EMOJIS[R_E_HALF]} {outcome1}", value="Neutral", inline=True)
    result_embed.add_field(name=f"{REACT_EMOJIS[-1]} {outcome2}", value=o2, inline=True)
    result_embed.add_field(name="Outome", value=result_text, inline=False)
    else_text = f"WTF guys, vote goddamn you, what\'s wrong with you? {'Just one vote?!' if total_voters == 1 else 'NO VOTES?!?'} The death of democracy is not an assassination from ambush. It is a slow extinction from apathy, indifference, and undernourishment. You absolute monsters. Shame on every last one of you"
    result_embed.set_footer(text=f"{total_voters} {'person' if total_voters == 1 else 'people'} voted. {'Thanks to everyone who voted!' if total_voters > 1 else else_text}")

    return result_embed