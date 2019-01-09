import json
import argparse
import socket
import subprocess

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
    """ Devuelve true si json_object pasalos requisitos necesarios para ser un fichero valido
        Para ver el formato de entrada valido vease format.json
        y para ver un ejemplo vease example.json
    """
    try:
        if type(json_object) is not list:
            return False
        for machine_config in json_object:
            if (type(machine_config["ip"]) is not str) or not validate_ip(machine_config["ip"]):
                return False
            if type(machine_config["community"]) is not str:
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
        # Formato incorrecto debido a que algun campo no existe
        return False
    # Todos los campos existen y estan bien
    return True

def config_hubs(json_object):
    ''' 
        El fichero de entrada esta validado y es correcto, por lo que se puede proceder
        a configurar los hubs
    '''
    with open("/dev/null", "w") as devnull:
        for machine_config in json_object:
            ip = machine_config["ip"]
            community = machine_config["community"]
            snmp_res = subprocess.call(["snmpwalk", "-v", "1", "-c", community, ip, ".1.3.6.1.4.1.43.10.26.1.1.1.5"], stdout=devnull)
            if snmp_res!= 0:
                print("Fallo al establecer la conexion con el hub")
                exit(1)
            print ("==== Configurando el hub con ip: ", ip, "====")
            for actual_config in machine_config["config"]:
                segment = actual_config["segment"]
                snmp_res = subprocess.Popen(
                    ["snmpget", "-v", "1", "-c", community, ip, ".1.3.6.1.4.1.43.10.26.1.1.1.5.1." + str(1000 + segment)],
                    stdout=subprocess.PIPE)
                out, err = snmp_res.communicate()
                if snmp_res.returncode != 0:
                    print("Fallo al obtener el valor del segmento")
                    exit(1)
                seg_valor = int(out.split()[-1])
                print("-- Anyadiendo puertos al segmento:", segment, "--")
                for port in actual_config["ports"]:
                    snmp_res = subprocess.call(
                        ["snmpset", "-v", "1", "-c", community, ip,
                         ".1.3.6.1.4.1.43.10.26.1.1.1.5.1." + str(port), "i", str(seg_valor)],
                        stdout=devnull)
                    if snmp_res != 0:
                        print("Fallo al asignar el puerto al segmento")
                        exit(1)
                    print("Puerto:", port)

def main():
    # Parseador de argumentos
    parser = argparse.ArgumentParser(description='Configura los diferentes segmentos en los routers pasados')
    parser.add_argument('fichero', metavar='file', type=str,
                        help='fichero de configuracion a usar')
    args = parser.parse_args()
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