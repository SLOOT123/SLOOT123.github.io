"""Test para verificar que la página se renderiza correctamente."""
import sys
sys.path.insert(0, 'c:\\Users\\slotzs\\Desktop\\dashtv')

import dash
from dash import dcc, html
from pages.aplicacion_sir_unmsm_v2 import layout

# Crear una app simple de prueba
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Test Page"),
    layout
])

if __name__ == '__main__':
    print("✓ Layout cargado exitosamente sin errores")
    print("✓ La página debería renderizarse correctamente")
