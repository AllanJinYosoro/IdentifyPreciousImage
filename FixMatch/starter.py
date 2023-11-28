import subprocess

command = ['python', 'Mytrain.py', '--num-workers', '4', '--dataset', 'PhotoGraph', '--batch-size', '9', '--num-labeled', '45', '--eval-step', '1024', '--total-steps', '204800', '--arch', 'wideresnet', '--lr', '0.03', '--expand-labels', '--seed', '5', '--out', 'results/202311281553']

process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

if process.returncode != 0:
    print(f'Error occurred: {stderr.decode()}')
else:
    print(f'Success! Output: {stdout.decode()}')