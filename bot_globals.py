REACT_EMOJIS = ["🌕", "🌖", "🌗", "🌘", "🌑", "🌒", "🌓", "🌔", "🌝"]
R_E_HALF, R_E_ODD = divmod(len(REACT_EMOJIS),2)
MAX_STARS = 15
SECONDS = 1                     # unit of timeout_time
MINUTES = 60 * SECONDS          #       60
HOURS = 60 * MINUTES            #    3,600
DAYS = 24 * HOURS               #   86,400
MAX_TIME_WAIT = 12 * HOURS
DEFAULT_TIMEOUT_TIME = DAYS
DAY_HOUR_MINUTE = {"d":["d", "day", "days"],
                   "h":["h", "hr", "hrs", "hour", "hours"],
                   "m":["m", "min", "mins", "minutes"],
                   "s":["s", "sec", "secs", "second", "seconds"]
                   }