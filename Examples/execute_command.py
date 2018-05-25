import subprocess
output = subprocess.run(['echo', 'You got hacked'], stdout=subprocess.PIPE)
print(output.stdout)
