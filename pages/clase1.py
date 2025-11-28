"""
Clase 1: Crecimiento Exponencial de Poblaciones
===============================================

Página educativa sobre modelado exponencial de dinámicas poblacionales.
Incluye teoría, visualizaciones interactivas y análisis comparativo.

Autor: Equipo de Análisis
Versión: 2.0 (Profesional)
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
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
    path='/crecimiento-exponencial',
    name='Crecimiento Exponencial'
)

# ==========================================
# CONSTANTES Y CONFIGURACIÓN
# ==========================================

# Paleta de colores profesional
COLORES = {
    'primario': '#2C5AA0',          # Azul corporativo
    'secundario': '#E74C3C',        # Rojo
    'exito': '#27AE60',             # Verde
    'advertencia': '#F39C12',       # Naranja
    'fondo_claro': '#ECEFF1',       # Gris muy claro
    'fondo_oscuro': '#FFFFFF',      # Blanco
    'texto_primario': '#2C3E50',    # Gris oscuro
    'texto_secundario': '#7F8C8D',  # Gris medio
    'borde': '#BDC3C7',             # Gris claro
    'grid': '#ECF0F1'               # Grid tenue
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

ESTILO_CARD_CONTENIDO = {
    'backgroundColor': COLORES['fondo_oscuro'],
    'padding': '20px',
    'borderRadius': '8px',
    'border': f"1px solid {COLORES['borde']}",
    'marginBottom': '16px',
    'lineHeight': '1.6'
}

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def generar_figura_exponencial(p0, r, t_max):
    """
    Genera la figura del crecimiento exponencial.
    
    Parámetros:
        p0 (float): Población inicial
        r (float): Tasa de crecimiento
        t_max (float): Tiempo máximo
    
    Retorna:
        go.Figure: Figura de Plotly
    """
    t = np.linspace(0, t_max, 300)
    P = p0 * np.exp(r * t)
    
    fig = go.Figure()
    
    # Traza principal
    fig.add_trace(go.Scatter(
        x=t,
        y=P,
        mode='lines',
        name='P(t) = P₀e^(rt)',
        line=dict(
            color=COLORES['primario'],
            width=3
        ),
        fill='tozeroy',
        fillcolor='rgba(44, 90, 160, 0.1)',
        hovertemplate='<b>Tiempo:</b> %{x:.2f}<br><b>Población:</b> %{y:.0f}<extra></extra>'
    ))
    
    # Anotación de la fórmula
    fig.add_annotation(
        text=f"P₀ = {p0:.0f}, r = {r:.3f}",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor=COLORES['primario'],
        borderwidth=1,
        borderpad=10,
        font=dict(size=12, color=COLORES['texto_primario'])
    )
    
    fig.update_layout(
        title={
            'text': '<b>Modelo Exponencial: P(t) = P₀e^(rt)</b>',
            'font': {'size': 18, 'color': COLORES['primario']},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        hovermode='x unified',
        
        # Estilos
        paper_bgcolor=COLORES['fondo_claro'],
        plot_bgcolor=COLORES['fondo_oscuro'],
        font=dict(color=COLORES['texto_primario'], size=12),
        
        # Ejes
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=COLORES['grid'],
            zeroline=False,
            showline=True,
            linewidth=1,
            linecolor=COLORES['borde'],
            mirror=False
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
    
    return fig


# Figura por defecto
fig_default = generar_figura_exponencial(100, 0.03, 100)

# ==========================================
# LAYOUT DE LA PÁGINA
# ==========================================

layout = html.Div([
    # Header
    html.Div([
        html.H1(
            "Clase 1: Crecimiento Exponencial de Poblaciones",
            style={
                'textAlign': 'center',
                'color': COLORES['primario'],
                'fontFamily': 'Segoe UI, Arial, sans-serif',
                'marginBottom': '8px',
                'marginTop': '0px'
            }
        ),
        html.P(
            "Fundamentos de modelado matemático en dinámicas poblacionales",
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
        # SECCIÓN 1: TEORÍA FUNDAMENTAL
        html.Div([
            html.H2(
                "1. Fundamentos Teóricos",
                style={
                    'color': COLORES['primario'],
                    'borderBottom': f"3px solid {COLORES['primario']}",
                    'paddingBottom': '12px',
                    'marginBottom': '20px',
                    'fontSize': '18px'
                }
            ),

            # Subsección 1.1
            html.Div([
                html.H3(
                    "1.1 Variables y Notación",
                    style={
                        'color': COLORES['texto_primario'],
                        'marginTop': '16px',
                        'marginBottom': '12px',
                        'fontSize': '16px'
                    }
                ),
                html.Div([
                    html.P(
                        "Para modelar el crecimiento de la población mediante ecuaciones diferenciales, "
                        "introducimos las siguientes variables y términos:",
                        style={'marginBottom': '12px'}
                    ),
                    html.Ul([
                        html.Li([
                            html.Span("P(t): ", style={'fontWeight': '600', 'color': COLORES['primario']}),
                            "Población en función del tiempo (unidades: individuos)"
                        ], style={'marginBottom': '8px'}),
                        html.Li([
                            html.Span("t: ", style={'fontWeight': '600', 'color': COLORES['primario']}),
                            "Variable temporal (unidades: horas, días, meses o años según contexto)"
                        ], style={'marginBottom': '8px'}),
                        html.Li([
                            html.Span("dP/dt: ", style={'fontWeight': '600', 'color': COLORES['primario']}),
                            "Tasa instantánea de cambio de la población"
                        ], style={'marginBottom': '8px'}),
                        html.Li([
                            html.Span("P₀: ", style={'fontWeight': '600', 'color': COLORES['primario']}),
                            "Población inicial (P en el tiempo t = 0)"
                        ], style={'marginBottom': '8px'}),
                        html.Li([
                            html.Span("r: ", style={'fontWeight': '600', 'color': COLORES['primario']}),
                            "Tasa de crecimiento intrínseca (r > 0 para crecimiento, r < 0 para decaimiento)"
                        ])
                    ], style={'paddingLeft': '20px'})
                ], style=ESTILO_CARD_CONTENIDO)
            ], style={**ESTILO_CONTENEDOR, 'marginBottom': '24px'}),

            # Subsección 1.2
            html.Div([
                html.H3(
                    "1.2 Modelo Exponencial",
                    style={
                        'color': COLORES['texto_primario'],
                        'marginTop': '16px',
                        'marginBottom': '12px',
                        'fontSize': '16px'
                    }
                ),
                html.Div([
                    html.P(
                        "El modelo exponencial asume que la población crece sin restricciones, "
                        "a una tasa proporcional al tamaño actual de la población:",
                        style={'marginBottom': '12px', 'fontStyle': 'italic'}
                    ),
                    html.Div(
                        "dP/dt = rP",
                        style={
                            'backgroundColor': f"rgba(44, 90, 160, 0.1)",
                            'padding': '12px',
                            'borderLeft': f"4px solid {COLORES['primario']}",
                            'borderRadius': '4px',
                            'marginBottom': '12px',
                            'fontFamily': 'monospace',
                            'fontSize': '14px',
                            'color': COLORES['primario']
                        }
                    ),
                    html.P(
                        "La solución analítica de esta ecuación diferencial es:",
                        style={'marginBottom': '12px', 'fontStyle': 'italic'}
                    ),
                    html.Div(
                        "P(t) = P₀ × e^(rt)",
                        style={
                            'backgroundColor': f"rgba(39, 174, 96, 0.1)",
                            'padding': '12px',
                            'borderLeft': f"4px solid {COLORES['exito']}",
                            'borderRadius': '4px',
                            'marginBottom': '12px',
                            'fontFamily': 'monospace',
                            'fontSize': '14px',
                            'color': COLORES['exito'],
                            'fontWeight': '600'
                        }
                    ),
                    html.P([
                        html.Span("Donde: ", style={'fontWeight': '600'}),
                        "e ≈ 2.71828 es la base del logaritmo natural"
                    ])
                ], style=ESTILO_CARD_CONTENIDO)
            ], style={**ESTILO_CONTENEDOR, 'marginBottom': '24px'}),

            # Subsección 1.3
            html.Div([
                html.H3(
                    "1.3 Interpretación de Parámetros",
                    style={
                        'color': COLORES['texto_primario'],
                        'marginTop': '16px',
                        'marginBottom': '12px',
                        'fontSize': '16px'
                    }
                ),
                html.Div([
                    html.P(
                        "La tasa de crecimiento r determina la velocidad de cambio:",
                        style={'marginBottom': '12px', 'fontStyle': 'italic'}
                    ),
                    html.Ul([
                        html.Li([
                            html.Span("r > 0: ", style={'fontWeight': '600', 'color': COLORES['exito']}),
                            "Crecimiento exponencial (población aumenta)"
                        ], style={'marginBottom': '8px'}),
                        html.Li([
                            html.Span("r = 0: ", style={'fontWeight': '600', 'color': COLORES['texto_secundario']}),
                            "Población constante"
                        ], style={'marginBottom': '8px'}),
                        html.Li([
                            html.Span("r < 0: ", style={'fontWeight': '600', 'color': COLORES['secundario']}),
                            "Decaimiento exponencial (población disminuye)"
                        ])
                    ], style={'paddingLeft': '20px', 'marginBottom': '12px'}),
                    html.P([
                        html.Span("Tiempo de duplicación: ", style={'fontWeight': '600'}),
                        "T_d = ln(2)/r ≈ 0.693/r"
                    ])
                ], style=ESTILO_CARD_CONTENIDO)
            ], style={**ESTILO_CONTENEDOR, 'marginBottom': '24px'})

        ], style={'maxWidth': '900px', 'margin': '0 auto', 'marginBottom': '40px'}),

        # SECCIÓN 2: SIMULACIÓN INTERACTIVA
        html.Div([
            html.H2(
                "2. Simulación Interactiva",
                style={
                    'color': COLORES['primario'],
                    'borderBottom': f"3px solid {COLORES['primario']}",
                    'paddingBottom': '12px',
                    'marginBottom': '20px',
                    'fontSize': '18px'
                }
            ),

            html.Div([
                html.Div([
                    # Panel de control
                    html.Div([
                        html.H3(
                            "Parámetros del Modelo",
                            style={
                                'color': COLORES['primario'],
                                'borderBottom': f"2px solid {COLORES['primario']}",
                                'paddingBottom': '12px',
                                'marginBottom': '20px',
                                'fontSize': '16px'
                            }
                        ),

                        # Input 1: Población inicial
                        html.Div([
                            html.Label(
                                "Población Inicial P₀",
                                htmlFor="input-p0-clase1",
                                style=ESTILO_LABEL
                            ),
                            dcc.Input(
                                id="input-p0-clase1",
                                type="number",
                                value=100,
                                min=1,
                                max=100000,
                                step=10,
                                style=ESTILO_INPUT,
                                placeholder="Población inicial"
                            ),
                            html.P(
                                "Número inicial de individuos (1 - 100,000)",
                                style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                            )
                        ]),

                        # Input 2: Tasa de crecimiento
                        html.Div([
                            html.Label(
                                "Tasa de Crecimiento (r)",
                                htmlFor="input-r-clase1",
                                style=ESTILO_LABEL
                            ),
                            dcc.Input(
                                id="input-r-clase1",
                                type="number",
                                value=0.03,
                                min=-0.5,
                                max=0.5,
                                step=0.01,
                                style=ESTILO_INPUT,
                                placeholder="Tasa de crecimiento"
                            ),
                            html.P(
                                "Negativo = decaimiento, Positivo = crecimiento (-0.5 a 0.5)",
                                style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                            )
                        ]),

                        # Input 3: Tiempo máximo
                        html.Div([
                            html.Label(
                                "Tiempo Máximo (t)",
                                htmlFor="input-t-clase1",
                                style=ESTILO_LABEL
                            ),
                            dcc.Input(
                                id="input-t-clase1",
                                type="number",
                                value=100,
                                min=1,
                                max=500,
                                step=10,
                                style=ESTILO_INPUT,
                                placeholder="Tiempo máximo"
                            ),
                            html.P(
                                "Duración de la simulación (1 - 500 unidades)",
                                style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                            )
                        ]),

                        # Botón
                        html.Button(
                            "Actualizar Gráfica",
                            id="btn-actualizar-clase1",
                            style=ESTILO_BTN_PRIMARIO,
                            n_clicks=0
                        ),

                        # Panel de métricas
                        html.Div(
                            id="metricas-clase1",
                            style={
                                'marginTop': '20px',
                                'padding': '12px',
                                'backgroundColor': f"rgba(44, 90, 160, 0.1)",
                                'borderRadius': '6px',
                                'borderLeft': f"4px solid {COLORES['primario']}"
                            }
                        )

                    ], style={
                        **ESTILO_CONTENEDOR,
                        'flex': '1',
                        'minWidth': '300px',
                        'maxWidth': '350px'
                    }),

                    # Gráfica
                    html.Div([
                        dcc.Graph(
                            id='grafica-clase1',
                            figure=fig_default,
                            config={
                                'responsive': True,
                                'displayModeBar': True,
                                'displaylogo': False,
                                'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                            }
                        )
                    ], style={
                        'flex': '2',
                        'minWidth': '400px'
                    })

                ], style={
                    'display': 'flex',
                    'flexWrap': 'wrap',
                    'gap': '24px',
                    'justifyContent': 'space-between'
                })

            ], style={'maxWidth': '1200px', 'margin': '0 auto'})

        ], style={**ESTILO_CONTENEDOR, 'marginBottom': '40px'}),

        # SECCIÓN 3: APLICACIONES
        html.Div([
            html.H2(
                "3. Aplicaciones Prácticas",
                style={
                    'color': COLORES['primario'],
                    'borderBottom': f"3px solid {COLORES['primario']}",
                    'paddingBottom': '12px',
                    'marginBottom': '20px',
                    'fontSize': '18px'
                }
            ),

            html.Div([
                html.Div([
                    html.H4("Biología y Epidemiología", style={'color': COLORES['primario'], 'marginBottom': '8px'}),
                    html.P(
                        "Modelado de crecimiento bacteriano, crecimiento viral inicial, "
                        "y dinámicas de población en ecosistemas sin depredadores.",
                        style={'fontSize': '14px'}
                    )
                ], style={**ESTILO_CARD_CONTENIDO, 'flex': '1', 'minWidth': '250px'}),

                html.Div([
                    html.H4("Economía y Finanzas", style={'color': COLORES['primario'], 'marginBottom': '8px'}),
                    html.P(
                        "Crecimiento de inversiones con interés compuesto continuo, "
                        "expansión del mercado, y depreciación de activos.",
                        style={'fontSize': '14px'}
                    )
                ], style={**ESTILO_CARD_CONTENIDO, 'flex': '1', 'minWidth': '250px'}),

                html.Div([
                    html.H4("Tecnología y Redes", style={'color': COLORES['primario'], 'marginBottom': '8px'}),
                    html.P(
                        "Crecimiento de usuarios en redes sociales, propagación de contenido viral, "
                        "y adopción de nueva tecnología.",
                        style={'fontSize': '14px'}
                    )
                ], style={**ESTILO_CARD_CONTENIDO, 'flex': '1', 'minWidth': '250px'})

            ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'gap': '16px',
                'justifyContent': 'space-between',
                'maxWidth': '1000px',
                'margin': '0 auto'
            })

        ], style={**ESTILO_CONTENEDOR, 'marginBottom': '40px', 'maxWidth': '1000px', 'margin': '0 auto 40px'})

    ], style={
        'maxWidth': '1200px',
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
    [Output('grafica-clase1', 'figure'),
     Output('metricas-clase1', 'children')],
    Input('btn-actualizar-clase1', 'n_clicks'),
    [State('input-p0-clase1', 'value'),
     State('input-r-clase1', 'value'),
     State('input-t-clase1', 'value')],
    prevent_initial_call=False
)
def actualizar_simulacion_clase1(n_clicks, p0, r, t_max):
    """
    Actualiza la gráfica y métricas basada en los parámetros ingresados.
    """
    # Validación de parámetros
    if p0 is None or p0 <= 0:
        p0 = 100
    if r is None:
        r = 0.03
    if t_max is None or t_max <= 0:
        t_max = 100

    try:
        # Generar figura
        fig = generar_figura_exponencial(p0, r, t_max)
        
        # Calcular métricas
        t = np.linspace(0, t_max, 300)
        P = p0 * np.exp(r * t)
        
        p_final = P[-1]
        
        # Tiempo de duplicación (si r > 0)
        if r > 0:
            t_duplicacion = np.log(2) / r
            multiplicador = 2 ** (t_max / t_duplicacion)
            interpretacion = f"La población se duplica cada {t_duplicacion:.2f} unidades de tiempo"
        else:
            multiplicador = p_final / p0
            interpretacion = f"Factor de cambio total: {multiplicador:.2f}x"

        # Crear panel de métricas
        metricas = html.Div([
            html.Div([
                html.Span("Población Final: ", style={'fontWeight': '600'}),
                html.Span(f"{p_final:.0f} individuos", style={'color': COLORES['primario'], 'fontWeight': '600'})
            ], style={'marginBottom': '8px'}),
            html.Div([
                html.Span("Factor de Cambio: ", style={'fontWeight': '600'}),
                html.Span(f"{multiplicador:.2f}x", style={'color': COLORES['primario'], 'fontWeight': '600'})
            ], style={'marginBottom': '8px'}),
            html.Div([
                html.Span("Análisis: ", style={'fontWeight': '600'}),
                html.Span(interpretacion, style={'color': COLORES['texto_secundario']})
            ])
        ])

        logger.info(f"Simulación Clase 1 actualizada: P0={p0}, r={r}, t_max={t_max}")
        
        return fig, metricas

    except Exception as e:
        logger.error(f"Error en simulación Clase 1: {str(e)}")
        fig_error = go.Figure()
        fig_error.add_annotation(text="Error en el cálculo", showarrow=False)
        return fig_error, html.Div("Error en el cálculo")
