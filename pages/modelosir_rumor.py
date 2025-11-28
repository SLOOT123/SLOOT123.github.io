"""
Simulación de Propagación de Rumores mediante Modelo SIR
=========================================================

Módulo profesional que implementa un modelo epidemiológico (SIR) para simular
la difusión de rumores en poblaciones, permitiendo comparar escenarios con
diferentes niveles de racionalidad. Utiliza ecuaciones diferenciales ordinarias
para modelar dinámicas de información.

Traducción epidemiológica:
- S (Susceptible): Población ignorante del rumor
- I (Infectado): Personas propagando el rumor
- R (Recuperado): Individuos racionales que dejan de creer

Autor: Sistema de Simulación
Fecha: 2025
Versión: 2.0 (Profesional)
"""

import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.integrate import odeint
from dataclasses import dataclass
from typing import Tuple


# ==========================================
# CONFIGURACIÓN DASH
# ==========================================
dash.register_page(
    __name__,
    path='/Modelo_Rumor',
    name='Dinámicas de Rumor - Modelo SIR'
)


# ==========================================
# 1. CONSTANTES Y CONFIGURACIÓN
# ==========================================
@dataclass
class ConfiguracionUI:
    """Parámetros de diseño y estilo profesional de la interfaz."""
    
    # Paleta de colores (Material Design)
    COLOR_FONDO_PAPEL: str = '#FFF3E0'       # Naranja muy claro
    COLOR_FONDO_GRAFICO: str = '#FFFFFF'    # Blanco puro
    COLOR_GRID: str = '#FFE0B2'              # Naranja suave
    COLOR_TEXTO_PRINCIPAL: str = '#E65100'  # Naranja oscuro
    COLOR_TEXTO_SECUNDARIO: str = '#424242' # Gris oscuro
    COLOR_ZEROLINE: str = '#D32F2F'         # Rojo
    
    # Colores para modelo SIR (Rumor)
    COLOR_SUSCEPTIBLE: str = '#1976D2'      # Azul (Ignoran)
    COLOR_INFECTADO: str = '#F57C00'        # Naranja (Propagan)
    COLOR_RECUPERADO: str = '#388E3C'       # Verde (Racionales)
    
    # Dimensiones y espaciado
    PADDING_CONTENEDOR: str = '25px'
    BORDER_RADIUS: str = '10px'
    SOMBRA_SUAVE: str = '0 4px 8px rgba(0,0,0,0.12)'
    SOMBRA_MEDIA: str = '0 6px 12px rgba(0,0,0,0.15)'
    
    # Tipografía
    FUENTE_PRINCIPAL: str = 'Outfit, Arial, sans-serif'
    TAMAÑO_TITULO: int = 24
    TAMAÑO_SUBTITULO: int = 18
    TAMAÑO_SECCION: int = 14
    TAMAÑO_ETIQUETA: int = 12
    TAMAÑO_CUERPO: int = 11


@dataclass
class ParametrosModelo:
    """Valores por defecto del modelo SIR para rumores."""
    
    POBLACION_TOTAL: int = 275
    TASA_TRANSMISION: float = 0.004
    TASA_RACIONALIDAD_BAJA: float = 0.01
    TASA_RACIONALIDAD_MEDIA: float = 0.02
    PROPAGADORES_INICIALES: int = 1
    RACIONALES_INICIALES: int = 8
    DIAS_SIMULACION: int = 15
    PUNTOS_DISCRETIZACION: int = 200


config = ConfiguracionUI()
params = ParametrosModelo()


