# Uso
```bash
$ python3 configurador.py nombre_config_file
```

# Formato config file
```json
[
    {
        "ip": "String", // Dirección ip
        "config": [
            {
                "segment": "Integer", // Segmento al que se quieren añadir puertos
                "ports": ["Integer"] // Puertos a añadir al segmento
            }
        ]
    }
]
```