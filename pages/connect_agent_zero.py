import requests
import sseclient

def connect_to_agent_zero():
    url = "http://localhost:32768/mcp/t-mWDlt3BFNePBzz9R/sse"
    try:
        # Realiza la conexión al servidor SSE
        response = requests.get(url, stream=True)
        client = sseclient.SSEClient(response)

        print("Conectado a agent-zero. Escuchando eventos...")
        for event in client.events():
            print(f"Evento recibido: {event.data}")
    except Exception as e:
        print(f"Error al conectar con agent-zero: {e}")

# Ejecuta la conexión
connect_to_agent_zero()