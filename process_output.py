from bot_globals import *

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