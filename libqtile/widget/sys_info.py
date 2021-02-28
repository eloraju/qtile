import psutil
from libqtile.widget import base


# What to do with this?
# - Combine CPU and Memory widgets
# - Add coloring
# - Add bar representation
# - Take a peek into psutil and see what does it offer
# - Add rounding
class SysInfo(base.ThreadPoolText):
    """Displays memory/swap and cpu usage

    mem_used: Returns memory in use
    mem_total: Returns total amount of memory
    mem_free: Returns amount of memory free
    mem_percent: Returns memory in use as a percentage
    buffers: Returns buffer amount
    active: Returns active memory
    inactive: Returns inactive memory
    shmem: Returns shared memory
    swap_total: Returns total amount of swap
    swap_free: Returns amount of swap free
    swap_used: Returns amount of swap in use
    swap_percent: Returns swap in use as a percentage

    Cpu spesifc data is measured as deltas between the reads

    cpu_load: Returns the cpu load percentage
    cpu_current_freq: Returns the current cpu frequency
    cpu_max_freq: Returns the maximum cpu frequency
    cpu_min_freq: Returns the minumum cpu frequency


    Widget requirements: psutil_.

    .. _psutil: https://pypi.org/project/psutil/
    """


    def __init__(self, **config):
        super().__init__("", **config)
        self.add_defaults(SysInfo.defaults)


    defaults = [
        ("update_interval", 1.0, "Update interval for the widget"),
        ("format", "{mem_used}M/{mem_total}M", "Formatting for field names."),
    ]

    def get_memory(self):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        val = {}
        val["mem_used"] = mem.used // 1024 // 1024
        val["mem_total"] = mem.total // 1024 // 1024
        val["mem_free"] = mem.free // 1024 // 1024
        val["mem_percent"] = mem.percent
        val["buffers"] = mem.buffers // 1024 // 1024
        val["active"] = mem.active // 1024 // 1024
        val["inactive"] = mem.inactive // 1024 // 1024
        val["shmem"] = mem.shared // 1024 // 1024
        val["swap_total"] = swap.total // 1024 // 1024
        val["swap_free"] = swap.free // 1024 // 1024
        val["swap_used"] = swap.used // 1024 // 1024
        val["swap_percent"] = swap.percent
        return val;

    def get_cpu(self):
        val = {}

        val["load_percent"] = round(psutil.cpu_percent(), 1)
        freq = psutil.cpu_freq()
        val["freq_current"] = round(freq.current / 1000, 1)
        val["freq_max"] = round(freq.max / 1000, 1)
        val["freq_min"] = round(freq.min / 1000, 1)

        return val;

    def createBarRepresentation(self, cur, max, activeChar, inactiveChar, charCount):
        return "yolo"

    def poll(self):
        cpu = self.get_cpu()
        mem = self.get_memory()
