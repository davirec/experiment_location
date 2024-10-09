import os
import subprocess
import time
import shutil


def list_apks(path):
    # apps = []
    for name in os.listdir(path):
        file_name = os.path.join(path, name)
        if ".apk" in file_name:
            return file_name
    return ""


def count_loss(apk_name):
    count = 0
    name = apk_name.split("/")[-1].split(".apk")[0]
    app_path = os.path.join(dir_output, name)
    # print(app_path)
    for root, dirs, files in os.walk(app_path):
        for subdir in files:
            if subdir.endswith('.png'):
                count += 1
    print(count / 2)
    return count / 2


def move_apk(apk_name):
    folder_name = 'process'
    name = apk_name.split("/")[-1]
    folder_dest = os.path.join(dir_input, folder_name)
    dest = os.path.join(dir_input, folder_name, name)

    if not os.path.exists(folder_dest):
        os.mkdir(folder_dest)
    shutil.move(apk_name, dest)


def run_droidbot_apks(list_apk_test, output_report, device_name, device_id):
    if not os.path.exists(output_report):
        os.makedirs(output_report)

    while list_apk_test != "":
        inicio = time.time()
        nome = list_apk_test.split("/")[-1].split(".apk")[0]
        nome = nome.replace(" ", "\ ")

        list_apk_test = list_apk_test.replace(" ", "\ ")
        comando = "python start.py -d {} -a {} -o {}/{}_{} -policy memory_guided -grant_perm -random -count 2250 -keep_app".format(device_id, list_apk_test, output_report, nome, device_name)

        print(comando)

        process = subprocess.Popen(comando, shell=True)
        output, error = process.communicate()

        fim = time.time()
        print("Tempo em horas {}".format((fim - inicio) / 3600))
        move_apk(list_apk_test)
        list_apk_test = list_apks(dir_input)
        time.sleep(10)


dir_input = "apps/apks"
dir_output = "apps/out"
list_apk = list_apks(dir_input)

run_droidbot_apks(list_apk, dir_output, "AVD", "emulator-5554")