# ==========================================
# 2. LÓGICA MATEMÁTICA - MODELO SIR RUMOR
# ==========================================
class ModeloSIRRumor:
    """
    Implementa el modelo SIR (Susceptible-Infectado-Recuperado) para
    propagación de rumores en poblaciones.
    
    Ecuaciones diferenciales:
    - dS/dt = -β·S·I       (Susceptibles que creen el rumor)
    - dI/dt = β·S·I - γ·I  (Balance de propagadores)
    - dR/dt = γ·I          (Racionales que descartan el rumor)
    
    Donde:
    - β: Tasa de transmisión (contacto × credibilidad)
    - γ: Tasa de racionalidad (velocidad de escepticismo)
    """
    
    @staticmethod
    def ecuaciones_diferenciales(y: Tuple[float, float, float],
                                  t: float,
                                  N: int,
                                  beta: float,
                                  gamma: float) -> Tuple[float, float, float]:
        """
        Sistema de ecuaciones diferenciales del modelo SIR.
        
        Parámetros:
            y: tupla (S, I, R) - estado actual
            t: tiempo (variable independiente)
            N: población total
            beta: tasa de transmisión (β)
            gamma: tasa de racionalidad (γ)
            
        Retorna:
            tupla (dS/dt, dI/dt, dR/dt)
        """
        S, I, R = y
        
        # Normalización por población
        dSdt = -beta * S * I / N
        dIdt = (beta * S * I / N) - gamma * I
        dRdt = gamma * I
        
        return dSdt, dIdt, dRdt
    
    @staticmethod
    def resolver(N: int,
                 beta: float,
                 gamma: float,
                 S0: int,
                 I0: int,
                 R0: int,
                 t_max: int,
                 num_puntos: int = 200) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Resuelve numéricamente el sistema de EDO.
        
        Parámetros:
            N: población total
            beta: tasa de transmisión
            gamma: tasa de racionalidad
            S0, I0, R0: condiciones iniciales
            t_max: tiempo máximo de simulación (días)
            num_puntos: resolución temporal
            
        Retorna:
            (t, S, I, R): arrays de tiempo y soluciones
            
        Levanta:
            ValueError: si las condiciones iniciales son inválidas
        """
        # Validación
        if S0 + I0 + R0 != N:
            raise ValueError(
                f"Condiciones iniciales inválidas: S0({S0}) + I0({I0}) + R0({R0}) ≠ N({N})"
            )
        if any(x < 0 for x in [N, beta, gamma, S0, I0, R0, t_max]):
            raise ValueError("Todos los parámetros deben ser no-negativos")
        
        # Discretización temporal
        t = np.linspace(0, t_max, num_puntos)
        y0 = (S0, I0, R0)
        
        # Resolución numérica (método de Runge-Kutta embebido)
        solucion = odeint(
            ModeloSIRRumor.ecuaciones_diferenciales,
            y0, t,
            args=(N, beta, gamma),
            full_output=False
        )
        
        S, I, R = solucion.T
        
        return t, S, I, R
    
    @staticmethod
    def calcular_metricas(t: np.ndarray,
                         I: np.ndarray) -> dict:
        """
        Calcula métricas epidemiológicas relevantes.
        
        Parámetros:
            t: array temporal
            I: array de infectados (propagadores)
            
        Retorna:
            dict: métricas {pico_valor, pico_tiempo, area_bajo_curva}
        """
        pico_idx = np.argmax(I)
        
        return {
            'pico_valor': float(I[pico_idx]),
            'pico_tiempo': float(t[pico_idx]),
            'area_bajo_curva': float(np.trapz(I, t))
        }


# ==========================================
# 3. COMPONENTES DE INTERFAZ
# ==========================================
def crear_entrada_parametro(etiqueta: str,
                            id_componente: str,
                            valor_defecto: float,
                            valor_min: float = 0,
                            paso: float = 0.001,
                            descripcion: str = "") -> html.Div:
    """
    Crea un componente reutilizable de entrada de parámetros.
    
    Incluye:
    - Etiqueta descriptiva con ícono
    - Input con validación
    - Descripción auxiliar (opcional)
    
    Parámetros:
        etiqueta: texto de la etiqueta
        id_componente: identificador único (Dash)
        valor_defecto: valor inicial
        valor_min: mínimo permitido
        paso: incremento/decremento
        descripcion: texto de ayuda
    """
    return html.Div([
        html.Label(
            etiqueta,
            style={
                'fontWeight': '600',
                'color': config.COLOR_TEXTO_PRINCIPAL,
                'fontSize': f'{config.TAMAÑO_ETIQUETA}px',
                'display': 'block',
                'marginBottom': '6px'
            }
        ),
        dcc.Input(
            id=id_componente,
            type="number",
            value=valor_defecto,
            min=valor_min,
            step=paso,
            style={
                'width': '100%',
                'padding': '10px 12px',
                'borderRadius': '6px',
                'border': '2px solid #E0E0E0',
                'marginBottom': '4px',
                'boxSizing': 'border-box',
                'backgroundColor': config.COLOR_FONDO_GRAFICO,
                'color': config.COLOR_TEXTO_SECUNDARIO,
                'fontSize': f'{config.TAMAÑO_CUERPO}px',
                'fontFamily': config.FUENTE_PRINCIPAL,
                'transition': 'border-color 0.2s ease, box-shadow 0.2s ease'
            }
        ),
        html.P(
            descripcion,
            style={
                'fontSize': '10px',
                'color': '#9E9E9E',
                'margin': '4px 0 12px 0',
                'fontStyle': 'italic',
                'lineHeight': '1.3'
            }
        ) if descripcion else None
    ], style={'marginBottom': '0px'})


def crear_panel_parametros() -> html.Div:
    """Crea el panel lateral de control con todos los parámetros."""
    
    return html.Div([
        # Encabezado
        html.Div([
            html.H3(
                "⚙️ Panel de Control",
                style={
                    'color': config.COLOR_TEXTO_PRINCIPAL,
                    'borderBottom': f'3px solid {config.COLOR_GRID}',
                    'paddingBottom': '12px',
                    'marginBottom': '20px',
                    'fontSize': f'{config.TAMAÑO_SUBTITULO}px',
                    'fontWeight': '700'
                }
            ),
            html.P(
                "Configure los parámetros para simular diferentes dinámicas de propagación de rumores.",
                style={
                    'fontSize': f'{config.TAMAÑO_ETIQUETA}px',
                    'color': config.COLOR_TEXTO_SECUNDARIO,
                    'marginBottom': '20px',
                    'lineHeight': '1.4'
                }
            )
        ]),
        
        # Sección 1: Parámetros Generales
        html.Div([
            html.H4(
                "Parámetros Generales",
                style={
                    'color': config.COLOR_TEXTO_PRINCIPAL,
                    'fontSize': f'{config.TAMAÑO_SECCION}px',
                    'marginBottom': '15px',
                    'fontWeight': '600',
                    'borderLeft': f'4px solid {config.COLOR_INFECTADO}',
                    'paddingLeft': '10px'
                }
            ),
            
            crear_entrada_parametro(
                "Población Total (N):",
                "input-N",
                params.POBLACION_TOTAL,
                valor_min=50,
                paso=10,
                descripcion="Tamaño total de la población (50-5000)"
            ),
            
            crear_entrada_parametro(
                "Tasa de Transmisión (β):",
                "input-beta",
                params.TASA_TRANSMISION,
                valor_min=0.0001,
                paso=0.0001,
                descripcion="Probabilidad de contacto × credibilidad"
            ),
            
            crear_entrada_parametro(
                "Días a Simular:",
                "input-days",
                params.DIAS_SIMULACION,
                valor_min=5,
                paso=1,
                descripcion="Horizonte temporal de la simulación"
            ),
        ], style={'marginBottom': '25px'}),
        
        # Sección 2: Racionalidad
        html.Div([
            html.H4(
                "Tasas de Racionalidad (γ)",
                style={
                    'color': config.COLOR_TEXTO_PRINCIPAL,
                    'fontSize': f'{config.TAMAÑO_SECCION}px',
                    'marginBottom': '15px',
                    'fontWeight': '600',
                    'borderLeft': f'4px solid {config.COLOR_RECUPERADO}',
                    'paddingLeft': '10px'
                }
            ),
            
            html.P(
                "Contrasta dos escenarios: uno con baja racionalidad (credulidad alta) "
                "y otro con alta racionalidad (escepticismo alto).",
                style={
                    'fontSize': '10px',
                    'color': '#9E9E9E',
                    'marginBottom': '12px',
                    'lineHeight': '1.3'
                }
            ),
            
            crear_entrada_parametro(
                "Escenario A - Racionalidad Baja (γ₁):",
                "input-gamma1",
                params.TASA_RACIONALIDAD_BAJA,
                valor_min=0.001,
                paso=0.001,
                descripcion="Población poco escéptica"
            ),
            
            crear_entrada_parametro(
                "Escenario B - Racionalidad Alta (γ₂):",
                "input-gamma2",
                params.TASA_RACIONALIDAD_MEDIA,
                valor_min=0.001,
                paso=0.001,
                descripcion="Población muy escéptica"
            ),
        ], style={'marginBottom': '25px'}),
        
        # Sección 3: Condiciones Iniciales
        html.Div([
            html.H4(
                "Condiciones Iniciales",
                style={
                    'color': config.COLOR_TEXTO_PRINCIPAL,
                    'fontSize': f'{config.TAMAÑO_SECCION}px',
                    'marginBottom': '15px',
                    'fontWeight': '600',
                    'borderLeft': f'4px solid {config.COLOR_SUSCEPTIBLE}',
                    'paddingLeft': '10px'
                }
            ),
            
            crear_entrada_parametro(
                "Propagadores Iniciales (I₀):",
                "input-I0",
                params.PROPAGADORES_INICIALES,
                valor_min=1,
                paso=1,
                descripcion="Primeras personas que difunden el rumor"
            ),
            
            crear_entrada_parametro(
                "Racionales Iniciales (R₀):",
                "input-R0",
                params.RACIONALES_INICIALES,
                valor_min=0,
                paso=1,
                descripcion="Personas que descartan el rumor desde el inicio"
            ),
        ], style={'marginBottom': '25px'}),
        
        # Botón de Simulación
        html.Button(
            "▶ Ejecutar Simulación",
            id="btn-simular-rumor",
            style={
                'backgroundColor': config.COLOR_TEXTO_PRINCIPAL,
                'color': config.COLOR_FONDO_GRAFICO,
                'padding': '14px 20px',
                'width': '100%',
                'border': 'none',
                'borderRadius': config.BORDER_RADIUS,
                'cursor': 'pointer',
                'marginTop': '25px',
                'fontSize': f'{config.TAMAÑO_SECCION}px',
                'fontWeight': '700',
                'transition': 'all 0.3s ease',
                'boxShadow': config.SOMBRA_SUAVE
            },
            n_clicks=0
        ),
        
        html.Div(
            "Usa el botón para actualizar la simulación con nuevos parámetros.",
            style={
                'fontSize': '10px',
                'color': '#9E9E9E',
                'marginTop': '12px',
                'textAlign': 'center'
            }
        )
        
    ], style={
        'flex': '1',
        'minWidth': '330px',
        'padding': config.PADDING_CONTENEDOR,
        'backgroundColor': '#FAFAFA',
        'borderRadius': config.BORDER_RADIUS,
        'boxShadow': config.SOMBRA_SUAVE,
        'borderLeft': f'5px solid {config.COLOR_TEXTO_PRINCIPAL}',
        'height': 'fit-content'
    })


# ==========================================
# 4. GENERACIÓN DE VISUALIZACIONES
# ==========================================
class GeneradorVisualizaciones:
    """Factory para crear gráficos interactivos de alta calidad."""
    
    @staticmethod
    def crear_grafico_comparativo(t: np.ndarray,
                                  res_a: Tuple[np.ndarray, np.ndarray, np.ndarray],
                                  res_b: Tuple[np.ndarray, np.ndarray, np.ndarray],
                                  gamma1: float,
                                  gamma2: float) -> go.Figure:
        """
        Crea un gráfico comparativo con dos escenarios lado a lado.
        
        Parámetros:
            t: vector temporal
            res_a: tupla (S, I, R) del escenario A
            res_b: tupla (S, I, R) del escenario B
            gamma1, gamma2: tasas de racionalidad
            
        Retorna:
            go.Figure: gráfico con subplots
        """
        S1, I1, R1 = res_a
        S2, I2, R2 = res_b
        
        # Crear subplots (1x2)
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(
                f"<b>Escenario A: Baja Racionalidad</b><br>γ = {gamma1}",
                f"<b>Escenario B: Alta Racionalidad</b><br>γ = {gamma2}"
            ),
            horizontal_spacing=0.12,
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Escenario A (Líneas sólidas)
        fig.add_trace(go.Scatter(
            x=t, y=S1,
            mode='lines',
            name='Ignoran (S)',
            line=dict(color=config.COLOR_SUSCEPTIBLE, width=3, dash='solid'),
            fill=None,
            hovertemplate='<b>Día %{x:.1f}</b><br>Susceptibles: %{y:.0f}<extra></extra>',
            legendgroup='A'
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=t, y=I1,
            mode='lines',
            name='Propagan (I)',
            line=dict(color=config.COLOR_INFECTADO, width=3, dash='solid'),
            fill=None,
            hovertemplate='<b>Día %{x:.1f}</b><br>Propagadores: %{y:.0f}<extra></extra>',
            legendgroup='A'
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=t, y=R1,
            mode='lines',
            name='Racionales (R)',
            line=dict(color=config.COLOR_RECUPERADO, width=3, dash='solid'),
            fill=None,
            hovertemplate='<b>Día %{x:.1f}</b><br>Racionales: %{y:.0f}<extra></extra>',
            legendgroup='A'
        ), row=1, col=1)
        
        # Escenario B (Líneas punteadas para distinción visual)
        fig.add_trace(go.Scatter(
            x=t, y=S2,
            mode='lines',
            name='Ignoran (S)',
            line=dict(color=config.COLOR_SUSCEPTIBLE, width=3, dash='dash'),
            fill=None,
            hovertemplate='<b>Día %{x:.1f}</b><br>Susceptibles: %{y:.0f}<extra></extra>',
            legendgroup='B',
            showlegend=False
        ), row=1, col=2)
        
        fig.add_trace(go.Scatter(
            x=t, y=I2,
            mode='lines',
            name='Propagan (I)',
            line=dict(color=config.COLOR_INFECTADO, width=3, dash='dash'),
            fill=None,
            hovertemplate='<b>Día %{x:.1f}</b><br>Propagadores: %{y:.0f}<extra></extra>',
            legendgroup='B',
            showlegend=False
        ), row=1, col=2)
        
        fig.add_trace(go.Scatter(
            x=t, y=R2,
            mode='lines',
            name='Racionales (R)',
            line=dict(color=config.COLOR_RECUPERADO, width=3, dash='dash'),
            fill=None,
            hovertemplate='<b>Día %{x:.1f}</b><br>Racionales: %{y:.0f}<extra></extra>',
            legendgroup='B',
            showlegend=False
        ), row=1, col=2)
        
        # Configuración del layout
        fig.update_layout(
            title=dict(
                text='<b>Comparación de Dinámicas de Rumor: Impacto de la Racionalidad</b>',
                font=dict(
                    size=config.TAMAÑO_TITULO,
                    color=config.COLOR_TEXTO_PRINCIPAL,
                    family=config.FUENTE_PRINCIPAL
                ),
                x=0.5, xanchor='center',
                y=0.98, yanchor='top'
            ),
            paper_bgcolor=config.COLOR_FONDO_PAPEL,
            plot_bgcolor=config.COLOR_FONDO_GRAFICO,
            font=dict(
                family=config.FUENTE_PRINCIPAL,
                size=config.TAMAÑO_CUERPO,
                color=config.COLOR_TEXTO_SECUNDARIO
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom', y=-0.15,
                xanchor='center', x=0.5,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#E0E0E0',
                borderwidth=1,
                font=dict(size=config.TAMAÑO_ETIQUETA)
            ),
            hovermode='x unified',
            margin=dict(l=70, r=50, t=120, b=100),
            height=580,
            template='plotly_white'
        )
        
        # Configuración de ejes
        estilo_ejes = dict(
            showgrid=True,
            gridwidth=1,
            gridcolor=config.COLOR_GRID,
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor=config.COLOR_ZEROLINE,
            showline=True,
            linecolor=config.COLOR_TEXTO_SECUNDARIO,
            linewidth=2,
            mirror=True
        )
        
        fig.update_xaxes(
            **estilo_ejes,
            title_text='<b>Tiempo (días)</b>',
            title_font=dict(size=config.TAMAÑO_ETIQUETA, color=config.COLOR_TEXTO_PRINCIPAL)
        )
        
        fig.update_yaxes(
            **estilo_ejes,
            title_text='<b>Población (personas)</b>',
            title_font=dict(size=config.TAMAÑO_ETIQUETA, color=config.COLOR_TEXTO_PRINCIPAL),
            row=1, col=1
        )
        
        fig.update_yaxes(
            **estilo_ejes,
            row=1, col=2
        )
        
        return fig


# ==========================================
# 5. LAYOUT PRINCIPAL
# ==========================================
layout = html.Div([
    
    # Encabezado principal
    html.Div([
        html.H1(
            "🔊 Modelo SIR para Propagación de Rumores",
            style={
                'textAlign': 'center',
                'color': config.COLOR_TEXTO_PRINCIPAL,
                'marginBottom': '8px',
                'fontSize': '32px',
                'fontWeight': '700'
            }
        ),
        html.P(
            "Análisis de dinámicas de información mediante modelado epidemiológico "
            "comparando escenarios de racionalidad poblacional",
            style={
                'textAlign': 'center',
                'color': config.COLOR_TEXTO_SECUNDARIO,
                'marginBottom': '30px',
                'fontSize': '14px',
                'fontStyle': 'italic',
                'lineHeight': '1.5'
            }
        )
    ]),
    
    # Contenedor principal (Flexbox)
    html.Div([
        
        # Panel izquierdo: Parámetros
        crear_panel_parametros(),
        
        # Panel derecho: Visualización y Estadísticas
        html.Div([
            dcc.Graph(
                id='grafica-rumor-comparativa',
                style={'width': '100%'},
                config={'responsive': True, 'displayModeBar': True}
            ),
            
            # Sección de estadísticas
            html.Div(
                id='stats-output',
                style={
                    'marginTop': '25px',
                    'padding': config.PADDING_CONTENEDOR,
                    'backgroundColor': config.COLOR_FONDO_PAPEL,
                    'borderRadius': config.BORDER_RADIUS,
                    'borderLeft': f'5px solid {config.COLOR_INFECTADO}',
                    'boxShadow': config.SOMBRA_SUAVE
                }
            )
        ], style={
            'flex': '2.5',
            'minWidth': '500px',
            'padding': '10px'
        })
        
    ], style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'gap': '30px',
        'maxWidth': '1600px',
        'margin': '0 auto',
        'alignItems': 'flex-start'
    }),
    
    # Pie de página informativo
    html.Hr(style={'borderTop': '2px solid #E0E0E0', 'margin': '40px 0 20px 0'}),
    html.Div([
        html.P(
            "Modelo SIR (Susceptible-Infectado-Recuperado): Ecuaciones diferenciales "
            "dS/dt = -βSI/N, dI/dt = βSI/N - γI, dR/dt = γI. "
            "β = tasa de transmisión | γ = tasa de racionalidad. "
            "Aplicación a dinámicas de información y propagación viral de contenidos.",
            style={
                'textAlign': 'center',
                'fontSize': '11px',
                'color': '#9E9E9E',
                'marginTop': '20px',
                'lineHeight': '1.5'
            }
        )
    ])
    
], style={
    'padding': '40px 20px',
    'fontFamily': config.FUENTE_PRINCIPAL,
    'backgroundColor': '#FAFAFA',
    'minHeight': '100vh'
})


# ==========================================
# 6. CALLBACKS - INTERACTIVIDAD
# ==========================================
@callback(
    [Output('grafica-rumor-comparativa', 'figure'),
     Output('stats-output', 'children')],
    Input('btn-simular-rumor', 'n_clicks'),
    [State('input-N', 'value'),
     State('input-beta', 'value'),
     State('input-gamma1', 'value'),
     State('input-gamma2', 'value'),
     State('input-I0', 'value'),
     State('input-R0', 'value'),
     State('input-days', 'value')],
    prevent_initial_call=False
)
def ejecutar_simulacion(n_clicks: int,
                       N: float,
                       beta: float,
                       gamma1: float,
                       gamma2: float,
                       I0: int,
                       R0: int,
                       days: int):
    """
    Callback principal que ejecuta la simulación y actualiza visualizaciones.
    
    Parámetros:
        n_clicks: contador de clics del botón
        N, beta, gamma1, gamma2, I0, R0, days: parámetros del modelo
        
    Retorna:
        tupla (figura, estadísticas): gráfico y análisis
    """
    
    # Asignación de valores por defecto
    N = N or params.POBLACION_TOTAL
    beta = beta or params.TASA_TRANSMISION
    gamma1 = gamma1 or params.TASA_RACIONALIDAD_BAJA
    gamma2 = gamma2 or params.TASA_RACIONALIDAD_MEDIA
    I0 = I0 or params.PROPAGADORES_INICIALES
    R0 = R0 or params.RACIONALES_INICIALES
    days = days or params.DIAS_SIMULACION
    
    # Cálculo de susceptibles iniciales
    S0 = N - I0 - R0
    
    # Validación de parámetros
    try:
        if S0 < 0:
            raise ValueError(
                f"Condiciones iniciales inválidas: S₀ ({S0}) < 0. "
                f"Asegúrese que I₀ + R₀ ≤ N"
            )
        
        if not all([N > 0, beta > 0, gamma1 > 0, gamma2 > 0, days > 0]):
            raise ValueError("Todos los parámetros deben ser positivos")
        
        # Resolución del modelo
        t, S1, I1, R1 = ModeloSIRRumor.resolver(N, beta, gamma1, S0, I0, R0, days)
        _, S2, I2, R2 = ModeloSIRRumor.resolver(N, beta, gamma2, S0, I0, R0, days)
        
        # Cálculo de métricas
        metricas_a = ModeloSIRRumor.calcular_metricas(t, I1)
        metricas_b = ModeloSIRRumor.calcular_metricas(t, I2)
        
        # Generación del gráfico
        figura = GeneradorVisualizaciones.crear_grafico_comparativo(
            t, (S1, I1, R1), (S2, I2, R2), gamma1, gamma2
        )
        
        # Generación de estadísticas
        estadisticas = html.Div([
            html.H3(
                "📊 Análisis Comparativo",
                style={
                    'color': config.COLOR_TEXTO_PRINCIPAL,
                    'marginBottom': '15px',
                    'fontSize': f'{config.TAMAÑO_SECCION}px'
                }
            ),
            
            html.Div([
                # Escenario A
                html.Div([
                    html.H4(
                        f"Escenario A (γ₁ = {gamma1})",
                        style={'color': config.COLOR_INFECTADO, 'marginBottom': '10px'}
                    ),
                    html.P(
                        f"📈 Pico de propagadores: {metricas_a['pico_valor']:.0f} personas",
                        style={'marginBottom': '6px'}
                    ),
                    html.P(
                        f"⏱ Alcanzado en: Día {metricas_a['pico_tiempo']:.1f}",
                        style={'marginBottom': '6px'}
                    ),
                    html.P(
                        f"📊 Área bajo curva: {metricas_a['area_bajo_curva']:.0f} personas-día",
                        style={'marginBottom': '0px'}
                    ),
                ], style={'flex': '1', 'padding': '15px', 'backgroundColor': 'rgba(245, 124, 0, 0.08)', 'borderRadius': '6px'}),
                
                # Escenario B
                html.Div([
                    html.H4(
                        f"Escenario B (γ₂ = {gamma2})",
                        style={'color': config.COLOR_RECUPERADO, 'marginBottom': '10px'}
                    ),
                    html.P(
                        f"📈 Pico de propagadores: {metricas_b['pico_valor']:.0f} personas",
                        style={'marginBottom': '6px'}
                    ),
                    html.P(
                        f"⏱ Alcanzado en: Día {metricas_b['pico_tiempo']:.1f}",
                        style={'marginBottom': '6px'}
                    ),
                    html.P(
                        f"📊 Área bajo curva: {metricas_b['area_bajo_curva']:.0f} personas-día",
                        style={'marginBottom': '0px'}
                    ),
                ], style={'flex': '1', 'padding': '15px', 'backgroundColor': 'rgba(56, 142, 60, 0.08)', 'borderRadius': '6px'}),
            ], style={'display': 'flex', 'gap': '15px', 'marginBottom': '15px'}),
            
            # Insights
            html.Div([
                html.P(
                    f"💡 <b>Insight:</b> "
                    f"Con mayor racionalidad (γ₂ = {gamma2}), el pico se reduce en "
                    f"{(metricas_a['pico_valor'] - metricas_b['pico_valor']):.0f} propagadores "
                    f"({100 * (metricas_a['pico_valor'] - metricas_b['pico_valor']) / metricas_a['pico_valor']:.1f}%) "
                    f"y ocurre {abs(metricas_b['pico_tiempo'] - metricas_a['pico_tiempo']):.1f} días "
                    f"{'más tarde' if metricas_b['pico_tiempo'] > metricas_a['pico_tiempo'] else 'más temprano'}.",
                    style={
                        'fontSize': f'{config.TAMAÑO_ETIQUETA}px',
                        'color': config.COLOR_TEXTO_SECUNDARIO,
                        'lineHeight': '1.5'
                    }
                )
            ])
        ])
        
        return figura, estadisticas
    
    except ValueError as e:
        # Gráfico de error
        fig_error = go.Figure()
        fig_error.add_annotation(
            text=f"⚠️ <b>Error de Validación:</b><br>{str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color='#D32F2F'),
            bgcolor='#FFCDD2',
            bordercolor='#D32F2F',
            borderwidth=2,
            borderpad=20
        )
        fig_error.update_layout(
            paper_bgcolor=config.COLOR_FONDO_PAPEL,
            xaxis_visible=False,
            yaxis_visible=False,
            height=580
        )
        
        # Estadísticas de error
        stats_error = html.Div([
            html.H3("❌ Error en la Simulación", style={'color': '#D32F2F'}),
            html.P(str(e), style={'color': config.COLOR_TEXTO_SECUNDARIO})
        ])
        
        return fig_error, stats_error
    
    except Exception as e:
        # Error no esperado
        fig_error = go.Figure()
        fig_error.add_annotation(
            text=f"❌ <b>Error Inesperado:</b><br>{type(e).__name__}: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color='#D32F2F'),
            bgcolor='#FFCDD2',
            bordercolor='#D32F2F',
            borderwidth=2,
            borderpad=15
        )
        fig_error.update_layout(
            paper_bgcolor=config.COLOR_FONDO_PAPEL,
            xaxis_visible=False,
            yaxis_visible=False,
            height=580
        )
        
        stats_error = html.Div([
            html.H3("❌ Error del Sistema", style={'color': '#D32F2F'}),
            html.P("Se ha producido un error inesperado. Verifique los parámetros e intente de nuevo.",
                   style={'color': config.COLOR_TEXTO_SECUNDARIO})
        ])
        
        return fig_error, stats_error
