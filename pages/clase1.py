import dash
from dash import html, dcc
import numpy as np
import plotly.graph_objs as go

# Registrar la página como sección 'Clase1'
dash.register_page(__name__, path='/clase1', name='Clase1')

# Figura de ejemplo (crecimiento exponencial)
t = np.arange(0, 101, 10)
P0 = 100
r = 0.03
P = P0 * np.exp(r * t)

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=P, mode='lines+markers', line=dict(dash='dash', color='#0B84A5'),
                         marker=dict(symbol='square', size=8, color='#0B84A5')))
fig.update_layout(title='Crecimiento de la población', xaxis_title='Tiempo (t)',
                  yaxis_title='Población (P)', margin=dict(l=40, r=20, t=40, b=40),
                  plot_bgcolor='#e7f3f5')

# Layout de la página
layout = html.Div(className='app-container', children=[
    html.Div(className='content card', children=[
        html.H2("Crecimiento de la población y capacidad de carga", className='title'),
        dcc.Markdown(
            """
Para modelar el crecimiento de la población mediante una ecuación diferencial, primero
tenemos que introducir algunas variables y términos relevantes. La variable $P(t)$
representará la población en función del tiempo. Las unidades de tiempo pueden ser horas, días, semanas,
meses o incluso años. Cualquier problema dado debe especificar las unidades utilizadas
en ese problema en particular. La variable $P$ representará a la población. Como la
población varía con el tiempo, se entiende que es una función del tiempo. Por lo tanto,
utilizamos la notación $P(t)$ para la población en función del tiempo. Si $P(t)$ es
una función diferenciable, entonces la primera derivada $\frac{dP}{dt}$
representa la tasa instantánea de cambio de la población en función del tiempo.

Un ejemplo de función de crecimiento exponencial es $P(t)=P_0 e^{rt}$.
En esta función, $P(t)$ representa la población en el momento $t$, $P_0$ es
la población inicial (población en el tiempo $t=0$), y la constante $r>0$
se denomina tasa de crecimiento. Por ejemplo, podemos tomar $P_0=100$ y $r=0.03$.
            """,
            mathjax=True
        )
    ]),

    html.Div(className='graph-container', children=[
        html.Div(className='graph-card', children=[
            html.H2("Gráfica", className='title'),
            dcc.Graph(figure=fig, id='population-graph')
        ])
    ])
])
