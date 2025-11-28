

"""
Modelo Logístico de Crecimiento - Aplicación Dash Profesional
==============================================================

Aplicación interactiva para visualizar dinámicas poblacionales usando
el modelo logístico. Incluye validación robusta, accesibilidad y
diseño profesional.

Autor: Equipo de Análisis
Versión: 2.0 (Profesional)
"""

import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np
import logging

# ==========================================
# CONFIGURACIÓN DE LOGGING
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

dash.register_page(
    __name__,
    path='/crecimiento-logistico',
    name='Crecimiento Logístico'
)

# ==========================================
# CONSTANTES Y CONFIGURACIÓN
# ==========================================

# Paleta de colores profesional (coherente con diseño corporativo)
COLORES = {
    'primario': '#2C5AA0',        # Azul corporativo
    'secundario': '#E74C3C',      # Rojo para énfasis
    'exito': '#27AE60',           # Verde para validación
    'advertencia': '#F39C12',     # Naranja para límites
    'fondo_claro': '#ECEFF1',     # Gris muy claro
    'fondo_oscuro': '#FFFFFF',    # Blanco puro
    'texto_primario': '#2C3E50',  # Gris oscuro
    'texto_secundario': '#7F8C8D',# Gris medio
    'borde': '#BDC3C7',           # Gris claro
    'grid': '#ECF0F1'             # Grid tenue
}

# Estilos reutilizables
ESTILO_CONTENEDOR = {
    'backgroundColor': COLORES['fondo_claro'],
    'padding': '24px',
    'borderRadius': '8px',
    'border': f"1px solid {COLORES['borde']}",
    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.08)',
    'marginBottom': '20px'
}

ESTILO_LABEL = {
    'fontWeight': '600',
    'color': COLORES['texto_primario'],
    'display': 'block',
    'marginBottom': '8px',
    'fontSize': '14px'
}

ESTILO_INPUT = {
    'width': '100%',
    'padding': '10px 12px',
    'borderRadius': '6px',
    'border': f"1px solid {COLORES['borde']}",
    'marginBottom': '16px',
    'boxSizing': 'border-box',
    'fontSize': '14px',
    'fontFamily': 'Segoe UI, Arial, sans-serif',
    'transition': 'border-color 0.3s ease'
}

ESTILO_BTN_PRIMARIO = {
    'backgroundColor': COLORES['primario'],
    'color': COLORES['fondo_oscuro'],
    'padding': '12px 20px',
    'border': 'none',
    'borderRadius': '6px',
    'cursor': 'pointer',
    'width': '100%',
    'fontSize': '14px',
    'fontWeight': '600',
    'transition': 'background-color 0.3s ease, box-shadow 0.3s ease',
    'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.1)'
}

# Rango de validación
VALIDACION = {
    'p0_min': 0,
    'p0_max': 1000000,
    'r_min': 0.001,
    'r_max': 1.0,
    'k_min': 1,
    'k_max': 10000000,
    't_min': 1,
    't_max': 1000
}

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def validar_parametros(p0, r, k, t_max):
    """
    Valida los parámetros del modelo logístico.
    
    Retorna:
        tuple: (es_valido, mensaje_error)
    """
    errores = []
    
    if p0 is None:
        errores.append("La población inicial es requerida")
    elif p0 < VALIDACION['p0_min'] or p0 > VALIDACION['p0_max']:
        errores.append(f"P(0) debe estar entre {VALIDACION['p0_min']} y {VALIDACION['p0_max']}")
    
    if r is None:
        errores.append("La tasa de crecimiento es requerida")
    elif r < VALIDACION['r_min'] or r > VALIDACION['r_max']:
        errores.append(f"r debe estar entre {VALIDACION['r_min']} y {VALIDACION['r_max']}")
    
    if k is None:
        errores.append("La capacidad de carga es requerida")
    elif k < VALIDACION['k_min'] or k > VALIDACION['k_max']:
        errores.append(f"K debe estar entre {VALIDACION['k_min']} y {VALIDACION['k_max']}")
    
    if t_max is None:
        errores.append("El tiempo máximo es requerido")
    elif t_max < VALIDACION['t_min'] or t_max > VALIDACION['t_max']:
        errores.append(f"t debe estar entre {VALIDACION['t_min']} y {VALIDACION['t_max']}")
    
    if p0 and k and p0 > k:
        errores.append("La población inicial P(0) no puede exceder la capacidad de carga K")
    
    return len(errores) == 0, " | ".join(errores) if errores else ""


