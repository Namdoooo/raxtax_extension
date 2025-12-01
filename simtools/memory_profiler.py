import psutil
import subprocess
import sys
import time

memory_result_path = sys.argv[1]
CMD = sys.argv[2:]

p = subprocess.Popen(CMD)
parent = psutil.Process(p.pid)

peak = 0
parent_peak = 0
children_peak = 0

while p.poll() is None:
    try:
        procs_children = parent.children(recursive=True)
        total = 0

        parent_memory = parent.memory_info().rss
        parent_peak = max(parent_peak, parent_memory)

        total += parent_memory

        for proc in procs_children:
            try:
                children_memory = proc.memory_info().rss
                total += children_memory
                children_peak = max(children_peak, children_memory)
            except psutil.NoSuchProcess:
                pass

        peak = max(peak, total)

    except psutil.NoSuchProcess:
        break

    time.sleep(0.01)  # 10 ms

cmd_str = " ".join(CMD)
peak_gb = peak / 1024 / 1024 / 1024
parent_peak_gb = parent_peak / 1024 / 1024 / 1024
children_peak_gb = children_peak / 1024 / 1024 / 1024

file_name = CMD[-1].split(".")[-1]

with open(memory_result_path, "a") as f:
    f.write(f"{cmd_str} \n")
    f.write(f"{file_name} peak (GB): {peak_gb} \n")
    f.write(f"{file_name} parent_peak (GB): {parent_peak_gb} \n")
    f.write(f"{file_name} children_peak (GB): {children_peak_gb} \n")
