import cairocffi
import pytest

from libqtile.widget import memory
from libqtile.widget.memory import Memory

def mock_virt_mem():
    return "yolo"

def mock_swap_mem():
    return "oloy"

def test_ascii_bar(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr("psutil.virtual_memory", mock_virt_mem)
        m.setattr("psutil.swap_memory", mock_swap_mem)
        mem = Memory()

    print(mem.poll())
    
