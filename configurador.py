import json
# import argparse

# Parseador de argumentos
#parser = argparse.ArgumentParser(description='Configurac los diferentes segmentos en los routers pasados')
#parser.add_argument('fichero', metavar='FILE', type=str, nargs='+',
#                    help='fichero de configuración a usar')

def validate_port(port):
    # TODO: Validar puerto
    return port > 0

def validate_segment(segment):
    # TODO: Validar segmento
    return segment > 0

def validate_ip(ip):
    # TODO: Validar ip
    return True

def validate_input(json_object):
    """ Devuelve true si json_object pasalos requisitos necesarios para ser un fichero válido
        Para ver el formato de entrada válido véase format.json 
        y para ver un ejemplo véase example.json
    """
    try:
        if type(json_object) is not list:
            return False
        for machine_config in json_object:
            if (type(machine_config["ip"]) is not str) or not validate_ip(machine_config["ip"]):
                return False
            if type(machine_config["config"]) is not list:
                return False
            for actual_config in machine_config["config"]:
                if (type(actual_config["segment"]) is not int) or not validate_segment(actual_config["segment"]):
                    return False
                if type(actual_config["ports"]) is not list:
                    return False
                for actual_port in actual_config["ports"]:
                    if (type(actual_port) is not int) or not validate_port(actual_port):
                        return False
    except KeyError as ke:
        # Formato incorrecto debido a que algún campo no existe
        return False
    # Todos los campos existen y están bien
    return True

with open("example.json", "r") as read_file:
    try:
        data = json.load(read_file)
        print(validate_input(data))
    except ValueError as ve:
        print("Error al parsear el json")
        exit()

print("final")

