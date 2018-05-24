import subprocess
output = subprocess.run(['ls'], shell=True, stdout=subprocess.PIPE)
print(output.stdout)
