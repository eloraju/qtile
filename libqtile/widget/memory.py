# -*- coding: utf-8 -*-
# Copyright (c) 2015 Jörg Thalheim (Mic92)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
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

__all__ = ["Memory"]

class Memory(base.ThreadedPollText):
    """Displays memory/swap usage

    MemUsed: Returns memory in use
    MemTotal: Returns total amount of memory
    MemFree: Returns amount of memory free
    MemPercent: Returns memory in use as a percentage
    MemBar: Returns ascii bar presentation of usage
    Buffers: Returns buffer amount
    Active: Returns active memory
    Inactive: Returns inactive memory
    Shmem: Returns shared memory
    SwapTotal: Returns total amount of swap
    SwapFree: Returns amount of swap free
    SwapUsed: Returns amount of swap in use
    SwapPercent: Returns swap in use as a percentage


    Widget requirements: psutil_.

    .. _psutil: https://pypi.org/project/psutil/
    """

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("format", "{MemUsed}M/{MemTotal}M", "Formatting for field names."),
        ("update_interval", 1.0, "Update interval for the Memory"),
        ("bar_unused", ":", "Inactive char for ascii-bar"),
        ("bar_used", "#", "Active char for ascii-bar"),
        ("char_count", 10, "Number of characters to use in the ascii bar"),
        ("color_low", None, "Color to use when usage is below medium threshold. If None self.foreground is used"),
        ("color_medium", "FFBA08", "Color to use with the Bar when usage is above medium threshold"),
        ("color_high", "D00000", "Color to use with the Bar when usage is above high threshold"),
        ("thresholds", True, "Use the threshold color values with all outputs"),
        ("threshold_medium", 50, "When to use medium color"),
        ("threshold_high", 80, "When to use high color"),
        ("decimals", None, "How many decimals are shown")
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(Memory.defaults)

    def tick(self):
        self.update(self.poll())
        return self.update_interval

    def poll(self):
        val = {}
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        val["MemUsed"] = round(mem.used // 1024 // 1024, self.decimals)
        val["MemTotal"] = round(mem.total // 1024 // 1024, self.decimals)
        val["MemFree"] = round(mem.free // 1024 // 1024, self.decimals)
        val["MemPercent"] = round(mem.percent, self.decimals)
        val["Buffers"] = round(mem.buffers // 1024 // 1024, self.decimals)
        val["Active"] = round(mem.active // 1024 // 1024, self.decimals)
        val["Inactive"] = round(mem.inactive // 1024 // 1024, self.decimals)
        val["Shmem"] = round(mem.shared // 1024 // 1024, self.decimals)
        val["SwapTotal"] = round(swap.total // 1024 // 1024, self.decimals)
        val["SwapFree"] = round(swap.free // 1024 // 1024, self.decimals)
        val["SwapUsed"] = round(swap.used // 1024 // 1024, self.decimals)
        val["SwapPercent"] = round(swap.percent, self.decimals)

        values = bar_utils.apply_color_fomatting(val)
        values["MemBar"] = bar_utils.create_ascii_bar(mem.percent, self)

        return self.format.format(**values)

