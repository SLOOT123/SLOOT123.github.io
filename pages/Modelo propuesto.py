import dash
from dash import html, dcc, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

# Registrar esta página en Dash multipage
dash.register_page(__name__, path='/Modelo_Propuesto', name='Modelo Propuesto SIR')

# ================================
# 1. Configuración Visual y Estilos
# ================================
class Estilos:
    COLOR_FONDO_PAPEL = '#E3F2FD'  # Azul claro
    COLOR_FONDO_GRAFICO = 'white'
    COLOR_GRID = '#FFE0B2'  # Naranja suave
    COLOR_TEXTO_PRINCIPAL = '#1565C0'  # Azul oscuro
    COLOR_TEXTO_SECUNDARIO = 'black'
    COLOR_ZEROLINE = 'red'
    COLOR_S = "blue"
    COLOR_I = "red"
    COLOR_R = "green"
    TRANSITION = 'border-color 0.3s ease'

# ================================
# 2. Modelo Matemático SIR
# ================================
class ModeloSIR:
    def __init__(self, N, b, k, I0):
        self.N = N
        self.b = b
        self.k = k
        self.I0 = I0

    def deriv(self, y, t):
        S, I, R = y
        dSdt = -self.b * S * I
        dIdt = self.b * S * I - self.k * I
        dRdt = self.k * I
        return dSdt, dIdt, dRdt

    def resolver(self, t_max, num_puntos=200):
        S0 = self.N - self.I0
        R0 = 0
        y0 = (S0, self.I0, R0)
        t = np.linspace(0, t_max, num_puntos)
        ret = odeint(self.deriv, y0, t)
        S, I, R = ret.T
        return t, S, I, R

# ================================
# 3. Creación de Componentes UI
# ================================
def crear_input(label_text, input_id, valor, min_val=0, step=1, tipo="number"):
    return html.Div([
        html.Label(label_text, style={'fontWeight':'bold', 'color': Estilos.COLOR_TEXTO_SECUNDARIO, 'fontSize':'14px'}),
        dcc.Input(
            id=input_id,
            type=tipo,
            value=valor,
            min=min_val,
            step=step,
            style={
                'width': '100%', 'padding':'8px', 'borderRadius':'5px',
                'border':'1px solid #ccc', 'marginTop':'5px', 'marginBottom':'15px',
                'boxSizing':'border-box', 'backgroundColor':'white', 'color':'black'
            }
        )
    ])

# ================================
# 4. Generación de Gráficos
# ================================
def crear_grafico(t, S, I, R, t_max):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=S, mode='lines', name='S: Susceptibles',
        line=dict(color=Estilos.COLOR_S, width=3),
        hovertemplate='Día: %{x:.1f}<br>S: %{y:.0f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=t, y=I, mode='lines', name='I: Infectados',
        line=dict(color=Estilos.COLOR_I, width=3),
        hovertemplate='Día: %{x:.1f}<br>I: %{y:.0f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=t, y=R, mode='lines', name='R: Recuperados',
        line=dict(color=Estilos.COLOR_R, width=3),
        hovertemplate='Día: %{x:.1f}<br>R: %{y:.0f}<extra></extra>'
    ))

    fig.update_layout(
        title={'text':'Ciclo de Vida de una Moda (Crocs) en el Campus',
               'font':{'size':20, 'color':Estilos.COLOR_TEXTO_PRINCIPAL},
               'x':0.5,'y':0.95,'xanchor':'center','yanchor':'top'},
        xaxis_title='Días',
        yaxis_title='Número de Estudiantes',
        paper_bgcolor=Estilos.COLOR_FONDO_PAPEL,
        plot_bgcolor=Estilos.COLOR_FONDO_GRAFICO,
        font=dict(family='Outfit, Arial, sans-serif', size=12, color=Estilos.COLOR_TEXTO_SECUNDARIO),
        legend=dict(orientation='v', y=0.9, x=0.99, bgcolor='rgba(255,255,255,0.8)', bordercolor='lightgray'),
        hovermode='x unified',
        xaxis=dict(showgrid=True, gridcolor=Estilos.COLOR_GRID, zeroline=True, zerolinecolor=Estilos.COLOR_ZEROLINE),
        yaxis=dict(showgrid=True, gridcolor=Estilos.COLOR_GRID, zeroline=True, zerolinecolor=Estilos.COLOR_ZEROLINE)
    )

    # Ajuste dinámico del rango en y
    y_max = max(max(S), max(I), max(R)) * 1.05
    fig.update_yaxes(range=[0, y_max])

    # Rango en x
    fig.update_xaxes(range=[0, t_max])

    return fig

