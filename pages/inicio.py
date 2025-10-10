import dash
from dash import html

# Página principal: portada personal
dash.register_page(__name__, path='/', name='Inicio')

layout = html.Div(
    className='app-container hero',
    children=[
        html.Div(
            className='hero-card',
            children=[
                html.Div(
                    className='hero-text',
                    children=[
                        html.H1('Jhovany Calixto'),
                        html.H3('Programador Fullstack • Modelador Matemático'),
                        html.P(
                            """
                            Soy desarrollador Fullstack con experiencia en backend y frontend, y en
                            modelamiento matemático y análisis numérico. Utilizo herramientas modernas
                            como Dash, FastAPI, React y bibliotecas científicas en Python.
                            """
                        ),
                        html.P(
                            """
                            Además, integro modelos asistidos por LLMs (por ejemplo ChatGPT) para
                            acelerar y mejorar procesos de modelado: generación de código de simulación,
                            ajuste de parámetros, explicaciones y validación.
                            """
                        ),
                        html.Ul(
                            children=[
                                html.Li('Lenguajes: Python, JavaScript, TypeScript'),
                                html.Li('Frameworks: Dash, Flask, FastAPI, React'),
                                html.Li('Modelado: EDOs, simulaciones, optimización; uso de LLMs para apoyo'),
                            ]
                        ),
                        html.Div(
                            className='hero-ctas',
                            children=[
                                html.A('GitHub', href='https://github.com/', target='_blank', className='btn btn-primary'),
                                html.A('LinkedIn', href='https://www.linkedin.com/', target='_blank', className='btn'),
                                html.A('Contactar', href='mailto:tu.email@ejemplo.com', className='btn'),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className='hero-image',
                    children=[html.Img(src='/assets/images/loty.svg', alt='Mi retrato')],
                ),
            ],
        )
    ],
)
