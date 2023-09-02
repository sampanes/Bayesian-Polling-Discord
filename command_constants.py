from bot_globals import *

poll_descr = f'''type !poll "_body in quotes_" "_option nofacemoon_" "_option smilemoon_"
Poll body: describe what you want public opinion on.
Emojis: {REACT_EMOJIS[0]} >>> {REACT_EMOJIS[-1]} are strengths of opinion, 🌑 is neutral
Command examples (don't forget quotes):
`!poll "best pet" "dogs" "cats"`
`!poll "should I eat donut" "nah" "bet" "3600 seconds"` <-optional, default: {DEFAULT_TIMEOUT_TIME}
`!poll "age" "0" "90"`
these are the emojis for voting, first option is left, second option is right
{''.join(REACT_EMOJIS)}'''

poll_channel = f'''type `!pollchannel #` and then select the channel where polls should go (only need to do this once)'''

results_channel = f'''type `!resultschannel #` and then select the channel where poll results should go (only need to do this once)'''

# List of commands and their descriptions
COMMANDS_AND_DESCRIPTIONS = [
    ("!ping", "Check if I'm alive and kicking!"),
    ("!poll", poll_descr),
    ("!pollchannel", poll_channel),
    ("!resultschannel", results_channel)
    # Add more commands and descriptions here
]