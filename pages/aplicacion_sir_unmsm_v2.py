"""
Aplicaciones Integradas del Modelo SIR - UNMSM (v2 Multi-página Optimizada)
==================================================================

Módulo profesional optimizado con visualizaciones mejoradas y diseño responsive.
Implementa tres aplicaciones del modelo epidemiológico SIR en contextos reales.

Mejoras visuales implementadas:
- Gráficos con áreas semitransparentes y líneas más definidas
- Tooltips informativos y interactivos
- Diseño responsive que se adapta a diferentes tamaños de pantalla
- Colores más vibrantes y contrastantes
- Animaciones suaves en hover
- Layout mejorado con mejor distribución del espacio

Autor: Sistema de Simulación
Fecha: 2025
Versión: 3.2 (Visualización Profesional)
"""

import dash
from dash import dcc, html, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from scipy.integrate import odeint
from dataclasses import dataclass
from typing import Tuple, Dict, Callable, Optional
from abc import ABC, abstractmethod
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Registrar como página Dash multi-página (si app existe)
try:
    dash.register_page(
        __name__,
        path='/Aplicacion_SIR_UNMSM_v2',
        name='Modelo SIR UNMSM v2'
    )
except Exception as e:
    logger.info(f"Página será registrada automáticamente: {e}")


# ==========================================
# 1. CONSTANTES Y CONFIGURACIÓN MEJORADA
# ==========================================
@dataclass
class ConfiguracionUI:
    """Configuración centralizada de estilos y colores profesionales mejorados."""
    
    # Paleta de colores vibrante y profesional
    COLOR_FONDO_PRINCIPAL: str = '#FFFFFF'
    COLOR_FONDO_PAPEL: str = '#F8FAFC'
    COLOR_FONDO_GRAFICO: str = '#FFFFFF'
    COLOR_GRID: str = '#E2E8F0'
    
    # Colores temáticos mejorados
    COLOR_TITULO: str = '#1E40AF'
    COLOR_TEXTO_PRINCIPAL: str = '#1E293B'
    COLOR_TEXTO_SECUNDARIO: str = '#64748B'
    
    # Colores SIR mejorados (más vibrantes y accesibles)
    COLOR_S: str = '#3B82F6'      # Azul vibrante (Susceptible)
    COLOR_I: str = '#EF4444'      # Rojo intenso (Infectado)
    COLOR_R: str = '#10B981'      # Verde esmeralda (Recuperado)
    
    # Colores de áreas semitransparentes
    COLOR_S_AREA: str = 'rgba(59, 130, 246, 0.15)'
    COLOR_I_AREA: str = 'rgba(239, 68, 68, 0.15)'
    COLOR_R_AREA: str = 'rgba(16, 185, 129, 0.15)'
    
    # Estilos mejorados
    PADDING: str = '24px'
    BORDER_RADIUS: str = '12px'
    SOMBRA: str = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
    FUENTE: str = 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    
    # Tamaños mejorados
    TAMAÑO_TITULO: int = 28
    TAMAÑO_SUBTITULO: int = 20
    TAMAÑO_SECCION: int = 16
    TAMAÑO_ETIQUETA: int = 14
    TAMAÑO_TEXTO: int = 15


@dataclass
class ParametrosAplicaciones:
    """Valores por defecto para cada aplicación con rango de validación."""
    
    # Influenza
    POBLACION_FLU: int = 10000
    TASA_TRANSMISION_FLU: float = 0.0003
    TASA_RECUPERACION_FLU: float = 0.4
    RANGO_POBLACION_FLU: Tuple[int, int] = (1000, 50000)
    
    # Rumor
    POBLACION_RUMOR: int = 1000
    TASA_TRANSMISION_RUMOR: float = 0.005
    TASA_RACIONALIZACION_RUMOR: float = 0.02
    PROPAGADORES_INICIALES: int = 5
    RACIONALES_INICIALES: int = 10
    
    # App Móvil
    POBLACION_APP: int = 10000
    TASA_ADOPCION_APP: float = 0.0008
    TASA_ABANDONO_APP: float = 0.03


# Instancias globales (singleton)
config = ConfiguracionUI()
params = ParametrosAplicaciones()


