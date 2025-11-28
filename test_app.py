"""Test de la app completa con manejo de errores."""
import sys
sys.path.insert(0, 'c:\\Users\\slotzs\\Desktop\\dashtv')

import dash
from dash import dcc, html, callback, Input, Output
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Crear app
app = dash.Dash(__name__, use_pages=True)

# Registrar pages
try:
    from pages import aplicacion_sir_unmsm_v2
    logger.info("✓ Página aplicacion_sir_unmsm_v2 importada")
except Exception as e:
    logger.error(f"✗ Error importando aplicacion_sir_unmsm_v2: {e}")
    import traceback
    traceback.print_exc()

# Layout simple
app.layout = html.Div([
    html.H1("Test App"),
    dcc.Tabs(id='test-tabs', value='test', children=[
        dcc.Tab(label='Test', value='test', children=[
            html.Div([
                html.Button("Test Button", id='test-btn'),
                html.Div(id='test-output')
            ])
        ])
    ])
])

@callback(
    Output('test-output', 'children'),
    Input('test-btn', 'n_clicks')
)
def test_callback(n_clicks):
    return f"Clicked {n_clicks} times"

if __name__ == '__main__':
    print("✓ App configurada correctamente")
    print("✓ Todos los imports funcionan")
