

def get_config():
    with open("config.txt", 'r') as file:
        informations = file.read().split('\n')
    informations[0] = informations[0][9:]
    informations[1] = informations[1][9:]

    return informations
