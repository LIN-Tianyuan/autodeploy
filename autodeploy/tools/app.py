from logbook import Logger, StreamHandler
import sys
from autodeploy.tools.read_toml import get_project_toml_value
from autodeploy.tools.command import configuration_parameter, remove_same_name_directory_from_root, \
                                     get_project_from_git, remove_same_name_service, \
                                     remove_same_name_directory, upload_directory, \
                                     environment_configuration, install_service
from pypsrp.client import Client
from autodeploy.rootpath import ROOT_DIR

StreamHandler(sys.stdout).push_application()
log = Logger("Process")


def main_step():
    log.info("Load the git project...")
    git_link, host_name = configuration_parameter()
    deploy_directory_name = git_link.split("/")[-1].split(".")[0]
    log.info("Git link: " + git_link)
    log.info("Host name: " + host_name)
    log.info("Deploy directory name: " + deploy_directory_name)
    client = Client(host_name, ssl=False)
    log.info("Delete the directory with the same name under the root path...")
    log.info(remove_same_name_directory_from_root(deploy_directory_name))
    get_project_from_git(git_link)
    log.info("Delete the service with the same name as the remote server...")
    remove_same_name_service(client, deploy_directory_name)
    destination_path = get_project_toml_value(deploy_directory_name, "deploy.path.destination_path")
    env_path = get_project_toml_value(deploy_directory_name, "deploy.path.env_path")
    log.info("Delete the directory with the same name under the destination path...")
    remove_same_name_directory(client, destination_path, deploy_directory_name)
    log.info("Upload the project directory to the destination path...")
    upload_directory(client, deploy_directory_name, ROOT_DIR, destination_path)
    python_version = get_project_toml_value(deploy_directory_name, "project.requires-python")
    requirement = get_project_toml_value(deploy_directory_name, "project.dependency")
    log.info("Remote server environment configuration...")
    log.info(environment_configuration(client, deploy_directory_name, python_version, destination_path, requirement))
    log.info("Service installing...")
    log.info(install_service(client, deploy_directory_name, destination_path, env_path))


if __name__ == "__main__":
    main_step()