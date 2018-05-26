import configparser


def read_config_file(config_path):
    config = configparser.ConfigParser()
    dataset = config.read(config_path)
    if len(dataset) == 1 and 'rpc.server' in config:
        return config['rpc.server']
    config.read("../" + config_path)
    if len(dataset) == 1 and 'rpc.server' in config:
        return config['rpc.server']
    raise ValueError("Failed to open/find config file!")
