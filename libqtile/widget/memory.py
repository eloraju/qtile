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

from libqtile.widget import base
from libqtile import utils

__all__ = '<span foreground="{utils.hex(text_color)">["Memory"]</span>'


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
        ("color_low", None, "Color to use with the Bar when usage is below medium threshold. If None self.foreground is used"),
        ("color_medium", "FFBA08", "Color to use with the Bar when usage is above medium threshold"),
        ("color_high", "D00000", "Color to use with the Bar when usage is above high threshold"),
        ("thresholds", True, "Use the threshold color values with all outputs"),
        ("threshold_medium", 50, "When to use medium color"),
        ("threshold_high", 80, "When to use high color"),
        ("decimals", 0, "How many decimals are shown")
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(Memory.defaults)

    def tick(self):
        self.update(self.poll())
        return self.update_interval

    def apply_color(self, color, val, is_percent = False):
        value = val if is_percent else self.human_readable(val)
        return f'<span foreground="{color}">{value}</span>'

    def human_readable(self, value):
        return round(value / 1024 / 1024, self.decimals)

    def poll(self):
        val = {}
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()


        if mem.percent < self.threshold_medium:
            bar_color = self.color_low if self.color_low else self.foreground
        elif mem.percent < self.threshold_high:
            bar_color = self.color_medium
        else:
            bar_color = self.color_high

        mem_bar_used = (round( mem.percent / 10)) * self.bar_used
        mem_bar_unused = (10-len(mem_bar_used)) * self.bar_unused

        text_color = utils.hex(bar_color) if self.thresholds else utils.hex(self.foreground)

        val["MemUsed"] = self.apply_color(text_color, mem.used) if self.thresholds else mem.used
        val["MemTotal"] = self.apply_color(text_color, mem.total) if self.thresholds else mem.total
        val["MemFree"] = self.apply_color(text_color, mem.free) if self.thresholds else mem.free
        val["MemPercent"] = self.apply_color(text_color, mem.percent, True) if self.thresholds else mem.percent
        val["MemBar"] = f'<span foreground="#{bar_color}>{mem_bar_used}</span>{mem_bar_unused}'
        val["Buffers"] = self.apply_color(text_color, mem.buffers) if self.thresholds else mem.buffers
        val["Active"] = self.apply_color(text_color, mem.active) if self.thresholds else mem.active
        val["Inactive"] = self.apply_color(text_color, mem.inactive) if self.thresholds else mem.inactive
        val["Shmem"] = self.apply_color(text_color, mem.shared) if self.thresholds else mem.shared
        val["SwapTotal"] = self.apply_color(text_color, swap.total) if self.thresholds else swap.total
        val["SwapFree"] = self.apply_color(text_color, swap.free) if self.thresholds else swap.free
        val["SwapUsed"] = self.apply_color(text_color, swap.used) if self.thresholds else swap.used
        val["SwapPercent"] = self.apply_color(text_color, swap.percent, True) if self.thresholds else swap.percent

        print(val)

        return self.format.format(**val)
