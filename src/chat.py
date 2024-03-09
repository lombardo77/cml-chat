import sys
import subprocess

k = input("Hello! Are you a server or a chatter? [s] or [c]")

if k == 's':
    subprocess.run(['./chat'])
elif k == 'c':
    subprocess.rub(['python', 'client.py'])
else:
    print("Invalid input. Goodbye!")
    sys.exit(0)
