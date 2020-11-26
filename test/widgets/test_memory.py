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

def test_ascii_bar(monkeypatch):
    monkeypatch.setattr(psutil,"virtual_memory", get_mem())
    monkeypatch.setattr(psutil,"swap_memory", get_mem())
    mem = Memory(format="{MemBar}")

    print(mem.poll())

def test_ascii_bar_low_threshold(monkeypatch):
    monkeypatch.setattr(psutil,"virtual_memory", get_mem(percent = 10))
    monkeypatch.setattr(psutil,"swap_memory", get_mem())
    mem = Memory(format="{MemBar}")

    print(mem.poll())
