# Descripción
Script que configura los segmentos de un grupo de hubs mediante el protocolo SNMP.

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