# ==========================================
# 2. MODELOS MATEMÁTICOS - ARQUITECTURA ABSTRACTA
# ==========================================
class ModeloSIR(ABC):
    """Clase base abstracta para todas las variantes del modelo SIR."""
    
    @staticmethod
    @abstractmethod
    def ecuaciones(y: Tuple[float, float, float],
                   t: float,
                   N: int,
                   **kwargs) -> Tuple[float, float, float]:
        pass
    
    @staticmethod
    def resolver(N: int,
                 S0: int,
                 I0: int,
                 R0: int,
                 t_max: int,
                 ecuaciones: Callable,
                 **params_modelo) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Resuelve numéricamente el sistema de EDO con mejor manejo de errores.
        """
        # Validación estricta mejorada
        if not all(isinstance(x, (int, float)) and x >= 0 for x in [S0, I0, R0, N, t_max]):
            raise ValueError("Todos los parámetros deben ser números no-negativos")
        
        if abs(S0 + I0 + R0 - N) > 1e-6:  # Tolerancia para floats
            raise ValueError(
                f"Inconsistencia: S0({S0}) + I0({I0}) + R0({R0}) ≠ N({N}). "
                "Las condiciones iniciales deben sumar la población total."
            )
        
        try:
            # Discretización más fina para gráficos suaves
            t = np.linspace(0, t_max, 300)
            y0 = (S0, I0, R0)
            
            solucion = odeint(
                ecuaciones,
                y0, t,
                args=(N, *params_modelo.values()) if params_modelo else (N,),
                full_output=False,
                rtol=1e-8,
                atol=1e-11
            )
            
            S, I, R = solucion.T
            
            # Validación de salida mejorada
            if np.any(np.isnan(S)) or np.any(np.isnan(I)) or np.any(np.isnan(R)):
                raise RuntimeError("La integración produjo valores NaN")
            
            # Asegurar que los valores sean positivos
            S = np.maximum(S, 0)
            I = np.maximum(I, 0)
            R = np.maximum(R, 0)
            
            return t, S, I, R
            
        except Exception as e:
            logger.error(f"Error en resolución de EDO: {str(e)}")
            raise


class ModeloSIRClasico(ModeloSIR):
    """Modelo SIR clásico para influenza y adopción de app móvil."""
    
    @staticmethod
    def ecuaciones(y: Tuple[float, float, float],
                   t: float,
                   N: int,
                   beta: float,
                   gamma: float) -> Tuple[float, float, float]:
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = (beta * S * I / N) - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt


class ModeloSIRRumor(ModeloSIR):
    """Modelo SIR modificado para propagación de rumores con racionales."""
    
    @staticmethod
    def ecuaciones(y: Tuple[float, float, float],
                   t: float,
                   N: int,
                   beta: float,
                   gamma: float) -> Tuple[float, float, float]:
        S, I, R = y
        dSdt = -beta * S * I / N
        dIdt = (beta * S * I / N) - gamma * I * R / N
        dRdt = gamma * I * R / N
        return dSdt, dIdt, dRdt


# ==========================================
# 3. GENERADOR DE VISUALIZACIONES MEJORADO
# ==========================================
class GeneradorGraficos:
    """Factory para crear gráficos Plotly profesionales mejorados."""
    
    @staticmethod
    def crear_grafico_sir(t: np.ndarray,
                         S: np.ndarray,
                         I: np.ndarray,
                         R: np.ndarray,
                         titulo: str,
                         etiquetas: Optional[Dict[str, str]] = None,
                         altura: int = 500) -> go.Figure:
        """
        Crea un gráfico SIR interactivo con estilo profesional mejorado.
        
        Mejoras implementadas:
        - Áreas semitransparentes bajo las curvas
        - Líneas más gruesas y definidas
        - Tooltips más informativos
        - Mejor distribución de colores
        - Ejes más legibles
        - Animaciones en hover
        - Marcador de pico de infección
        """
        # Etiquetas por defecto
        if etiquetas is None:
            etiquetas = {
                'S': 'Susceptibles',
                'I': 'Infectados',
                'R': 'Recuperados'
            }
        
        fig = go.Figure()

        # Encontrar el pico de infectados para la anotación
        idx_pico = np.argmax(I)
        t_pico = t[idx_pico]
        i_pico = I[idx_pico]
        
        # Traza S: Susceptibles (con área mejorada)
        fig.add_trace(go.Scatter(
            x=t, y=S,
            mode='lines',
            name=etiquetas['S'],
            line=dict(
                color=config.COLOR_S, 
                width=4,
                shape='spline',
                smoothing=1.3
            ),
            fill='tozeroy',
            fillcolor=config.COLOR_S_AREA,
            hovertemplate=(
                '<b>Día %{x:.1f}</b><br>'
                f'<span style="color:{config.COLOR_S}">●</span> '
                f'{etiquetas["S"]}: <b>%{{y:.0f}}</b> personas<br>'
                '<extra></extra>'
            ),
            hoverlabel=dict(bgcolor=config.COLOR_S)
        ))
        
        # Traza I: Infectados (con área mejorada)
        fig.add_trace(go.Scatter(
            x=t, y=I,
            mode='lines',
            name=etiquetas['I'],
            line=dict(
                color=config.COLOR_I, 
                width=4,
                shape='spline',
                smoothing=1.3
            ),
            fill='tozeroy',
            fillcolor=config.COLOR_I_AREA,
            hovertemplate=(
                '<b>Día %{x:.1f}</b><br>'
                f'<span style="color:{config.COLOR_I}">●</span> '
                f'{etiquetas["I"]}: <b>%{{y:.0f}}</b> personas<br>'
                '<extra></extra>'
            ),
            hoverlabel=dict(bgcolor=config.COLOR_I)
        ))
        
        # Traza R: Recuperados (con área mejorada)
        fig.add_trace(go.Scatter(
            x=t, y=R,
            mode='lines',
            name=etiquetas['R'],
            line=dict(
                color=config.COLOR_R, 
                width=4,
                shape='spline',
                smoothing=1.3
            ),
            fill='tozeroy',
            fillcolor=config.COLOR_R_AREA,
            hovertemplate=(
                '<b>Día %{x:.1f}</b><br>'
                f'<span style="color:{config.COLOR_R}">●</span> '
                f'{etiquetas["R"]}: <b>%{{y:.0f}}</b> personas<br>'
                '<extra></extra>'
            ),
            hoverlabel=dict(bgcolor=config.COLOR_R)
        ))

        # Añadir marcador del pico
        fig.add_trace(go.Scatter(
            x=[t_pico], y=[i_pico],
            mode='markers',
            name='Pico de Infección',
            marker=dict(
                color='red',
                size=12,
                symbol='star',
                line=dict(width=2, color='white')
            ),
            hoverinfo='skip'
        ))

        fig.add_annotation(
            x=t_pico, y=i_pico,
            text=f"Pico: {int(i_pico):,}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#475569",
            ax=0,
            ay=-40,
            font=dict(size=12, color="#475569", family=config.FUENTE),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#E2E8F0",
            borderwidth=1,
            borderpad=4
        )
        
        # Configuración del layout mejorada
        fig.update_layout(
            title=dict(
                text=f'<b>{titulo}</b>',
                font=dict(
                    size=config.TAMAÑO_SUBTITULO,
                    color=config.COLOR_TITULO,
                    family=config.FUENTE
                ),
                x=0.05,
                xanchor='left',
                y=0.95,
                yanchor='top'
            ),
            xaxis_title=dict(
                text='<b>Tiempo (días)</b>',
                font=dict(
                    size=config.TAMAÑO_ETIQUETA,
                    color=config.COLOR_TEXTO_SECUNDARIO
                )
            ),
            yaxis_title=dict(
                text='<b>Población (personas)</b>',
                font=dict(
                    size=config.TAMAÑO_ETIQUETA,
                    color=config.COLOR_TEXTO_SECUNDARIO
                )
            ),
            paper_bgcolor=config.COLOR_FONDO_PAPEL,
            plot_bgcolor=config.COLOR_FONDO_GRAFICO,
            font=dict(
                family=config.FUENTE,
                size=config.TAMAÑO_TEXTO,
                color=config.COLOR_TEXTO_PRINCIPAL
            ),
            hovermode='x unified',
            hoverdistance=100,
            spikedistance=1000,
            margin=dict(l=80, r=40, t=120, b=80),
            height=altura,
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#E2E8F0',
                borderwidth=1,
                font=dict(size=config.TAMAÑO_ETIQUETA)
            )
        )
        
        # Configuración de ejes mejorada
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor=config.COLOR_GRID,
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor='#CBD5E1',
            mirror=False,
            showspikes=True,
            spikecolor='#64748B',
            spikethickness=1,
            spikedash='dot'
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor=config.COLOR_GRID,
            zeroline=False,
            showline=True,
            linewidth=2,
            linecolor='#CBD5E1',
            mirror=False
        )
        
        return fig
    
    @staticmethod
    def crear_grafico_fase(S: np.ndarray,
                          I: np.ndarray,
                          titulo: str = "Plano de Fase (S vs I)") -> go.Figure:
        """
        Crea un gráfico de plano de fase (Susceptibles vs Infectados).
        Útil para visualizar la trayectoria de la epidemia.
        """
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=S, y=I,
            mode='lines',
            name='Trayectoria',
            line=dict(
                color=config.COLOR_TITULO,
                width=3,
                shape='spline'
            ),
            hovertemplate=(
                '<b>Susceptibles</b>: %{x:.0f}<br>'
                '<b>Infectados</b>: %{y:.0f}<br>'
                '<extra></extra>'
            )
        ))

        # Marcador de inicio
        fig.add_trace(go.Scatter(
            x=[S[0]], y=[I[0]],
            mode='markers',
            name='Inicio',
            marker=dict(color='green', size=10, symbol='circle'),
            showlegend=True
        ))

        # Marcador de fin
        fig.add_trace(go.Scatter(
            x=[S[-1]], y=[I[-1]],
            mode='markers',
            name='Fin',
            marker=dict(color='red', size=10, symbol='x'),
            showlegend=True
        ))

        fig.update_layout(
            title=dict(
                text=f'<b>{titulo}</b>',
                font=dict(size=config.TAMAÑO_SUBTITULO, color=config.COLOR_TITULO)
            ),
            xaxis_title="Susceptibles (S)",
            yaxis_title="Infectados (I)",
            paper_bgcolor=config.COLOR_FONDO_PAPEL,
            plot_bgcolor=config.COLOR_FONDO_GRAFICO,
            font=dict(family=config.FUENTE),
            margin=dict(l=60, r=40, t=80, b=60),
            height=400,
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        fig.update_xaxes(autorange="reversed") # S disminuye con el tiempo

        return fig
    
    @staticmethod
    def crear_grafico_error(mensaje: str) -> go.Figure:
        """Crea un gráfico de error profesional."""
        fig = go.Figure()
        fig.add_annotation(
            text=f"⚠️ {mensaje}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, 
            xanchor='center',
            yanchor='middle',
            showarrow=False,
            font=dict(size=16, color='#DC2626')
        )
        fig.update_layout(
            paper_bgcolor=config.COLOR_FONDO_PAPEL,
            plot_bgcolor=config.COLOR_FONDO_GRAFICO,
            margin=dict(l=40, r=40, t=40, b=40),
            height=400
        )
        return fig


# ==========================================
# 4. GENERADOR DE COMPONENTES UI MEJORADO
# ==========================================
class GeneradorComponentesUI:
    """Factory para crear componentes de interfaz reutilizables mejorados."""
    
    @staticmethod
    def crear_slider(etiqueta: str,
                    id_slider: str,
                    min_val: float,
                    max_val: float,
                    valor_defecto: float,
                    paso: float,
                    marks: Optional[Dict] = None,
                    tooltip_prefix: str = "",
                    tooltip_suffix: str = "") -> html.Div:
        """
        Crea un slider profesional mejorado con tooltips descriptivos.
        """
        if marks is None:
            marks = {}
        
        return html.Div([
            html.Label(
                etiqueta,
                style={
                    'fontWeight': '600',
                    'color': config.COLOR_TEXTO_PRINCIPAL,
                    'fontSize': f'{config.TAMAÑO_ETIQUETA}px',
                    'marginBottom': '12px',
                    'display': 'block'
                }
            ),
            dcc.Slider(
                id=id_slider,
                min=min_val,
                max=max_val,
                step=paso,
                value=valor_defecto,
                marks=marks,
                tooltip={
                    "placement": "bottom", 
                    "always_visible": True
                },
                className="slider-profesional"
            )
        ], style={'marginBottom': '30px'})
    
    @staticmethod
    def crear_input_numero(etiqueta: str,
                          id_input: str,
                          valor_defecto: float,
                          min_val: float = 0,
                          paso: float = 1,
                          placeholder: str = "") -> html.Div:
        """Crea un input numérico con validación HTML5 mejorado."""
        return html.Div([
            html.Label(
                etiqueta,
                style={
                    'fontWeight': '600',
                    'color': config.COLOR_TEXTO_PRINCIPAL,
                    'fontSize': f'{config.TAMAÑO_ETIQUETA}px',
                    'marginBottom': '8px',
                    'display': 'block'
                }
            ),
            dcc.Input(
                id=id_input,
                type='number',
                value=valor_defecto,
                min=min_val,
                step=paso,
                placeholder=placeholder,
                style={
                    'width': '100%',
                    'padding': '12px 16px',
                    'borderRadius': config.BORDER_RADIUS,
                    'border': f'2px solid #E2E8F0',
                    'fontSize': f'{config.TAMAÑO_TEXTO}px',
                    'transition': 'all 0.2s ease',
                    'backgroundColor': '#FFFFFF'
                }
            )
        ], style={'marginBottom': '20px'})
    
    @staticmethod
    def crear_tarjeta_estadisticas(titulo: str, 
                                  metricas: Dict[str, float],
                                  color_borde: str) -> html.Div:
        """Crea una tarjeta de estadísticas profesional."""
        return html.Div([
            html.H4(
                titulo,
                style={
                    'marginBottom': '16px',
                    'fontWeight': '600',
                    'color': config.COLOR_TEXTO_PRINCIPAL,
                    'fontSize': f'{config.TAMAÑO_SECCION}px'
                }
            ),
            *[
                html.Div([
                    html.Span("• ", style={'color': color_borde, 'fontWeight': 'bold'}),
                    html.Span(
                        f"{nombre}: ",
                        style={'fontWeight': '500', 'color': config.COLOR_TEXTO_PRINCIPAL}
                    ),
                    html.Span(
                        f"{valor:.1f}" if isinstance(valor, float) else f"{valor}",
                        style={'fontWeight': '600', 'color': color_borde}
                    )
                ], style={'marginBottom': '8px', 'lineHeight': '1.4'})
                for nombre, valor in metricas.items()
            ]
        ], style={
            'padding': config.PADDING,
            'backgroundColor': '#FFFFFF',
            'borderLeft': f'4px solid {color_borde}',
            'borderRadius': config.BORDER_RADIUS,
            'boxShadow': config.SOMBRA,
            'marginTop': '20px'
        })


# ==========================================
# 5. LAYOUT PRINCIPAL MEJORADO
# ==========================================
def crear_layout_principal() -> html.Div:
    """
    Crea el layout completo mejorado con diseño responsive.
    """
    return html.Div([
        # Encabezado mejorado
        html.Div([
            html.Div([
                html.H1(
                    "🎯 Aplicaciones del Modelo SIR",
                    style={
                        'textAlign': 'center',
                        'color': config.COLOR_TITULO,
                        'marginBottom': '8px',
                        'fontSize': f'{config.TAMAÑO_TITULO}px',
                        'fontWeight': '700',
                        'lineHeight': '1.2'
                    }
                ),
                html.H3(
                    "Universidad Nacional Mayor de San Marcos - Técnicas de Modelamiento",
                    style={
                        'textAlign': 'center',
                        'color': config.COLOR_TEXTO_SECUNDARIO,
                        'marginTop': '0px',
                        'marginBottom': '0px',
                        'fontSize': f'{config.TAMAÑO_SECCION}px',
                        'fontWeight': '400'
                    }
                ),
                html.P(
                    "Simulaciones interactivas de propagación en diferentes contextos",
                    style={
                        'textAlign': 'center',
                        'color': config.COLOR_TEXTO_SECUNDARIO,
                        'marginTop': '8px',
                        'fontSize': f'{config.TAMAÑO_ETIQUETA}px'
                    }
                )
            ], style={'maxWidth': '800px', 'margin': '0 auto'})
        ], style={
            'padding': '40px 20px',
            'backgroundColor': '#F8FAFC',
            'borderBottom': f'1px solid #E2E8F0',
            'marginBottom': '0px'
        }),
        
        # Contenedor principal mejorado
        html.Div([
            dcc.Tabs(
                id='tabs-aplicaciones',
                value='tab-influenza',
                children=[
                    # Tab Influenza
                    dcc.Tab(
                        label='🦠 Brote Influenza',
                        value='tab-influenza',
                        children=[
                            html.Div([
                                html.Div([
                                    html.H3(
                                        "Modelado de Brote de Influenza",
                                        style={
                                            'color': config.COLOR_TITULO,
                                            'marginBottom': '16px',
                                            'fontWeight': '600',
                                            'fontSize': f'{config.TAMAÑO_SUBTITULO}px'
                                        }
                                    ),
                                    html.P(
                                        "Simula la propagación de un virus respiratorio en una población cerrada. "
                                        "El modelo SIR clásico describe cómo una enfermedad se propaga entre "
                                        "susceptibles (S), infectados (I) y recuperados (R).",
                                        style={
                                            'color': config.COLOR_TEXTO_SECUNDARIO,
                                            'marginBottom': '30px',
                                            'lineHeight': '1.6',
                                            'fontSize': f'{config.TAMAÑO_TEXTO}px'
                                        }
                                    ),
                                    
                                    html.Div([
                                        # Panel de controles
                                        html.Div([
                                            html.H4(
                                                "📊 Parámetros del Modelo",
                                                style={
                                                    'color': config.COLOR_TEXTO_PRINCIPAL,
                                                    'marginBottom': '20px',
                                                    'fontWeight': '600'
                                                }
                                            ),
                                            GeneradorComponentesUI.crear_input_numero(
                                                "Población Total (N):",
                                                'input-n-flu',
                                                params.POBLACION_FLU,
                                                min_val=1000,
                                                paso=100,
                                                placeholder="Ej: 10000"
                                            ),
                                            
                                            GeneradorComponentesUI.crear_slider(
                                                "Tasa de Transmisión (β):",
                                                'slider-b-flu',
                                                0.00001,
                                                0.001,
                                                params.TASA_TRANSMISION_FLU,
                                                0.00001,
                                                marks={
                                                    0.00001: 'Muy Baja',
                                                    0.0001: 'Baja',
                                                    0.0005: 'Media',
                                                    0.001: 'Alta'
                                                },
                                                tooltip_prefix="β = "
                                            ),
                                            
                                            GeneradorComponentesUI.crear_slider(
                                                "Tasa de Recuperación (γ):",
                                                'slider-k-flu',
                                                0.1,
                                                1.0,
                                                params.TASA_RECUPERACION_FLU,
                                                0.05,
                                                marks={
                                                    0.1: '10%',
                                                    0.4: '40%',
                                                    0.7: '70%',
                                                    1.0: '100%'
                                                },
                                                tooltip_prefix="γ = "
                                            ),
                                        ], style={
                                            'flex': '1',
                                            'minWidth': '320px',
                                            'padding': config.PADDING,
                                            'backgroundColor': '#FFFFFF',
                                            'borderRadius': config.BORDER_RADIUS,
                                            'boxShadow': config.SOMBRA
                                        }),
                                        
                                        # Panel de gráfico y estadísticas
                                        html.Div([
                                            dcc.Graph(
                                                id='grafico-influenza',
                                                style={'height': '500px'},
                                                config={
                                                    'responsive': True,
                                                    'displayModeBar': True,
                                                    'displaylogo': False,
                                                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
                                                    'toImageButtonOptions': {
                                                        'format': 'png',
                                                        'filename': 'modelo_sir_influenza',
                                                        'height': 500,
                                                        'width': 800,
                                                        'scale': 2
                                                    }
                                                }
                                            ),
                                            html.Div(id='stats-influenza'),
                                            
                                            # Nuevo: Gráfico de Fase
                                            html.Div([
                                                dcc.Graph(
                                                    id='grafico-fase-influenza',
                                                    style={'height': '400px'},
                                                    config={'displayModeBar': False}
                                                )
                                            ], style={'marginTop': '30px'}),

                                            # Nuevo: Botón de Descarga
                                            html.Div([
                                                html.Button("📥 Descargar Datos (CSV)", id="btn-download-influenza", 
                                                           style={
                                                               'backgroundColor': config.COLOR_TITULO,
                                                               'color': 'white',
                                                               'padding': '10px 20px',
                                                               'border': 'none',
                                                               'borderRadius': config.BORDER_RADIUS,
                                                               'cursor': 'pointer',
                                                               'fontSize': config.TAMAÑO_TEXTO,
                                                               'fontWeight': '600',
                                                               'marginTop': '20px',
                                                               'width': '100%'
                                                           }),
                                                dcc.Download(id="download-dataframe-influenza")
                                            ])
                                        ], style={'flex': '2', 'minWidth': '500px'})
                                    ], style={
                                        'display': 'flex',
                                        'gap': '30px',
                                        'flexWrap': 'wrap',
                                        'alignItems': 'flex-start'
                                    })
                                ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px'})
                            ], style={'padding': config.PADDING})
                        ]
                    ),
                    
                    # Tabs para rumor y app (estructura similar)
                    dcc.Tab(
                        label='🔊 Propagación Rumor',
                        value='tab-rumor',
                        children=[
                            html.Div([
                                html.Div([
                                    html.H3(
                                        "Modelado de Propagación de Rumores",
                                        style={
                                            'color': config.COLOR_TITULO,
                                            'marginBottom': '16px',
                                            'fontWeight': '600'
                                        }
                                    ),
                                    html.P(
                                        "Simula cómo los rumores se propagan en una población con individuos racionales. "
                                        "El modelo SIR modificado incluye la interacción entre propagadores e individuos escépticos.",
                                        style={
                                            'color': config.COLOR_TEXTO_SECUNDARIO,
                                            'marginBottom': '30px',
                                            'lineHeight': '1.6'
                                        }
                                    ),
                                    
                                    html.Div([
                                        html.Div([
                                            html.H4(
                                                "📊 Parámetros del Rumor",
                                                style={
                                                    'color': config.COLOR_TEXTO_PRINCIPAL,
                                                    'marginBottom': '20px',
                                                    'fontWeight': '600'
                                                }
                                            ),
                                            GeneradorComponentesUI.crear_slider(
                                                "Tasa de Propagación (β):",
                                                'slider-b-rumor',
                                                0.001,
                                                0.02,
                                                params.TASA_TRANSMISION_RUMOR,
                                                0.001,
                                                marks={0.001: '0.001', 0.01: '0.01', 0.02: '0.02'}
                                            ),
                                            
                                            GeneradorComponentesUI.crear_slider(
                                                "Tasa de Racionalización (γ):",
                                                'slider-k-rumor',
                                                0.005,
                                                0.1,
                                                params.TASA_RACIONALIZACION_RUMOR,
                                                0.005,
                                                marks={0.01: '0.01', 0.05: '0.05', 0.1: '0.1'}
                                            ),
                                            
                                            GeneradorComponentesUI.crear_slider(
                                                "Propagadores Iniciales (I₀):",
                                                'slider-i0-rumor',
                                                1,
                                                50,
                                                params.PROPAGADORES_INICIALES,
                                                1
                                            ),
                                            
                                            GeneradorComponentesUI.crear_slider(
                                                "Racionales Iniciales (R₀):",
                                                'slider-r0-rumor',
                                                0,
                                                100,
                                                params.RACIONALES_INICIALES,
                                                5
                                            ),
                                        ], style={
                                            'flex': '1',
                                            'minWidth': '320px',
                                            'padding': config.PADDING,
                                            'backgroundColor': '#FFFFFF',
                                            'borderRadius': config.BORDER_RADIUS,
                                            'boxShadow': config.SOMBRA
                                        }),
                                        
                                        html.Div([
                                            dcc.Graph(
                                                id='grafico-rumor',
                                                style={'height': '500px'},
                                                config={
                                                    'responsive': True,
                                                    'displayModeBar': True,
                                                    'displaylogo': False
                                                }
                                            ),
                                            html.Div(id='stats-rumor')
                                        ], style={'flex': '2', 'minWidth': '500px'})
                                    ], style={
                                        'display': 'flex',
                                        'gap': '30px',
                                        'flexWrap': 'wrap',
                                        'alignItems': 'flex-start'
                                    })
                                ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px'})
                            ], style={'padding': config.PADDING})
                        ]
                    ),
                    
                    dcc.Tab(
                        label='📱 Adopción App Móvil',
                        value='tab-app',
                        children=[
                            html.Div([
                                html.Div([
                                    html.H3(
                                        "Modelado de Adopción de Aplicación Móvil",
                                        style={
                                            'color': config.COLOR_TITULO,
                                            'marginBottom': '16px',
                                            'fontWeight': '600'
                                        }
                                    ),
                                    html.P(
                                        "Simula el ciclo de vida de una aplicación móvil: desde no usuarios (S), "
                                        "usuarios activos (I) hasta usuarios que desinstalaron (R). "
                                        "Similar a dinámicas virales de adopción de tecnología.",
                                        style={
                                            'color': config.COLOR_TEXTO_SECUNDARIO,
                                            'marginBottom': '30px',
                                            'lineHeight': '1.6'
                                        }
                                    ),
                                    
                                    html.Div([
                                        html.Div([
                                            html.H4(
                                                "📊 Parámetros de Adopción",
                                                style={
                                                    'color': config.COLOR_TEXTO_PRINCIPAL,
                                                    'marginBottom': '20px',
                                                    'fontWeight': '600'
                                                }
                                            ),
                                            GeneradorComponentesUI.crear_slider(
                                                "Viralidad (β - Tasa de Adopción):",
                                                'slider-b-app',
                                                0.0001,
                                                0.005,
                                                params.TASA_ADOPCION_APP,
                                                0.0001,
                                                marks={
                                                    0.0001: 'Fracaso',
                                                    0.001: 'Viral',
                                                    0.005: 'Explosivo'
                                                }
                                            ),
                                            
                                            GeneradorComponentesUI.crear_slider(
                                                "Abandono (γ - Tasa de Desinstalación):",
                                                'slider-k-app',
                                                0.01,
                                                0.2,
                                                params.TASA_ABANDONO_APP,
                                                0.01,
                                                marks={
                                                    0.05: 'Buena',
                                                    0.1: 'Regular',
                                                    0.2: 'Mala'
                                                }
                                            ),
                                        ], style={
                                            'flex': '1',
                                            'minWidth': '320px',
                                            'padding': config.PADDING,
                                            'backgroundColor': '#FFFFFF',
                                            'borderRadius': config.BORDER_RADIUS,
                                            'boxShadow': config.SOMBRA
                                        }),
                                        
                                        html.Div([
                                            dcc.Graph(
                                                id='grafico-app',
                                                style={'height': '500px'},
                                                config={
                                                    'responsive': True,
                                                    'displayModeBar': True,
                                                    'displaylogo': False
                                                }
                                            ),
                                            html.Div(id='stats-app')
                                        ], style={'flex': '2', 'minWidth': '500px'})
                                    ], style={
                                        'display': 'flex',
                                        'gap': '30px',
                                        'flexWrap': 'wrap',
                                        'alignItems': 'flex-start'
                                    })
                                ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px'})
                            ], style={'padding': config.PADDING})
                        ]
                    )
                ],
                style={
                    'borderBottom': '1px solid #E2E8F0',
                    'padding': '0px 20px'
                },
                content_style={
                    'border': 'none',
                    'padding': '0px'
                }
            )
        ], style={'minHeight': 'calc(100vh - 200px)'})
        
    ], style={
        'fontFamily': config.FUENTE,
        'backgroundColor': config.COLOR_FONDO_PRINCIPAL,
        'minHeight': '100vh',
        'margin': '0',
        'padding': '0'
    }),
    dcc.Store(id='store-page-init', data=False)  # Para rastrear inicialización


# Asignar el layout (requerido para Dash multi-página)
layout = crear_layout_principal()


# ==========================================
# 6. CALLBACKS MEJORADOS
# ==========================================
@callback(
    [Output('grafico-influenza', 'figure'),
     Output('stats-influenza', 'children'),
     Output('grafico-fase-influenza', 'figure')],
    [Input('input-n-flu', 'value'),
     Input('slider-b-flu', 'value'),
     Input('slider-k-flu', 'value')],
    prevent_initial_call=False
)
def actualizar_influenza(N: Optional[float],
                        beta: Optional[float],
                        gamma: Optional[float]) -> Tuple[go.Figure, html.Div, go.Figure]:
    """
    Callback mejorado para actualización de simulación de influenza.
    """
    # Asignación con valores por defecto mejorada
    try:
        N = int(N) if N and N > 0 else params.POBLACION_FLU
        beta = float(beta) if beta and beta > 0 else params.TASA_TRANSMISION_FLU
        gamma = float(gamma) if gamma and gamma > 0 else params.TASA_RECUPERACION_FLU
        
        # Validación adicional
        if N < 100:
            raise ValueError("La población debe ser al menos 100 personas")
        if beta <= 0 or gamma <= 0:
            raise ValueError("Las tasas deben ser positivas")
        
        # Condiciones iniciales
        I0, R0 = 1, 0
        S0 = N - I0 - R0
        
        if S0 < 0:
            raise ValueError("Población inicial inconsistente")
        
        # Resolución
        t, S, I, R = ModeloSIR.resolver(
            N, S0, I0, R0, 40,
            ModeloSIRClasico.ecuaciones,
            beta=beta, gamma=gamma
        )
        
        # Métricas mejoradas
        metricas = CalculadoraMetricas.calcular_metricas_influenza(t, I, beta, gamma)
        
        # Gráfico mejorado
        fig = GeneradorGraficos.crear_grafico_sir(
            t, S, I, R,
            f'Brote de Influenza en Población de {N:,} Personas',
            {'S': 'Susceptibles', 'I': 'Infectados', 'R': 'Recuperados'},
            altura=500
        )
        
        # Gráfico de Fase
        fig_fase = GeneradorGraficos.crear_grafico_fase(S, I, "Plano de Fase: Influenza (S vs I)")
        
        # Estadísticas mejoradas
        stats = GeneradorComponentesUI.crear_tarjeta_estadisticas(
            "📈 Métricas del Brote",
            {
                'Pico de infectados': metricas['pico_valor'],
                'Día del pico': metricas['pico_tiempo'],
                'Infectados día 6': metricas['dia_6'],
                'Impacto total': metricas['area_bajo_curva'],
                'R0 (Número Reproductivo Básico)': metricas.get('R0', 0)
            },
            config.COLOR_I
        )
        
        return fig, stats, fig_fase
        
    except ValueError as e:
        logger.warning(f"Error de validación en influenza: {str(e)}")
        fig_error = GeneradorGraficos.crear_grafico_error(f"Error de validación: {str(e)}")
        return fig_error, html.Div(), fig_error
    
    except Exception as e:
        logger.error(f"Error inesperado en influenza: {str(e)}")
        fig_error = GeneradorGraficos.crear_grafico_error("Error inesperado en la simulación")
        return fig_error, html.Div(), fig_error


@callback(
    Output("download-dataframe-influenza", "data"),
    Input("btn-download-influenza", "n_clicks"),
    [State('input-n-flu', 'value'),
     State('slider-b-flu', 'value'),
     State('slider-k-flu', 'value')],
    prevent_initial_call=True
)
def descargar_influenza(n_clicks, N, beta, gamma):
    """Callback para descargar datos de simulación."""
    if not n_clicks:
        return dash.no_update
        
    try:
        N = int(N) if N and N > 0 else params.POBLACION_FLU
        beta = float(beta) if beta and beta > 0 else params.TASA_TRANSMISION_FLU
        gamma = float(gamma) if gamma and gamma > 0 else params.TASA_RECUPERACION_FLU
        
        I0, R0 = 1, 0
        S0 = N - I0 - R0
        
        t, S, I, R = ModeloSIR.resolver(
            N, S0, I0, R0, 40,
            ModeloSIRClasico.ecuaciones,
            beta=beta, gamma=gamma
        )
        
        df = pd.DataFrame({
            "Dia": t,
            "Susceptibles": S,
            "Infectados": I,
            "Recuperados": R
        })
        
        return dcc.send_data_frame(df.to_csv, "simulacion_influenza.csv")
        
    except Exception as e:
        logger.error(f"Error en descarga: {e}")
        return dash.no_update


@callback(
    [Output('grafico-rumor', 'figure'),
     Output('stats-rumor', 'children')],
    [Input('slider-b-rumor', 'value'),
     Input('slider-k-rumor', 'value'),
     Input('slider-r0-rumor', 'value'),
     Input('slider-i0-rumor', 'value')],
    prevent_initial_call=False
)
def actualizar_rumor(beta: Optional[float],
                    gamma: Optional[float],
                    R0: Optional[int],
                    I0: Optional[int]) -> Tuple[go.Figure, html.Div]:
    """Callback mejorado para propagación de rumor."""
    try:
        beta = float(beta) if beta else params.TASA_TRANSMISION_RUMOR
        gamma = float(gamma) if gamma else params.TASA_RACIONALIZACION_RUMOR
        R0 = int(R0) if R0 else params.RACIONALES_INICIALES
        I0 = int(I0) if I0 else params.PROPAGADORES_INICIALES
        
        N = params.POBLACION_RUMOR
        S0 = N - I0 - R0
        
        if S0 < 0:
            raise ValueError(f"Condiciones iniciales inválidas: I₀({I0}) + R₀({R0}) > N({N})")
        
        t, S, I, R = ModeloSIR.resolver(
            N, S0, I0, R0, 30,
            ModeloSIRRumor.ecuaciones,
            beta=beta, gamma=gamma
        )
        
        metricas = CalculadoraMetricas.calcular_metricas(t, I)
        
        fig = GeneradorGraficos.crear_grafico_sir(
            t, S, I, R,
            'Propagación de Rumor - Modelo SIR Modificado',
            {'S': 'Creen Rumor', 'I': 'Propagan', 'R': 'Racionales'},
            altura=500
        )
        
        stats = GeneradorComponentesUI.crear_tarjeta_estadisticas(
            "📊 Estadísticas del Rumor",
            {
                'Máximo propagadores': metricas['pico_valor'],
                'Día del pico': metricas['pico_tiempo'],
                'Duración total': metricas['area_bajo_curva'] / metricas['pico_valor'] if metricas['pico_valor'] > 0 else 0
            },
            config.COLOR_I
        )
        
        return fig, stats
        
    except Exception as e:
        logger.error(f"Error en rumor: {str(e)}")
        fig_error = GeneradorGraficos.crear_grafico_error("Error en la simulación del rumor")
        return fig_error, html.Div()


@callback(
    [Output('grafico-app', 'figure'),
     Output('stats-app', 'children')],
    [Input('slider-b-app', 'value'),
     Input('slider-k-app', 'value')],
    prevent_initial_call=False
)
def actualizar_app(beta: Optional[float],
                  gamma: Optional[float]) -> Tuple[go.Figure, html.Div]:
    """Callback mejorado para adopción de app móvil."""
    try:
        beta = float(beta) if beta else params.TASA_ADOPCION_APP
        gamma = float(gamma) if gamma else params.TASA_ABANDONO_APP
        
        N = params.POBLACION_APP
        I0, R0 = 50, 0  # Más usuarios iniciales para mejor visualización
        S0 = N - I0 - R0
        
        t, S, I, R = ModeloSIR.resolver(
            N, S0, I0, R0, 180,  # Período más largo para app
            ModeloSIRClasico.ecuaciones,
            beta=beta, gamma=gamma
        )
        
        metricas = CalculadoraMetricas.calcular_metricas(t, I)
        
        fig = GeneradorGraficos.crear_grafico_sir(
            t, S, I, R,
            'Ciclo de Vida: Adopción de Aplicación Móvil',
            {'S': 'No Usuarios', 'I': 'Usuarios Activos', 'R': 'Desinstalados'},
            altura=500
        )
        
        # Calificaciones mejoradas
        viralidad = "🚀 Explosiva" if beta > 0.003 else ("📈 Viral" if beta > 0.001 else "📉 Orgánica")
        retencion = "⭐ Excelente" if gamma < 0.05 else ("✓ Buena" if gamma < 0.1 else "✗ Mejorable")
        
        stats = GeneradorComponentesUI.crear_tarjeta_estadisticas(
            "📱 Métricas de Adopción",
            {
                'Usuarios máximos': metricas['pico_valor'],
                'Día del pico': metricas['pico_tiempo'],
                'Viralidad': viralidad,
                'Retención': retencion
            },
            config.COLOR_R
        )
        
        return fig, stats
        
    except Exception as e:
        logger.error(f"Error en app móvil: {str(e)}")
        fig_error = GeneradorGraficos.crear_grafico_error("Error en la simulación de adopción")
        return fig_error, html.Div()


# ==========================================
# 7. CALCULADORA DE MÉTRICAS (complemento)
# ==========================================
class CalculadoraMetricas:
    """Calcula métricas epidemiológicas de las simulaciones."""
    
    @staticmethod
    def calcular_metricas(t: np.ndarray,
                         I: np.ndarray) -> Dict[str, float]:
        """
        Calcula métricas estándar de propagación.
        """
        pico_idx = np.argmax(I)
        return {
            'pico_valor': float(np.max(I)),
            'pico_tiempo': float(t[pico_idx]),
            'area_bajo_curva': float(np.trapz(I, t))
        }

    @staticmethod
    def calcular_r0(beta: float, gamma: float) -> float:
        """Calcula el Número Reproductivo Básico (R0)."""
        return beta / gamma if gamma > 0 else 0.0
    
    @staticmethod
    def calcular_metricas_influenza(t: np.ndarray,
                                   I: np.ndarray,
                                   beta: float = 0,
                                   gamma: float = 0) -> Dict[str, float]:
        """Calcula métricas específicas para influenza."""
        metricas = CalculadoraMetricas.calcular_metricas(t, I)
        
        # Métrica específica: infectados en día 6
        día_6_idx = np.argmin(np.abs(t - 6))
        metricas['dia_6'] = float(I[día_6_idx])
        
        if beta > 0 and gamma > 0:
            metricas['R0'] = CalculadoraMetricas.calcular_r0(beta, gamma)
        
        return metricas

