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
                "service_uri": "https://trd-nqy8t8x3b6eu50xjbs.z4.kusto.fabric.microsoft.com",
                "default_database": "TotalOrders_EventhouseEndpoint",
                "description": "Workspace: Finanzas & TI | Eventhouse Endpoint del Lakehouse TotalOrders (pedidos totales)",
            },
            {
                "service_uri": "https://trd-xh4r5sjjqgp0h1gkme.z2.kusto.fabric.microsoft.com",
                "default_database": "Field_Service_Scheduler_EventhouseEndpoint",
                "description": "Workspace: Servicio | Eventhouse Endpoint del Lakehouse Field_Service_Scheduler (programación de servicios en terreno)",
            },
            {
                "service_uri": "https://trd-cn6c2fyav0k5u0aswt.z1.kusto.fabric.microsoft.com",
                "default_database": "Libro_Facturacion_KSB_SER_EventhouseEndpoint",
                "description": "Workspace: Servicio | Eventhouse Endpoint del Lakehouse Libro_Facturacion_KSB_SER",
            },
            {
                "service_uri": "https://trd-u82q53np9fwwuqvuw6.z6.kusto.fabric.microsoft.com",
                "default_database": "Centro_Costo_EventhouseEndpoint",
                "description": "Workspace: Finanzas & TI | Eventhouse Endpoint del Lakehouse Centro_Costo (Centro de Costos)",
            },
            {
                "service_uri": "https://trd-6bq2q5753ypzy65ypc.z4.kusto.fabric.microsoft.com",
                "default_database": "Field_Service_Scheduler_EventhouseEndpoint",
                "description": "Workspace: Finanzas & TI | Eventhouse Endpoint del Lakehouse Field_Service_Scheduler (programación de servicios en terreno)",
            },
            {
                "service_uri": "https://trd-m8sgf852c6p8f74pkx.z4.kusto.fabric.microsoft.com",
                "default_database": "Interfaz_OI_TO_EventhouseEndpoint",
                "description": "Workspace: Finanzas & TI | Eventhouse Endpoint del Lakehouse Interfaz_OI_TO (Interfaz OI TO)",
            },
            {
                "service_uri": "https://trd-5cmfu1prrmvm0pef7f.z2.kusto.fabric.microsoft.com",
                "default_database": "Obsolescencia_inventario_EventhouseEndpoint",
                "description": "Workspace: Finanzas & TI | Eventhouse Endpoint del Lakehouse Obsolescencia_inventario (Obsolescencia de inventario)",
            },
        ]
    ),
)

from fabric_rti_mcp.server import main

main()
