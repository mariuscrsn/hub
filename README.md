# Descripción
Script que configura los segmentos de un grupo de hubs mediante el protocolo SNMP. El formato del fichero de configuración debe ser json. Se proporciona un fichero de ejemplo (example.json) que configura nuestro hub y el de los compañero de la bancada 3.

# Uso
```bash
$ python3 configurador.py nombre_config_file
```

# Config file
## Formato
```json
[
    {
        "ip": "String",
        "community": "String",
        "config": [
            {
                "segment": "Integer",
                "ports": ["Integer"]
            }
        ]
    }
]
```

## Descripción de campos
```json
[
    {
        "ip": "Dirección ip",
        "community": "Community",
        "config": [
            {
                "segment": "Segmento al que se quieren añadir puertos",
                "ports": ["Puertos a añadir al segmento"]
            }
        ]
    }
]
```