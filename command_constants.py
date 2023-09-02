from bot_globals import *

poll_descr = f'''type !poll "_body in quotes_" "_option nofacemoon_" "_option smilemoon_"
Poll body: describe what you want public opinion on.
Emojis: {REACT_EMOJIS[0]} >>> {REACT_EMOJIS[-1]} are strengths of opinion, 🌑 is neutral
Command examples (don't forget quotes):
`!poll "best pet" "dogs" "cats"`
`!poll "should I eat donut" "nah" "bet" "3600 seconds"` <-secret timeframe option, default: {DEFAULT_TIMEOUT_TIME}
`!poll "age" "0" "90"`
these are the  for voting, first option is left, second option is right
{''.join(REACT_EMOJIS)}'''

# List of commands and their descriptions
COMMANDS_AND_DESCRIPTIONS = [
    ("!ping", "Check if I'm alive and kicking!"),
    ("!poll", poll_descr),
    # Add more commands and descriptions here
]