# ================================
# 5. Layout de la Página
# ================================
layout = html.Div([
    html.H1("Simulación: Adopción de Moda SIR", style={'textAlign':'center', 'color':Estilos.COLOR_TEXTO_PRINCIPAL, 'marginBottom':'30px'}),

    html.Div([
        # Columna izquierda: controles
        html.Div([
            html.H3("Parámetros del Modelo", style={'color':Estilos.COLOR_TEXTO_PRINCIPAL, 'borderBottom':'2px solid lightpink', 'marginBottom':'20px'}),
            html.P("Ajuste las variables del modelo SIR para la tendencia de moda:", style={'fontSize':'14px', 'marginBottom':'20px'}),

            crear_input("Población Total (N):", "input-N", 1000, step=10),
            crear_input("Tasa de imitación (b):", "input-b", 0.0005, step=0.0001),
            crear_input("Tasa de aburrimiento (k):", "input-k", 0.1, step=0.01),
            crear_input("Usuarios Iniciales (I0):", "input-I0", 5, step=1),
            crear_input("Tiempo máximo (Días):", "input-tmax", 60, step=5),

            html.Button("Actualizar Gráfico", id='btn-actualizar', style={
                'backgroundColor':Estilos.COLOR_TEXTO_PRINCIPAL, 'color':'white', 'padding':'12px',
                'width':'100%', 'border':'none', 'borderRadius':'5px', 'cursor':'pointer',
                'marginTop':'10px', 'fontSize':'16px', 'transition':Estilos.TRANSITION
            })
        ], style={'flex':'1', 'minWidth':'300px', 'padding':'25px', 'backgroundColor':'#f9f9f9', 'borderRadius':'10px', 'boxShadow':'0 4px 6px rgba(0,0,0,0.1)'}),

        # Columna derecha: gráfica
        html.Div([
            dcc.Graph(id='grafico-sir', style={'height':'500px', 'width':'100%'})
        ], style={'flex':'2', 'minWidth':'400px', 'padding':'10px'})
    ], style={'display':'flex', 'flexWrap':'wrap', 'gap':'30px', 'maxWidth':'1200px', 'margin':'0 auto'})
], style={'padding':'20px', 'fontFamily':'Outfit, sans-serif'})

# ================================
# 6. Callbacks para la interactividad
# ================================
@callback(
    Output('grafico-sir', 'figure'),
    Input('btn-actualizar', 'n_clicks'),
    State('input-N', 'value'),
    State('input-b', 'value'),
    State('input-k', 'value'),
    State('input-I0', 'value'),
    State('input-tmax', 'value')
)
def actualizar_grafico(n_clicks, N, b, k, I0, t_max):
    # Validaciones básicas
    if N is None or N <= 0:
        N = 1000
    if b is None or b <= 0:
        b = 0.0005
    if k is None or k <= 0:
        k = 0.1
    if I0 is None or I0 <= 0:
        I0 = 5
    if t_max is None or t_max <= 0:
        t_max = 60

    # Modelo SIR
    modelo = ModeloSIR(N, b, k, I0)

    # Resolver
    t, S, I, R = modelo.resolver(t_max)

    # Crear gráfico
    fig = crear_grafico(t, S, I, R, t_max)
    return fig
