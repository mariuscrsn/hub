import json
import argparse
import socket

def validate_port(port):
    return port >= 1 and port <= 24

def validate_segment(segment):
    return segment >= 0 and segment <= 4

def validate_ip(ip):
    ''' Return true if ip is a valid address
    '''
    try:
        socket.inet_aton(ip)
        # legal address
        return True
    except socket.error:
        # Not legal address
        return False

def validate_input(json_object):
    """ Devuelve true si json_object pasalos requisitos necesarios para ser un fichero válido
        Para ver el formato de entrada válido véase format.json 
        y para ver un ejemplo véase example.json
    """
    try:
        if type(json_object) is not list:
            print("json_object")
            return False
        for machine_config in json_object:
            if (type(machine_config["ip"]) is not str) or not validate_ip(machine_config["ip"]):
                print("ip")
                return False
            if type(machine_config["community"]) is not str:
                print("community")
                return False
            if type(machine_config["config"]) is not list:
                print("config")
                return False
            for actual_config in machine_config["config"]:
                if (type(actual_config["segment"]) is not int) or not validate_segment(actual_config["segment"]):
                    print("segment")
                    return False
                if type(actual_config["ports"]) is not list:
                    print("ports")
                    return False
                for actual_port in actual_config["ports"]:
                    if (type(actual_port) is not int) or not validate_port(actual_port):
                        print("ports2")
                        return False
    except KeyError as ke:
        # Formato incorrecto debido a que algún campo no existe
        print("ke")
        return False
    # Todos los campos existen y están bien
    return True

def config_hubs(json_object):
    ''' 
        El fichero de entrada está validado y es correcto, por lo que se puede proceder
        a configurar los hubs
    '''
    # TODO: Implementar esta función
    # Para implementarla mirar https://docs.python.org/3/library/subprocess.html
    # Subprocess vale para lanzar comando de shell
    pass

def main():
    # Parseador de argumentos
    parser = argparse.ArgumentParser(description='Configura los diferentes segmentos en los routers pasados')
    parser.add_argument('fichero', metavar='file', type=str,
                        help='fichero de configuración a usar')
    args = parser.parse_args()
    print(args.fichero)
    try:    
        with open(args.fichero, "r") as read_file:
            try:
                data = json.load(read_file)
                if validate_input(data):
                    config_hubs(data)
                else:
                    print("Los datos del fichero de entrada son incoherentes")
            except ValueError as ve:
                print("El formato del fichero de entrada es incorrecto")
    except IOError:
        print("No se puede leer el fichero ", args.fichero)

main()