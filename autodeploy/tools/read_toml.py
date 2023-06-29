import toml
from autodeploy.rootpath import ROOT_DIR


def get_value(keys, i, setting):
    """
    Get the value of any toml key
    :param keys: delimited list of keys
    :param i: 0
    :param setting: toml data
    :return: value
    """
    string = setting.get(keys[i])
    if isinstance(string, dict):
        if i+1 < len(keys):
            return get_value(keys, i+1, string)
    return string


def get_toml_value(filepath, toml_key):
    """
    Get the value from any toml file
    :param filepath: filepath
    :param toml_key: the key to get the value for
    :return: required value
    """
    with open(filepath, mode="r") as fp:
        data = toml.load(fp)
    split_toml_key = toml_key.split(".")
    return get_value(split_toml_key, 0, data)


def get_project_toml_value(deploy_directory_name, toml_key):
    """
    Get toml value from standalone project
    :param deploy_directory_name: deploy_directory_name
    :param toml_key: toml_key
    :return: value
    """
    filepath = ROOT_DIR + "\\" + deploy_directory_name + "\pyproject.toml"
    print(filepath)
    value = get_toml_value(filepath, toml_key)
    return value


if __name__ == "__main__":
    print(ROOT_DIR)