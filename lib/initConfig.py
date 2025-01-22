import configparser

def importConfig() -> dict:
    config = configparser.ConfigParser()
    config.read('config.ini')
    config_dict = {
        # This is a very roundabout way of doing this but it works
        section.upper(): {key.upper(): value for key, value in config.items(section)}
        for section in config.sections()
    }
    
    return config_dict

def populateCofig() -> None:
    # TODO: Ask user for credential that are added to the config and also tell the user
    # they can manually enter it
    pass