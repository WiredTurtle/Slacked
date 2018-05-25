import subprocess
output = subprocess.run(['echo "You got hacked"'], shell=True, stdout=subprocess.PIPE)
print(output.stdout)
