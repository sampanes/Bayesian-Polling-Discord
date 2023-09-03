# Bayesian-Polling-Discord

A discord bot that allows you to take a poll where two options are voted on with credences, shown as a range of emojis from choice A to neutral to choice B

If you ask "What is your opinion on the impact of technology on the human species"
Some may say "Overall good" and others may say "Overall bad". But most people would be willing to concede the opposite to some degree. This polling allows users to express the degree to which they concede the opposite. In otherwords, how **strongly** they feel that technology has been good/bad, or what degree of impact it has had, for example

This can be used to get a consensus from a relatively small group of individuals, where traditional voting methods may not garner usable results. To absolutely beat this dead horse with examples: two people are trying to decide what to have for dinner. "Burgers" or "Pizza"
Person A has had pizza all week and does not want pizza again, too much pizza. Person B is hungry and thinks they can get more food per dollar with pizza, but is otherwise relatively indifferent. In A/B-only polling, it would be a tie, and they would both starve to death. With bayesian polling, where voters' credences are considered, the less strongly opinionated person would have the ability to both vote for pizza but also not strongly oppose burgers, and the result is an increase in net satisfaction at dinner and in life.

## Installation

If you are trying to run this bot on your own you need to just pip install the requirements

```
pip install -r requirements.txt
```

Then run the program

```
python3.10 .\main.py
```

Otherwise I think this should be one that is available to be invited. I am not sure if it's ready to be tested in larger servers with high stakes, and I need to figure out how to only ask for the permissions it actually needs.

## Usage

Start by configuring where the polls will post and where the results of those polls will post

```
!postpoll #poll-channel-example
!postresults #poll-results-example
```

Use the actual channel mention in discord, i.e. type ```!postpoll #po...``` and click the channel when you see the popup

The app will save both selected channels pickle the settings, and they should be available even if the bot shuts down. If you have multiple servers using this bot, they all get their own settings.

## Internal Configuration

1. Go to bot_globals.py and make sure you like the emojis being used. Any number of emojis should work, but odd numbers (and 9 specifically) were the most tested.
2. Still in bot_globals.py, set DEFAULT_TIMEOUT_TIME to the amount of time you want the poll to last before it automatically stops and calculates results. Note that when everyone who is able to vote has voted, the poll should automatically close. I haven't tested it though because that would require herding all my friends together to push the buttons when I need them to and all my friends are cats
3. Still in bot_globals.py go ahead and make sure that all the DAY_HOUR_MINUTE (I should refactor that name) strings are good. You may need to add more if one of your users just really really likes to abbreviate days as "dys" or something dumb
4. Go to main.py and double check the command aliases, I tried to make it so that a user who refuses to type ```!help``` can still possibly guess the commands. That said, there may be more to add or ones that are already used elsewhere and need to be deleted from the lists here
5. Next step is simply fix the code to work better because idk what I'm doing I taught myself this stuff this week
