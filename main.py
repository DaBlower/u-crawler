import subprocess
import os

# clear terminal
os.system("cls" if os.name == "nt" else "clear")

# get categories of interest
print("Running categories.py")
subprocess.run(['py', 'categories.py'])
print("\nRunning programs.py")
subprocess.run(['py', 'programs.py'])