def calcular_poblacion_logistica(p0, r, k, t_max, puntos=300):
    """
    Calcula la dinámica poblacional usando el modelo logístico.
    
    Parámetros:
        p0 (float): Población inicial
        r (float): Tasa de crecimiento intrínseca
        k (float): Capacidad de carga del ambiente
        t_max (float): Tiempo máximo de simulación
        puntos (int): Cantidad de puntos para discretizar
    
    Retorna:
        tuple: (tiempo, poblacion) - arrays de NumPy
    """
    t = np.linspace(0, t_max, puntos)
    
    # Fórmula logística: P(t) = K / (1 + ((K - P0) / P0) * exp(-r*t))
    if p0 == 0:
        P = np.zeros_like(t)
    elif p0 == k:
        P = np.full_like(t, k, dtype=float)
    else:
        try:
            with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
                exponente = np.exp(-r * t)
                coeficiente = (k - p0) / p0
                denominador = 1 + coeficiente * exponente
                P = k / denominador
                P = np.nan_to_num(P, nan=k, posinf=k, neginf=0)
        except Exception as e:
            logger.error(f"Error en cálculo logístico: {str(e)}")
            P = np.full_like(t, k, dtype=float)
    
    return t, P


def generar_figura_error(mensaje):
    """Genera una figura de error con mensaje personalizado."""
    fig = go.Figure()
    fig.add_annotation(
        text=mensaje,
        showarrow=False,
        font=dict(size=16, color=COLORES['secundario']),
        xref='paper', yref='paper',
        x=0.5, y=0.5
    )
    fig.update_layout(
        title="Error de Validación",
        paper_bgcolor=COLORES['fondo_claro'],
        plot_bgcolor=COLORES['fondo_oscuro'],
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=400
    )
    return fig


# ==========================================
# LAYOUT DE LA PÁGINA
# ==========================================

