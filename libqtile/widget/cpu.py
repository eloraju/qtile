# Copyright (c) 2019 Niko Järvinen (b10011)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import psutil

from libqtile.widget import base
from libqtile import utils


class CPU(base.ThreadedPollText):
    orientations = base.ORIENTATION_HORIZONTAL

    defaults = [
        ("update_interval", 1.0, "Update interval for the CPU widget"),
        (
            "format",
            "CPU {freq_current}GHz {load_percent}%",
            "CPU display format",
        ),
        ("bar_unused", ":", "Inactive char for ascii-bar"),
        ("bar_used", "#", "active char for ascii-bar"),
        ("color_low", None, "Color to use with the Bar when usage is below medium threshold. If None self.foreground is used"),
        ("color_medium", "FFBA08", "Color to use with the Bar when usage is above medium threshold"),
        ("color_high", "D00000", "Color to use with the Bar when usage is above high threshold"),
        ("sync_colors", True, "Use the threshold color values with all outputs"),
        ("threshold_medium", 50, "When to use medium color"),
        ("threshold_high", 80, "When to use high color"),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(CPU.defaults)

    def tick(self):
        self.update(self.poll())
        return self.update_interval

    def poll(self):
        variables = dict()
        cur_percent = psutil.cpu_percent()
        cpu_used = (round(cur_percent / 10)) * self.bar_used
        cpu_unused = (10-len(cpu_used)) * self.bar_unused

        if cur_percent < self.threshold_medium:
            bar_color = self.color_low if self.color_low else self.foreground
        elif cur_percent < self.threshold_high:
            bar_color = self.color_medium
        else:
            bar_color = self.color_high

        text_color = bar_color if self.sync_colors else self.foreground

        variables["load_percent"] = f'<span foreground="{utils.hex(text_color)}">{round(cur_percent)}</span>'
        variables["load_bar"] = f'<span foreground="{utils.hex(bar_color)}">{cpu_used}</span>{cpu_unused}'
        freq = psutil.cpu_freq()
        variables["freq_current"] = round(freq.current / 1000, 1)
        variables["freq_max"] = round(freq.max / 1000, 1)
        variables["freq_min"] = round(freq.min / 1000, 1)

        return self.format.format(**variables)
