import cairocffi
import pytest
import psutil

from libqtile.widget import memory
from libqtile.widget.memory import Memory

class MockMem:
    def __init__(self, **mem):
        self.total = 1024 * 1024 * 10 if not mem.get("total") else mem.get("total")
        self.percent = 50 if not mem.get("percent") else mem.get("percent")
        self.used = 1024 * 1024 * 5 if not mem.get("used") else mem.get("used")
        self.free = 1024 * 1024 * 5 if not mem.get("free") else mem.get("free")
        self.buffers = 1024 * 1024 * 10 if not mem.get("buffers") else mem.get("buffers")
        self.active = 1024 * 1024 * 10 if not mem.get("active") else mem.get("active")
        self.inactive = 1024 * 1024 * 10 if not mem.get("inactive") else mem.get("inactive")
        self.shared = 1024 * 1024 * 10 if not mem.get("shared") else mem.get("shared")
        # Swap attributes if not mem.get("attributes") else mem.get("attributes")
        self.sin = 0 if not mem.get("sin") else mem.get("sin")
        self.sout = 0 if not mem.get("sout") else mem.get("sout")

def get_mem(**mem):
    def virtual_memory():
        return MockMem(**mem)
    return virtual_memory

def test_ascii_bar_low_threshold_memory(monkeypatch):
    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 10))
    monkeypatch.setattr(psutil,"swap_memory", get_mem())
    mem = Memory(format="{MemBar}")

    assert mem.poll() == '<span foreground="#ffffff">#</span>:::::::::'

def test_ascii_bar_medium_threshold_memory(monkeypatch):
    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 51))
    monkeypatch.setattr(psutil,"swap_memory", get_mem())
    mem = Memory(format="{MemBar}", color_medium="deadbe")

    assert mem.poll() == '<span foreground="#deadbe">#####</span>:::::'

def test_ascii_bar_high_threshold_memory(monkeypatch):
    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 86))
    monkeypatch.setattr(psutil,"swap_memory", get_mem())
    mem = Memory(format="{MemBar}", color_high="deadbe")

    assert mem.poll() == '<span foreground="#deadbe">#########</span>:'

def test_ascii_bar_no_markup_memory(monkeypatch):
    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 50))
    monkeypatch.setattr(psutil,"swap_memory", get_mem())
    mem = Memory(format="{MemBar}", markup=False)

    assert mem.poll() == '#####:::::'

def test_ascii_bar_changes_memory(monkeypatch):
    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 50))
    monkeypatch.setattr(psutil,"swap_memory", get_mem())
    mem = Memory(
            format="{MemBar}",
            threshold_medium=25,
            threshold_high=55,
            color_low="000000",
            color_medium="111111",
            color_high="222222",
            )

    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 5))
    assert mem.poll() == '<span foreground="#000000"></span>::::::::::'

    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 30))
    assert mem.poll() == '<span foreground="#111111">###</span>:::::::'

    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 90))
    assert mem.poll() == '<span foreground="#222222">#########</span>:'

def test_threshold_colors_memory(monkeypatch):
    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 50))
    monkeypatch.setattr(psutil,"swap_memory", get_mem())
    mem = Memory(format="{MemPercent}", thresholds=True, color_medium="deadbe")

    assert mem.poll() == '<span foreground="#deadbe">50</span>'

def test_threshold_color_changes_memory(monkeypatch):
    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 11))
    monkeypatch.setattr(psutil,"swap_memory", get_mem())
    mem = Memory(
            format="{MemPercent}",
            thresholds=True,
            color_low="ffffff",
            color_medium="deadbe",
            color_high="999999",
            )

    assert mem.poll() == '<span foreground="#ffffff">11</span>'

    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 50))
    assert mem.poll() == '<span foreground="#deadbe">50</span>'

    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 99))
    assert mem.poll() == '<span foreground="#999999">99</span>'