layout = html.Div([
    # Header
    html.Div([
        html.H1(
            "Modelo Logístico de Crecimiento",
            style={
                'textAlign': 'center',
                'color': COLORES['primario'],
                'fontFamily': 'Segoe UI, Arial, sans-serif',
                'marginBottom': '8px',
                'marginTop': '0px'
            }
        ),
        html.P(
            "Simulación de dinámicas poblacionales con restricciones ambientales",
            style={
                'textAlign': 'center',
                'color': COLORES['texto_secundario'],
                'fontSize': '14px',
                'marginBottom': '24px'
            }
        )
    ], style={'padding': '30px 20px 10px', 'backgroundColor': COLORES['fondo_oscuro']}),

    # Contenedor principal
    html.Div([
        html.Div([
            # COLUMNA IZQUIERDA: PANEL DE CONTROL
            html.Div([
                html.H3(
                    "Configuración del Modelo",
                    style={
                        'color': COLORES['primario'],
                        'borderBottom': f"2px solid {COLORES['primario']}",
                        'paddingBottom': '12px',
                        'marginBottom': '20px',
                        'fontSize': '16px'
                    }
                ),

                # Grupo de entrada 1: Población inicial
                html.Div([
                    html.Label(
                        "Población Inicial P(0)",
                        htmlFor="input-p0",
                        style=ESTILO_LABEL
                    ),
                    dcc.Input(
                        id="input-p0",
                        type="number",
                        value=20,
                        min=VALIDACION['p0_min'],
                        max=VALIDACION['p0_max'],
                        step=1,
                        style=ESTILO_INPUT,
                        placeholder="Ingrese población inicial"
                    ),
                    html.P(
                        "Tamaño inicial de la población",
                        style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                    )
                ]),

                # Grupo de entrada 2: Tasa de crecimiento
                html.Div([
                    html.Label(
                        "Tasa de Crecimiento (r)",
                        htmlFor="input-r",
                        style=ESTILO_LABEL
                    ),
                    dcc.Input(
                        id="input-r",
                        type="number",
                        value=0.1,
                        min=VALIDACION['r_min'],
                        max=VALIDACION['r_max'],
                        step=0.01,
                        style=ESTILO_INPUT,
                        placeholder="Ingrese tasa de crecimiento"
                    ),
                    html.P(
                        "Tasa intrínseca de crecimiento (0.001 - 1.0)",
                        style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                    )
                ]),

                # Grupo de entrada 3: Capacidad de carga
                html.Div([
                    html.Label(
                        "Capacidad de Carga (K)",
                        htmlFor="input-k",
                        style=ESTILO_LABEL
                    ),
                    dcc.Input(
                        id="input-k",
                        type="number",
                        value=1000,
                        min=VALIDACION['k_min'],
                        max=VALIDACION['k_max'],
                        step=10,
                        style=ESTILO_INPUT,
                        placeholder="Ingrese capacidad de carga"
                    ),
                    html.P(
                        "Límite máximo de la población que el ambiente puede sostener",
                        style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                    )
                ]),

                # Grupo de entrada 4: Tiempo máximo
                html.Div([
                    html.Label(
                        "Tiempo Máximo (t)",
                        htmlFor="input-t",
                        style=ESTILO_LABEL
                    ),
                    dcc.Input(
                        id="input-t",
                        type="number",
                        value=100,
                        min=VALIDACION['t_min'],
                        max=VALIDACION['t_max'],
                        step=5,
                        style=ESTILO_INPUT,
                        placeholder="Ingrese tiempo máximo"
                    ),
                    html.P(
                        "Duración de la simulación en unidades de tiempo",
                        style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                    )
                ]),

                # Botón de acción
                html.Button(
                    "Generar Simulación",
                    id="btn-generar",
                    style=ESTILO_BTN_PRIMARIO,
                    n_clicks=0
                ),

                # Área de mensajes
                html.Div(
                    id="mensaje-validacion",
                    style={
                        'marginTop': '16px',
                        'padding': '12px',
                        'borderRadius': '6px',
                        'display': 'none',
                        'fontSize': '13px'
                    }
                )

            ], style={
                **ESTILO_CONTENEDOR,
                'flex': '1',
                'minWidth': '300px',
                'maxWidth': '380px'
            }),

            # COLUMNA DERECHA: GRÁFICA Y ESTADÍSTICAS
            html.Div([
                # Gráfica principal
                html.Div([
                    dcc.Graph(
                        id='grafica-poblacion',
                        style={'height': '500px', 'width': '100%'},
                        config={
                            'responsive': True,
                            'displayModeBar': True,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                        }
                    )
                ], style={
                    'backgroundColor': COLORES['fondo_oscuro'],
                    'padding': '12px',
                    'borderRadius': '8px',
                    'border': f"1px solid {COLORES['borde']}",
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.08)'
                }),

                # Panel de estadísticas
                html.Div([
                    html.H4(
                        "Estadísticas",
                        style={
                            'color': COLORES['primario'],
                            'marginTop': '20px',
                            'marginBottom': '12px'
                        }
                    ),
                    html.Div(
                        id="estadisticas-panel",
                        style={
                            'display': 'grid',
                            'gridTemplateColumns': '1fr 1fr',
                            'gap': '12px'
                        }
                    )
                ], style={**ESTILO_CONTENEDOR, 'marginTop': '16px'})

            ], style={'flex': '2', 'minWidth': '400px'})

        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'gap': '24px',
            'justifyContent': 'space-between'
        })

    ], style={
        'maxWidth': '1400px',
        'margin': '0 auto',
        'padding': '30px 20px'
    })

], style={
    'padding': '0px',
    'backgroundColor': COLORES['fondo_claro'],
    'minHeight': '100vh',
    'fontFamily': 'Segoe UI, Arial, sans-serif'
})


# ==========================================
# CALLBACKS
# ==========================================

