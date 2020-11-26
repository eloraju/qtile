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

from libqtile.widget import base, ascii_bar_utils as bar_utils
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
        ("bar_used", "#", "Active char for ascii-bar"),
        ("char_count", 10, "Number of characters to use in the ascii bar"),
        ("color_low", None, "Color to use when usage is below medium threshold. If None self.foreground is used"),
        ("color_medium", "FFBA08", "Color to use with the Bar when usage is above medium threshold"),
        ("color_high", "D00000", "Color to use with the Bar when usage is above high threshold"),
        ("thresholds", True, "Use the threshold color values with all outputs"),
        ("threshold_medium", 50, "When to use medium color"),
        ("threshold_high", 80, "When to use high color"),
        ("decimals", None, "How many decimals are shown"),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(CPU.defaults)

    def tick(self):
        self.update(self.poll())
        return self.update_interval

    def poll(self):
        variables = dict()
        cpu_percent = psutil.cpu_percent()

        variables["load_percent"] = round(cpu_percent, self.decimals)
        freq = psutil.cpu_freq()
        variables["freq_current"] = round(freq.current / 1000, self.decimals)
        variables["freq_max"] = round(freq.max / 1000, self.decimals)
        variables["freq_min"] = round(freq.min / 1000, self.decimals)

        values = bar_utils.apply_color_fomatting(variables)
        values["load_bar"] = bar_utils.create_ascii_bar(cpu_percent ,self)

        return self.format.format(**values)
