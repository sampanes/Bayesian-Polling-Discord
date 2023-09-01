from bot_globals import *

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

def is_a_time(num):
    num = extract_numbers(num)
    try:
        float(num)
        return True
    except ValueError:
        return False

def get_ret_timeout(option3):
    time_char = ""
    for char_key, list_value in DAY_HOUR_MINUTE.items():
        for substring in list_value:
            if substring.lower() in option3.lower():
                time_char = char_key
                break
    if time_char:
        raw_time = float(extract_numbers(option3))
        if time_char == "d":
            actual_time = raw_time * 24 * HOURS
        ret_timeout = actual_time
    else:
        ret_timeout 
    return ret_timeout

def poll_input_to_string(options):
    if len(options) == 3:
        ret_timeout = DEFAULT_TIMEOUT_TIME
    elif len(options) == 4 and is_a_time(options[3]):
        ret_timeout = get_ret_timeout(options[3])
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