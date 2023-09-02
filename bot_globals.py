REACT_EMOJIS = ["🌕", "🌖", "🌗", "🌘", "🌑", "🌒", "🌓", "🌔", "🌝"]
MAX_STARS = 15
SECONDS = 1                     # unit of timeout_time
MINUTES = 60 * SECONDS          #       60
HOURS = 60 * MINUTES            #    3,600
DAYS = 24 * HOURS               #   86,400
DEFAULT_TIMEOUT_TIME = DAYS
DAY_HOUR_MINUTE = {"d":["d", "day", "days"],
                   "h":["h", "hr", "hrs", "hour", "hours"],
                   "m":["m", "min", "mins", "minutes"],
                   "s":["s", "sec", "secs", "second", "seconds"]
                   }