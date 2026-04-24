import json
import os
import sys

# Add the app directory to sys.path so fabric_rti_mcp can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Force HTTP transport for Azure App Service
os.environ["FABRIC_RTI_TRANSPORT"] = "http"
os.environ["FABRIC_RTI_HTTP_HOST"] = "0.0.0.0"

os.environ.setdefault(
    "KUSTO_KNOWN_SERVICES",
    json.dumps(
        [
            {
                "service_uri": "https://trd-u82q53np9fwwuqvuw6.z6.kusto.fabric.microsoft.com",
                "description": "Centro de Costo",
            },
            {
                "service_uri": "https://trd-m8sgf852c6p8f74pkx.z4.kusto.fabric.microsoft.com",
                "description": "Interfaz OI TO",
            },
            {
                "service_uri": "https://trd-5cmfu1prrmvm0pef7f.z2.kusto.fabric.microsoft.com",
                "description": "Obsolescencia Inventario",
            },
        ]
    ),
)

from fabric_rti_mcp.server import main

main()