@callback(
    [Output('grafica-poblacion', 'figure'),
     Output('estadisticas-panel', 'children'),
     Output('mensaje-validacion', 'children'),
     Output('mensaje-validacion', 'style')],
    Input('btn-generar', 'n_clicks'),
    [State('input-p0', 'value'),
     State('input-r', 'value'),
     State('input-k', 'value'),
     State('input-t', 'value')],
    prevent_initial_call=False
)
def actualizar_simulacion(n_clicks, p0, r, k, t_max):
    """
    Actualiza la simulación y gráfica basada en los parámetros ingresados.
    """
    # Validar parámetros
    es_valido, mensaje_error = validar_parametros(p0, r, k, t_max)

    if not es_valido:
        logger.warning(f"Parámetros inválidos: {mensaje_error}")
        fig_error = generar_figura_error(mensaje_error)
        
        estilo_error = {
            'backgroundColor': '#FADBD8',
            'borderLeft': f"4px solid {COLORES['secundario']}",
            'padding': '12px',
            'borderRadius': '6px',
            'display': 'block',
            'color': COLORES['secundario'],
            'fontSize': '13px'
        }
        
        return fig_error, [], mensaje_error, estilo_error

    # Calcular dinámica poblacional
    try:
        t, P = calcular_poblacion_logistica(p0, r, k, t_max, puntos=300)
        logger.info(f"Simulación calculada: P0={p0}, r={r}, K={k}, t_max={t_max}")
    except Exception as e:
        logger.error(f"Error en cálculo: {str(e)}")
        fig_error = generar_figura_error("Error en el cálculo de la simulación")
        return fig_error, [], "Error interno", {'display': 'none'}

    # Crear trazos
    trace_poblacion = go.Scatter(
        x=t,
        y=P,
        mode='lines',
        name='Población P(t)',
        line=dict(
            color=COLORES['primario'],
            width=3
        ),
        fill='tozeroy',
        fillcolor=f"rgba(44, 90, 160, 0.1)",
        hovertemplate='<b>Tiempo:</b> %{x:.2f}<br><b>Población:</b> %{y:.0f}<extra></extra>'
    )

    trace_capacidad = go.Scatter(
        x=[0, t_max],
        y=[k, k],
        mode='lines',
        name='Capacidad de Carga (K)',
        line=dict(
            color=COLORES['advertencia'],
            width=2,
            dash='dash'
        ),
        hovertemplate='<b>Capacidad:</b> %{y:.0f}<extra></extra>'
    )

    # Construir figura
    fig = go.Figure(data=[trace_poblacion, trace_capacidad])

    fig.update_layout(
        title={
            'text': '<b>Dinámica Poblacional - Modelo Logístico</b>',
            'font': {'size': 18, 'color': COLORES['primario']},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        hovermode='x unified',
        
        # Estilos de fondo y texto
        paper_bgcolor=COLORES['fondo_claro'],
        plot_bgcolor=COLORES['fondo_oscuro'],
        font=dict(color=COLORES['texto_primario'], size=12),

        # Configuración de ejes
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORES['grid'],
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor=COLORES['borde'],
            mirror=False,
            range=[0, t_max]
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORES['grid'],
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor=COLORES['borde'],
            mirror=False
        ),

        # Leyenda
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.00,
            xanchor='right',
            x=1.0,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor=COLORES['borde'],
            borderwidth=1
        ),

        margin=dict(l=60, r=40, t=80, b=60),
        height=500
    )

    # Calcular estadísticas
    poblacion_inicial = P[0]
    poblacion_final = P[-1]
    poblacion_maxima = np.max(P)
    tiempo_mitad_capacidad = None

    # Encontrar tiempo en que se alcanza K/2
    indice_mitad = np.argmin(np.abs(P - k / 2))
    if indice_mitad > 0:
        tiempo_mitad_capacidad = t[indice_mitad]

    # Crear tarjetas de estadísticas
    estadisticas = [
        html.Div([
            html.P("Población Inicial", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{poblacion_inicial:.0f}", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['primario']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(44, 90, 160, 0.08)", 'borderRadius': '6px'}),

        html.Div([
            html.P("Población Final", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{poblacion_final:.0f}", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['primario']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(44, 90, 160, 0.08)", 'borderRadius': '6px'}),

        html.Div([
            html.P("Capacidad de Carga", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{k:.0f}", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['advertencia']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(243, 156, 18, 0.08)", 'borderRadius': '6px'}),

        html.Div([
            html.P("% de Capacidad Alcanzada", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{(poblacion_final / k * 100):.1f}%", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['exito']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(39, 174, 96, 0.08)", 'borderRadius': '6px'})
    ]

    if tiempo_mitad_capacidad:
        estadisticas.append(
            html.Div([
                html.P("Tiempo a K/2", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
                html.P(f"{tiempo_mitad_capacidad:.2f}", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['primario']})
            ], style={'padding': '12px', 'backgroundColor': f"rgba(44, 90, 160, 0.08)", 'borderRadius': '6px', 'gridColumn': '1'})
        )

    return fig, estadisticas, "", {'display': 'none'}