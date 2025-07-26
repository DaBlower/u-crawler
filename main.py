import categories
import programs
import os

# clear terminal
os.system("cls" if os.name == "nt" else "clear")

# get categories of interest
print("Running categories.py")
categories.run(debug=False)
print("\nRunning programs.py")
programs.run(debug=False)