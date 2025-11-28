
"""
Modelo SIR - Epidemiología Computacional
========================================

Aplicación interactiva para simular dinámicas epidemiológicas usando
el modelo SIR (Susceptibles-Infectados-Recuperados). Incluye validación
robusta, análisis de R₀ y diseño profesional.

Autor: Equipo de Análisis
Versión: 2.0 (Profesional)
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint
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
    path='/modelo-sir',
    name='Modelo SIR'
)

# ==========================================
# CONSTANTES Y CONFIGURACIÓN
# ==========================================

# Paleta de colores profesional
COLORES = {
    'primario': '#2C5AA0',          # Azul corporativo
    'secundario': '#E74C3C',        # Rojo para énfasis
    'exito': '#27AE60',             # Verde
    'advertencia': '#F39C12',       # Naranja
    'fondo_claro': '#ECEFF1',       # Gris muy claro
    'fondo_oscuro': '#FFFFFF',      # Blanco puro
    'texto_primario': '#2C3E50',    # Gris oscuro
    'texto_secundario': '#7F8C8D',  # Gris medio
    'borde': '#BDC3C7',             # Gris claro
    'grid': '#ECF0F1',              # Grid tenue
    
    # Colores específicos para SIR
    'susceptibles': '#3498DB',      # Azul claro (Susceptibles)
    'infectados': '#E74C3C',        # Rojo (Infectados)
    'recuperados': '#27AE60'        # Verde (Recuperados)
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

# Rangos de validación
VALIDACION = {
    'n_min': 10,
    'n_max': 1000000,
    'beta_min': 0.001,
    'beta_max': 2.0,
    'gamma_min': 0.001,
    'gamma_max': 2.0,
    'i0_min': 1,
    'i0_max': 100000,
    't_min': 1,
    't_max': 500
}

# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def validar_parametros_sir(n, beta, gamma, i0, t_max):
    """
    Valida los parámetros del modelo SIR.
    
    Retorna:
        tuple: (es_valido, mensaje_error)
    """
    errores = []
    
    if n is None:
        errores.append("La población total es requerida")
    elif n < VALIDACION['n_min'] or n > VALIDACION['n_max']:
        errores.append(f"N debe estar entre {VALIDACION['n_min']} y {VALIDACION['n_max']}")
    
    if beta is None:
        errores.append("La tasa de transmisión es requerida")
    elif beta < VALIDACION['beta_min'] or beta > VALIDACION['beta_max']:
        errores.append(f"β debe estar entre {VALIDACION['beta_min']} y {VALIDACION['beta_max']}")
    
    if gamma is None:
        errores.append("La tasa de recuperación es requerida")
    elif gamma < VALIDACION['gamma_min'] or gamma > VALIDACION['gamma_max']:
        errores.append(f"γ debe estar entre {VALIDACION['gamma_min']} y {VALIDACION['gamma_max']}")
    
    if i0 is None:
        errores.append("Los infectados iniciales son requeridos")
    elif i0 < VALIDACION['i0_min'] or i0 > VALIDACION['i0_max']:
        errores.append(f"I₀ debe estar entre {VALIDACION['i0_min']} y {VALIDACION['i0_max']}")
    
    if t_max is None:
        errores.append("El tiempo máximo es requerido")
    elif t_max < VALIDACION['t_min'] or t_max > VALIDACION['t_max']:
        errores.append(f"t debe estar entre {VALIDACION['t_min']} y {VALIDACION['t_max']}")
    
    if n and i0 and i0 >= n:
        errores.append("Los infectados iniciales I₀ no pueden ser mayores o iguales a la población total N")
    
    return len(errores) == 0, " | ".join(errores) if errores else ""


def modelo_sir(y, t, beta, gamma, n):
    """
    Define el sistema de ecuaciones diferenciales del modelo SIR.
    
    Parámetros:
        y: [S, I, R] - Estado actual
        t: Tiempo
        beta: Tasa de transmisión
        gamma: Tasa de recuperación
        n: Población total
    
    Retorna:
        [dS/dt, dI/dt, dR/dt]
    """
    S, I, R = y
    
    # Asegurar no negatividad
    S = max(0, min(S, n))
    I = max(0, min(I, n))
    
    dS_dt = -beta * S * I / n
    dI_dt = beta * S * I / n - gamma * I
    dR_dt = gamma * I
    
    return [dS_dt, dI_dt, dR_dt]


def calcular_sir(n, beta, gamma, i0, t_max, puntos=300):
    """
    Calcula la evolución del modelo SIR usando integración numérica.
    
    Parámetros:
        n (float): Población total
        beta (float): Tasa de transmisión
        gamma (float): Tasa de recuperación
        i0 (float): Infectados iniciales
        t_max (float): Tiempo máximo de simulación
        puntos (int): Cantidad de puntos para discretizar
    
    Retorna:
        tuple: (t, S, I, R, r0_val) - arrays y valor de R₀
    """
    s0 = n - i0
    r0 = 0
    y0 = [s0, i0, r0]
    
    t = np.linspace(0, t_max, puntos)
    
    try:
        with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
            solucion = odeint(modelo_sir, y0, t, args=(beta, gamma, n))
            S, I, R = solucion.T
            S = np.maximum(S, 0)
            I = np.maximum(I, 0)
            R = np.maximum(R, 0)
    except Exception as e:
        logger.error(f"Error en cálculo SIR: {str(e)}")
        S = np.full_like(t, s0)
        I = np.full_like(t, i0)
        R = np.full_like(t, r0)
    
    # Calcular R₀ (número reproductivo básico)
    r0_val = beta / gamma if gamma != 0 else 0
    
    return t, S, I, R, r0_val


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
        height=500
    )
    return fig


# ==========================================
# LAYOUT DE LA PÁGINA
# ==========================================

layout = html.Div([
    # Header
    html.Div([
        html.H1(
            "Modelo SIR - Epidemiología Computacional",
            style={
                'textAlign': 'center',
                'color': COLORES['primario'],
                'fontFamily': 'Segoe UI, Arial, sans-serif',
                'marginBottom': '8px',
                'marginTop': '0px'
            }
        ),
        html.P(
            "Simulación de dinámicas epidemiológicas: Susceptibles → Infectados → Recuperados",
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
                    "Parámetros Epidemiológicos",
                    style={
                        'color': COLORES['primario'],
                        'borderBottom': f"2px solid {COLORES['primario']}",
                        'paddingBottom': '12px',
                        'marginBottom': '20px',
                        'fontSize': '16px'
                    }
                ),

                html.P(
                    "Ajuste los parámetros para simular diferentes escenarios epidemiológicos",
                    style={
                        'fontSize': '13px',
                        'color': COLORES['texto_secundario'],
                        'marginBottom': '20px',
                        'fontStyle': 'italic'
                    }
                ),

                # Grupo de entrada 1: Población total
                html.Div([
                    html.Label(
                        "Población Total (N)",
                        htmlFor="input-n-sir",
                        style=ESTILO_LABEL
                    ),
                    dcc.Input(
                        id="input-n-sir",
                        type="number",
                        value=10000,
                        min=VALIDACION['n_min'],
                        max=VALIDACION['n_max'],
                        step=100,
                        style=ESTILO_INPUT,
                        placeholder="Población total"
                    ),
                    html.P(
                        "Tamaño de la población en estudio",
                        style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                    )
                ]),

                # Grupo de entrada 2: Tasa de transmisión
                html.Div([
                    html.Label(
                        "Tasa de Transmisión (β)",
                        htmlFor="input-b-sir",
                        style=ESTILO_LABEL
                    ),
                    dcc.Input(
                        id="input-b-sir",
                        type="number",
                        value=0.5,
                        min=VALIDACION['beta_min'],
                        max=VALIDACION['beta_max'],
                        step=0.05,
                        style=ESTILO_INPUT,
                        placeholder="Tasa de transmisión"
                    ),
                    html.P(
                        "Contactos efectivos por infectado por día (0.001 - 2.0)",
                        style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                    )
                ]),

                # Grupo de entrada 3: Tasa de recuperación
                html.Div([
                    html.Label(
                        "Tasa de Recuperación (γ)",
                        htmlFor="input-g-sir",
                        style=ESTILO_LABEL
                    ),
                    dcc.Input(
                        id="input-g-sir",
                        type="number",
                        value=0.1,
                        min=VALIDACION['gamma_min'],
                        max=VALIDACION['gamma_max'],
                        step=0.05,
                        style=ESTILO_INPUT,
                        placeholder="Tasa de recuperación"
                    ),
                    html.P(
                        "Proporción de recuperación diaria (1/γ = período infeccioso)",
                        style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                    )
                ]),

                # Grupo de entrada 4: Infectados iniciales
                html.Div([
                    html.Label(
                        "Infectados Iniciales (I₀)",
                        htmlFor="input-I0-sir",
                        style=ESTILO_LABEL
                    ),
                    dcc.Input(
                        id="input-I0-sir",
                        type="number",
                        value=10,
                        min=VALIDACION['i0_min'],
                        max=VALIDACION['i0_max'],
                        step=1,
                        style=ESTILO_INPUT,
                        placeholder="Infectados iniciales"
                    ),
                    html.P(
                        "Número de personas infectadas al inicio",
                        style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                    )
                ]),

                # Grupo de entrada 5: Tiempo máximo
                html.Div([
                    html.Label(
                        "Tiempo de Simulación (días)",
                        htmlFor="input-tiempo-sir",
                        style=ESTILO_LABEL
                    ),
                    dcc.Input(
                        id="input-tiempo-sir",
                        type="number",
                        value=150,
                        min=VALIDACION['t_min'],
                        max=VALIDACION['t_max'],
                        step=10,
                        style=ESTILO_INPUT,
                        placeholder="Días a simular"
                    ),
                    html.P(
                        "Duración de la epidemia a simular",
                        style={'fontSize': '12px', 'color': COLORES['texto_secundario'], 'marginTop': '-10px'}
                    )
                ]),

                # Botón de acción
                html.Button(
                    "Generar Simulación",
                    id="btn-generar-sir",
                    style=ESTILO_BTN_PRIMARIO,
                    n_clicks=0
                ),

                # Área de mensajes
                html.Div(
                    id="mensaje-validacion-sir",
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
                        id='grafica-sir',
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
                        "Indicadores Epidemiológicos",
                        style={
                            'color': COLORES['primario'],
                            'marginTop': '20px',
                            'marginBottom': '12px'
                        }
                    ),
                    html.Div(
                        id="estadisticas-panel-sir",
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
    [Output('grafica-sir', 'figure'),
     Output('estadisticas-panel-sir', 'children'),
     Output('mensaje-validacion-sir', 'children'),
     Output('mensaje-validacion-sir', 'style')],
    Input('btn-generar-sir', 'n_clicks'),
    [State('input-n-sir', 'value'),
     State('input-b-sir', 'value'),
     State('input-g-sir', 'value'),
     State('input-I0-sir', 'value'),
     State('input-tiempo-sir', 'value')],
    prevent_initial_call=False
)
def simular_sir(n_clicks, n, beta, gamma, i0, t_max):
    """
    Ejecuta la simulación del modelo SIR y actualiza la gráfica.
    """
    # Validar parámetros
    es_valido, mensaje_error = validar_parametros_sir(n, beta, gamma, i0, t_max)

    if not es_valido:
        logger.warning(f"Parámetros inválidos SIR: {mensaje_error}")
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

    # Calcular dinámica epidemiológica
    try:
        t, S, I, R, r0_val = calcular_sir(n, beta, gamma, i0, t_max, puntos=300)
        logger.info(f"Simulación SIR calculada: N={n}, β={beta}, γ={gamma}, I₀={i0}, R₀={r0_val:.3f}")
    except Exception as e:
        logger.error(f"Error en cálculo SIR: {str(e)}")
        fig_error = generar_figura_error("Error en el cálculo de la simulación")
        return fig_error, [], "Error interno", {'display': 'none'}

    # Crear trazos
    trace_susceptibles = go.Scatter(
        x=t,
        y=S,
        mode='lines',
        name='Susceptibles (S)',
        line=dict(
            color=COLORES['susceptibles'],
            width=3
        ),
        hovertemplate='<b>Día:</b> %{x:.1f}<br><b>Susceptibles:</b> %{y:.0f}<extra></extra>'
    )

    trace_infectados = go.Scatter(
        x=t,
        y=I,
        mode='lines',
        name='Infectados (I)',
        line=dict(
            color=COLORES['infectados'],
            width=3
        ),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.15)',
        hovertemplate='<b>Día:</b> %{x:.1f}<br><b>Infectados:</b> %{y:.0f}<extra></extra>'
    )

    trace_recuperados = go.Scatter(
        x=t,
        y=R,
        mode='lines',
        name='Recuperados (R)',
        line=dict(
            color=COLORES['recuperados'],
            width=3
        ),
        hovertemplate='<b>Día:</b> %{x:.1f}<br><b>Recuperados:</b> %{y:.0f}<extra></extra>'
    )

    # Construir figura
    fig = go.Figure(data=[trace_susceptibles, trace_infectados, trace_recuperados])

    # Determinar si es pandemia (R₀ > 1)
    tipo_epidemia = "Pandemia (R₀ > 1)" if r0_val > 1 else "Epidemia Controlada (R₀ ≤ 1)"
    color_titulo = COLORES['secundario'] if r0_val > 1 else COLORES['exito']

    fig.update_layout(
        title={
            'text': f'<b>Dinámica del Modelo SIR</b><br><sub>{tipo_epidemia} | R₀ = {r0_val:.3f}</sub>',
            'font': {'size': 18, 'color': color_titulo},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Tiempo (días)',
        yaxis_title='Número de personas',
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

        margin=dict(l=60, r=40, t=100, b=60),
        height=500
    )

    # Calcular estadísticas
    pico_infectados = np.max(I)
    dia_pico = t[np.argmax(I)] if len(I) > 0 else 0
    total_infectados = i0 + (R[-1] if len(R) > 0 else 0)
    tasa_ataque = (total_infectados / n * 100) if n > 0 else 0
    dias_infeccion = 1 / gamma if gamma != 0 else 0

    # Crear tarjetas de estadísticas
    estadisticas = [
        html.Div([
            html.P("R₀ (Número Reproductivo)", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{r0_val:.3f}", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['primario']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(44, 90, 160, 0.08)", 'borderRadius': '6px'}),

        html.Div([
            html.P("Pico de Infectados", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{pico_infectados:.0f}", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['infectados']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(231, 76, 60, 0.08)", 'borderRadius': '6px'}),

        html.Div([
            html.P("Día del Pico", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{dia_pico:.1f}", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['advertencia']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(243, 156, 18, 0.08)", 'borderRadius': '6px'}),

        html.Div([
            html.P("Tasa de Ataque (%)", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{tasa_ataque:.1f}%", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['exito']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(39, 174, 96, 0.08)", 'borderRadius': '6px'}),

        html.Div([
            html.P("Días de Infección (1/γ)", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{dias_infeccion:.1f}", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['primario']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(44, 90, 160, 0.08)", 'borderRadius': '6px'}),

        html.Div([
            html.P("Total Infectados", style={'margin': '0px', 'fontSize': '12px', 'color': COLORES['texto_secundario']}),
            html.P(f"{total_infectados:.0f}", style={'margin': '8px 0px 0px', 'fontSize': '20px', 'fontWeight': '600', 'color': COLORES['infectados']})
        ], style={'padding': '12px', 'backgroundColor': f"rgba(231, 76, 60, 0.08)", 'borderRadius': '6px'})
    ]

    return fig, estadisticas, "", {'display': 'none'}