"""
Módulo: Comparación de Escenarios - Propagación de Rumores
==========================================================

Simulación interactiva que compara dos escenarios epidemiológicos para modelar
la propagación de rumores/información en redes sociales.

Autor: Equipo de Análisis
Versión: 2.1 (Profesional)
Fecha: 2025-11-29
"""

import logging
from typing import Tuple, Dict, Any

import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.integrate import odeint

# ==========================
# CONFIGURACIÓN DE LOGGING
# ==========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==========================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================
dash.register_page(
    __name__,
    path='/comparacion-escenarios',
    name='Comparación de Escenarios',
    title='Propagación de Rumores - Comparación'
)

# ==========================
# FUNCIONES AUXILIARES
# ==========================

def modelo_rumores(y, t, beta, gamma):
    """
    Modelo SIR adaptado para la propagación de rumores.

    Parámetros:
    -----------
    y : tuple
        Estados: (S, I, R) = Susceptibles, Infectados, Recuperados
    t : float
        Tiempo
    beta : float
        Tasa de propagación
    gamma : float
        Tasa de recuperación (aburrimiento/racionalidad)

    Retorna:
    --------
    tuple
        Derivadas (dS/dt, dI/dt, dR/dt)
    """
    S, I, R = y
    N = S + I + R
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

def simular_escenario(beta: float, gamma: float, dias: int = 100) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Simula un escenario de propagación de rumores.

    Parámetros:
    -----------
    beta : float
        Tasa de propagación
    gamma : float
        Tasa de recuperación
    dias : int
        Número de días a simular

    Retorna:
    --------
    tuple
        Arrays de tiempo, S, I, R
    """
    N = 1000
    I0 = 1
    R0 = 0
    S0 = N - I0 - R0
    y0 = [S0, I0, R0]
    t = np.linspace(0, dias, dias)

    try:
        result = odeint(modelo_rumores, y0, t, args=(beta, gamma))
        S, I, R = result.T
        return t, S, I, R
    except Exception as e:
        logger.error(f"Error en la simulación: {e}")
        raise

# ==========================
# DISEÑO DE LA INTERFAZ
# ==========================

layout = html.Div([
    html.H2("Comparación de Escenarios - Propagación de Rumores", className="text-center mb-4"),

    html.Div([
        html.Label("Tasa de propagación (β) - Escenario 1:"),
        dcc.Slider(id='beta1', min=0.1, max=1.0, step=0.05, value=0.5, marks={i/10: str(i/10) for i in range(1, 11)}),
    ], className="mb-3"),

    html.Div([
        html.Label("Tasa de recuperación (γ) - Escenario 1:"),
        dcc.Slider(id='gamma1', min=0.1, max=1.0, step=0.05, value=0.2, marks={i/10: str(i/10) for i in range(1, 11)}),
    ], className="mb-3"),

    html.Div([
        html.Label("Tasa de propagación (β) - Escenario 2:"),
        dcc.Slider(id='beta2', min=0.1, max=1.0, step=0.05, value=0.7, marks={i/10: str(i/10) for i in range(1, 11)}),
    ], className="mb-3"),

    html.Div([
        html.Label("Tasa de recuperación (γ) - Escenario 2:"),
        dcc.Slider(id='gamma2', min=0.1, max=1.0, step=0.05, value=0.3, marks={i/10: str(i/10) for i in range(1, 11)}),
    ], className="mb-3"),

    html.Button("Simular", id='btn-simular', n_clicks=0, className="btn btn-primary mb-4"),

    dcc.Graph(id='grafico-comparacion')
], className="container mt-5")

# ==========================
# CALLBACKS
# ==========================

@callback(
    Output('grafico-comparacion', 'figure'),
    Input('btn-simular', 'n_clicks'),
    State('beta1', 'value'),
    State('gamma1', 'value'),
    State('beta2', 'value'),
    State('gamma2', 'value')
)
def actualizar_grafico(n_clicks, beta1, gamma1, beta2, gamma2):
    """
    Actualiza el gráfico de comparación entre dos escenarios.
    """
    if n_clicks == 0:
        return go.Figure()

    try:
        t1, S1, I1, R1 = simular_escenario(beta1, gamma1)
        t2, S2, I2, R2 = simular_escenario(beta2, gamma2)

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Escenario 1", "Escenario 2"),
            shared_yaxes=True
        )

        fig.add_trace(go.Scatter(x=t1, y=I1, mode='lines', name='Infectados (I)', line=dict(color='red')), row=1, col=1)
        fig.add_trace(go.Scatter(x=t1, y=S1, mode='lines', name='Susceptibles (S)', line=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=t1, y=R1, mode='lines', name='Recuperados (R)', line=dict(color='green')), row=1, col=1)

        fig.add_trace(go.Scatter(x=t2, y=I2, mode='lines', name='Infectados (I)', line=dict(color='red'), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=t2, y=S2, mode='lines', name='Susceptibles (S)', line=dict(color='blue'), showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(x=t2, y=R2, mode='lines', name='Recuperados (R)', line=dict(color='green'), showlegend=False), row=1, col=2)

        fig.update_layout(
            title="Comparación de Escenarios de Propagación de Rumores",
            xaxis_title="Días",
            yaxis_title="Población",
            hovermode='x unified',
            template='plotly_white'
        )

        return fig

    except Exception as e:
        logger.error(f"Error al generar gráfico: {e}")
        return go.Figure().add_annotation(
            text="Error al generar gráfico",
            xref="paper", yref="paper",
            showarrow=False, font=dict(size=20)
        )