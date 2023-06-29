import getopt
import os
import stat
import subprocess
import sys
import getopt
import shutil
from autodeploy.rootpath import ROOT_DIR


def remove_same_name_service(client, deploy_directory_name):
    client.execute_ps('''
        if (Get-Service %s -ErrorAction SilentlyContinue) {
            if ((Get-Service %s).Status -eq 'Running') {
                Stop-Service %s
            }
            nssm remove %s confirm
        }
    ''' %(deploy_directory_name,
          deploy_directory_name,
          deploy_directory_name,
          deploy_directory_name))


def remove_same_name_directory(client, destination_path, deploy_directory_name):
    client.execute_ps('''
        $deletefilepath = "%s\%s"
        if(Test-Path $deletefilepath){
            Remove-Item $deletefilepath -Force -Recurse
        }
    ''' %(destination_path, deploy_directory_name))


def copy_directory_to_remote_server(client, source_path, destination_path):
    """
    Copy a directory from the local host to the remote host
    :param client: connection
    :param source_path: local_folder_path
    :param destination_path: destination_folder_path
    :return:
    """
    for root, dirs, files in os.walk(source_path):
        if len(dirs) != 0:
            for directory in dirs:
                directory_path = os.path.join(root, directory)
                remote_path = os.path.join(destination_path, os.path.relpath(directory_path, source_path))
                client.execute_ps('''New-Item -Path %s -ItemType Directory''' % remote_path)
        for file in files:
            local_file = os.path.join(root, file)
            remote_file = os.path.join(destination_path, os.path.relpath(local_file, source_path))
            client.copy(local_file, remote_file)


def upload_directory(client, deploy_directory_name, source_path, destination_path):
    new_source_path = source_path + "\\" + deploy_directory_name
    new_destination_path = destination_path + "\\" + deploy_directory_name
    copy_directory_to_remote_server(client, new_source_path, new_destination_path)


def environment_configuration(client, deploy_directory_name, python_version, destination_path, requirement):
    output, streams, had_errors = client.execute_ps('''
        conda remove --name %s --all
        conda create -n %s python==%s
        conda activate %s
        conda env list
        cd %s\%s
        pip install -r %s
    ''' %(deploy_directory_name,
          deploy_directory_name,
          python_version,
          deploy_directory_name,
          destination_path,
          deploy_directory_name,
          requirement), configuration_name="Userprofile")
    return output


def install_service(client, deploy_directory_name, destination_path, env_path):
    output, streams, had_errors = client.execute_ps('''
        nssm install %s "%s\%s\python.exe" "%s\%s\%s\main.py"
        nssm start %s
    ''' %(deploy_directory_name,
          env_path,
          deploy_directory_name,
          destination_path,
          deploy_directory_name,
          deploy_directory_name,
          deploy_directory_name))
    return output


def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed


def get_project_from_git(git_link):
    hello_command = "git clone" + git_link
    print(hello_command)
    hello_info = run(hello_command)
    if hello_info.returncode != 0:
        print("An error occurred: %s", hello_info.stderr)
    else:
        print("Command executed successfully!")
    return hello_info


def configuration_parameter():
    argument_list = sys.argv[1:]

    options = "r:h:"
    long_options = ["repo=", "host="]

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argument_list, options, long_options)
        git_link = ''
        host_name = ''

        # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ("-r", "--repo"):
                git_link = currentValue
            elif currentArgument in ("-h", "--host"):
                host_name = currentValue

        return git_link, host_name

    except getopt.error as err:
        print(str(err))
        return str(err)


def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def remove_same_name_directory_from_root(deploy_directory_name):
    path = ROOT_DIR + "\\" + deploy_directory_name
    if os.path.isdir(path) and deploy_directory_name != '':
        shutil.rmtree(path, onerror=on_rm_error)
    return "Removed same name directory from root successfully!"


if __name__ == "__main__":
    print(ROOT_DIR)