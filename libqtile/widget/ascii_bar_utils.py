from libqtile import utils

# Options required for the bar and threshold coloring to work
#        ("bar_unused", ":", "Inactive char for ascii-bar"),
#        ("bar_used", "#", "Active char for ascii-bar"),
#        ("char_count", 10, "Number of characters to use in the ascii bar"),
#        ("color_low", None, "Color to use when usage is below medium threshold. If None self.foreground is used"),
#        ("color_medium", "FFBA08", "Color to use with the Bar when usage is above medium threshold"),
#        ("color_high", "D00000", "Color to use with the Bar when usage is above high threshold"),
#        ("thresholds", True, "Use the threshold color values with all outputs"),
#        ("threshold_medium", 50, "When to use medium color"),
#        ("threshold_high", 80, "When to use high color"),

def create_ascii_bar(percentage, conf):
    """ Create a bar representing percentual uasge of something """
    bar_used = (round( percentage / conf.char_count)) * conf.bar_used
    bar_unused = (conf.char_count-len(bar_used)) * conf.bar_unused
    color = get_treshold_color(percentage, conf)
    return apply_color(color, bar_used) + bar_unused if conf.markup else bar_used+bar_unused

def get_treshold_color(value, conf):
    """ Get correct treshold color depending on the current value """
    if value < conf.threshold_medium:
        return utils.hex(conf.color_low) if conf.color_low else utils.hex(conf.foreground)
    elif value < conf.threshold_high:
        return utils.hex(conf.color_medium)
    else:
        return utils.hex(conf.color_high)

def apply_color(color, value):
    """ Apply the given color to given value """
    return f'<span foreground="{color}">{value}</span>'

def apply_to_format_values(value, confs):
    if confs.thresholds and confs.markup:
        color = get_treshold_color(value, confs)
        return apply_color(color, value)
    else:
        return value

def apply_color_fomatting(vals, confs):
    return {k: apply_to_format_values(v, confs) for k,v in vals.items()}
