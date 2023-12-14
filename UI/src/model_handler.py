import subprocess
import time
import os

def train_model(username):
    timetik = time.time()
    command = ['python', 'FixMatch/Mytrain.py', '--num-workers', '4', '--dataset', 'PhotoGraph', '--batch-size', '9', '--num-labeled', '45', '--eval-step', '1024', '--total-steps', '204800', '--arch', 'wideresnet', '--lr', '0.03', '--expand-labels', '--seed', '5', '--out', f'UI/user/models/{username}/{timetik}_model']

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f'Error occurred: {stderr.decode()}')
    else:
        print(f'Success! Output: {stdout.decode()}')

def delete_pictures(username):
    folder_path = f'UI/user/models/{username}'
    # 获取文件夹中所有文件的路径
    file_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]

    # 按文件的修改时间进行排序
    file_paths.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    # 获取时间最新的文件路径
    newest_file_path = file_paths[0] if file_paths else None

    command = ['python', 'FixMatch/Mypredict.py', '--num-workers', '4', '--dataset', 'PhotoGraph', '--batch-size', '9', '--num-labeled', '45', '--eval-step', '1024', '--total-steps', '204800', '--arch', 'wideresnet', '--lr', '0.03', '--expand-labels', '--seed', '5', '--out', f'UI/user/models/{username}/model_result', '--predict_model_path', newest_file_path, '--predict_data_path', 'UI/data/compdata/all']

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # 分割子进程的输出
    outputs = process.stdout.splitlines()

    predict_label = outputs[1].decode()

    if process.returncode != 0:
        print(f'Error occurred: {stderr.decode()}')
    else:
        print(f'Success! Output: {stdout.decode()}')

    return predict_label