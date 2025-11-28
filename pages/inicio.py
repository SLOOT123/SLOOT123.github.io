"""
Página de Inicio - Portada Personal
===================================

Página principal del portafolio profesional. Presenta el perfil del desarrollador,
experiencias clave y enlaces a canales de contacto y redes profesionales.

Autor: Jhovany Calixto
Versión: 2.0 (Profesional)
"""

import dash
from dash import html

dash.register_page(
    __name__,
    path='/',
    name='Inicio'
)

# ==========================================
# CONSTANTES Y CONFIGURACIÓN
# ==========================================

# Paleta de colores profesional (consistente con el resto del portafolio)
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
ESTILO_BTN_PRIMARIO = {
    'backgroundColor': COLORES['primario'],
    'color': COLORES['fondo_oscuro'],
    'padding': '12px 24px',
    'border': 'none',
    'borderRadius': '6px',
    'cursor': 'pointer',
    'fontSize': '14px',
    'fontWeight': '600',
    'transition': 'all 0.3s ease',
    'boxShadow': '0 2px 8px rgba(44, 90, 160, 0.2)',
    'textDecoration': 'none',
    'display': 'inline-block',
    'marginRight': '12px',
    'marginBottom': '12px'
}

ESTILO_BTN_SECUNDARIO = {
    **ESTILO_BTN_PRIMARIO,
    'backgroundColor': COLORES['fondo_oscuro'],
    'color': COLORES['primario'],
    'border': f"2px solid {COLORES['primario']}",
    'boxShadow': '0 2px 8px rgba(44, 90, 160, 0.1)'
}

# ==========================================
# LAYOUT DE LA PÁGINA
# ==========================================

layout = html.Div([
    # Sección Hero
    html.Div([
        html.Div([
            # Columna izquierda: Contenido
            html.Div([
                # Nombre y título
                html.Div([
                    html.H1(
                        "Jhovany Calixto",
                        style={
                            'fontSize': '48px',
                            'fontWeight': '700',
                            'color': COLORES['primario'],
                            'marginBottom': '8px',
                            'marginTop': '0px'
                        }
                    ),
                    html.H2(
                        "Desarrollador Fullstack • Modelador Matemático",
                        style={
                            'fontSize': '24px',
                            'fontWeight': '600',
                            'color': COLORES['texto_secundario'],
                            'marginBottom': '24px',
                            'marginTop': '0px'
                        }
                    )
                ], style={'marginBottom': '32px'}),

                # Descripción profesional
                html.Div([
                    html.P(
                        "Soy desarrollador Fullstack con experiencia en desarrollo backend y frontend, "
                        "especializado en modelamiento matemático y análisis numérico. Utilizo herramientas "
                        "modernas como Dash, FastAPI, React y bibliotecas científicas de Python para crear "
                        "soluciones escalables e innovadoras.",
                        style={
                            'fontSize': '16px',
                            'lineHeight': '1.7',
                            'color': COLORES['texto_primario'],
                            'marginBottom': '16px'
                        }
                    ),
                    html.P(
                        "Integro modelos asistidos por LLMs (ChatGPT, Claude) para acelerar y mejorar procesos "
                        "de modelado: generación de código de simulación, ajuste de parámetros, explicaciones "
                        "técnicas profundas y validación de resultados. Esto permite crear soluciones complejas "
                        "de forma más eficiente.",
                        style={
                            'fontSize': '16px',
                            'lineHeight': '1.7',
                            'color': COLORES['texto_primario'],
                            'marginBottom': '24px'
                        }
                    )
                ]),

                # Competencias técnicas
                html.Div([
                    html.H3(
                        "Competencias Técnicas",
                        style={
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'color': COLORES['primario'],
                            'marginBottom': '16px',
                            'marginTop': '0px'
                        }
                    ),
                    html.Div([
                        # Grid de competencias
                        html.Div([
                            html.Div([
                                html.Span("🐍", style={'fontSize': '24px', 'marginRight': '8px'}),
                                html.Div([
                                    html.P("Lenguajes", style={'margin': '0px', 'fontWeight': '600', 'fontSize': '14px'}),
                                    html.P("Python, JavaScript, TypeScript", style={'margin': '4px 0px 0px', 'fontSize': '13px', 'color': COLORES['texto_secundario']})
                                ])
                            ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '16px'}),

                            html.Div([
                                html.Span("⚙️", style={'fontSize': '24px', 'marginRight': '8px'}),
                                html.Div([
                                    html.P("Frameworks", style={'margin': '0px', 'fontWeight': '600', 'fontSize': '14px'}),
                                    html.P("Dash, Flask, FastAPI, React", style={'margin': '4px 0px 0px', 'fontSize': '13px', 'color': COLORES['texto_secundario']})
                                ])
                            ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '16px'}),

                            html.Div([
                                html.Span("📊", style={'fontSize': '24px', 'marginRight': '8px'}),
                                html.Div([
                                    html.P("Modelado", style={'margin': '0px', 'fontWeight': '600', 'fontSize': '14px'}),
                                    html.P("EDOs, Simulaciones, Optimización, LLMs", style={'margin': '4px 0px 0px', 'fontSize': '13px', 'color': COLORES['texto_secundario']})
                                ])
                            ], style={'display': 'flex', 'alignItems': 'flex-start', 'marginBottom': '0px'}),
                        ], style={'backgroundColor': f"rgba(44, 90, 160, 0.05)", 'padding': '20px', 'borderRadius': '8px', 'borderLeft': f"4px solid {COLORES['primario']}"})
                    ])
                ], style={'marginBottom': '32px'}),

                # Llamadas a la acción
                html.Div([
                    html.H3(
                        "Conéctate Conmigo",
                        style={
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'color': COLORES['primario'],
                            'marginBottom': '16px',
                            'marginTop': '0px'
                        }
                    ),
                    html.Div([
                        html.A(
                            "GitHub",
                            href="https://github.com/",
                            target="_blank",
                            rel="noopener noreferrer",
                            style={
                                **ESTILO_BTN_PRIMARIO,
                                'marginRight': '12px'
                            }
                        ),
                        html.A(
                            "LinkedIn",
                            href="https://www.linkedin.com/",
                            target="_blank",
                            rel="noopener noreferrer",
                            style=ESTILO_BTN_SECUNDARIO
                        ),
                        html.A(
                            "Enviar Email",
                            href="mailto:tu.email@ejemplo.com",
                            style={
                                **ESTILO_BTN_PRIMARIO,
                                'marginRight': '0px'
                            }
                        )
                    ], style={'display': 'flex', 'flexWrap': 'wrap', 'alignItems': 'center'})
                ])

            ], style={
                'flex': '1',
                'minWidth': '300px',
                'paddingRight': '40px'
            }),

            # Columna derecha: Imagen/Ilustración
            html.Div([
                html.Div([
                    html.Img(
                        src='/assets/images/loty.svg',
                        alt='Ilustración personal',
                        style={
                            'width': '100%',
                            'maxWidth': '400px',
                            'height': 'auto'
                        }
                    )
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center'
                })
            ], style={
                'flex': '1',
                'minWidth': '300px',
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center'
            })

        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'gap': '40px',
            'alignItems': 'center',
            'justifyContent': 'space-between'
        })
    ], style={
        'padding': '60px 40px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    }),

    # Sección de estadísticas/destacados
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3(
                        "3+",
                        style={
                            'fontSize': '36px',
                            'fontWeight': '700',
                            'color': COLORES['primario'],
                            'margin': '0px',
                            'marginBottom': '8px'
                        }
                    ),
                    html.P(
                        "Años de Experiencia",
                        style={
                            'fontSize': '14px',
                            'color': COLORES['texto_secundario'],
                            'margin': '0px'
                        }
                    )
                ], style={'textAlign': 'center'})
            ], style={
                'padding': '24px',
                'backgroundColor': f"rgba(44, 90, 160, 0.08)",
                'borderRadius': '8px',
                'border': f"1px solid {COLORES['borde']}"
            }),

            html.Div([
                html.Div([
                    html.H3(
                        "10+",
                        style={
                            'fontSize': '36px',
                            'fontWeight': '700',
                            'color': COLORES['primario'],
                            'margin': '0px',
                            'marginBottom': '8px'
                        }
                    ),
                    html.P(
                        "Proyectos Completados",
                        style={
                            'fontSize': '14px',
                            'color': COLORES['texto_secundario'],
                            'margin': '0px'
                        }
                    )
                ], style={'textAlign': 'center'})
            ], style={
                'padding': '24px',
                'backgroundColor': f"rgba(39, 174, 96, 0.08)",
                'borderRadius': '8px',
                'border': f"1px solid {COLORES['borde']}"
            }),

            html.Div([
                html.Div([
                    html.H3(
                        "100%",
                        style={
                            'fontSize': '36px',
                            'fontWeight': '700',
                            'color': COLORES['primario'],
                            'margin': '0px',
                            'marginBottom': '8px'
                        }
                    ),
                    html.P(
                        "Comprometido",
                        style={
                            'fontSize': '14px',
                            'color': COLORES['texto_secundario'],
                            'margin': '0px'
                        }
                    )
                ], style={'textAlign': 'center'})
            ], style={
                'padding': '24px',
                'backgroundColor': f"rgba(243, 156, 18, 0.08)",
                'borderRadius': '8px',
                'border': f"1px solid {COLORES['borde']}"
            })

        ], style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
            'gap': '24px',
            'maxWidth': '1200px',
            'margin': '0 auto'
        })
    ], style={
        'padding': '60px 40px',
        'backgroundColor': COLORES['fondo_claro'],
        'borderTop': f"1px solid {COLORES['borde']}",
        'borderBottom': f"1px solid {COLORES['borde']}"
    }),

    # Sección de herramientas/stack
    html.Div([
        html.Div([
            html.H2(
                "Stack Tecnológico",
                style={
                    'fontSize': '32px',
                    'fontWeight': '700',
                    'color': COLORES['primario'],
                    'marginBottom': '32px',
                    'textAlign': 'center'
                }
            ),

            html.Div([
                # Backend
                html.Div([
                    html.H3(
                        "Backend",
                        style={
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'color': COLORES['primario'],
                            'marginBottom': '16px'
                        }
                    ),
                    html.Ul([
                        html.Li("Python (NumPy, SciPy, Pandas)"),
                        html.Li("FastAPI & Flask"),
                        html.Li("PostgreSQL & MongoDB"),
                        html.Li("Docker & Kubernetes")
                    ], style={'paddingLeft': '20px', 'color': COLORES['texto_primario']})
                ], style={'flex': '1', 'minWidth': '250px'}),

                # Frontend
                html.Div([
                    html.H3(
                        "Frontend",
                        style={
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'color': COLORES['primario'],
                            'marginBottom': '16px'
                        }
                    ),
                    html.Ul([
                        html.Li("React & TypeScript"),
                        html.Li("Dash (Plotly)"),
                        html.Li("HTML5 & CSS3"),
                        html.Li("Responsive Design")
                    ], style={'paddingLeft': '20px', 'color': COLORES['texto_primario']})
                ], style={'flex': '1', 'minWidth': '250px'}),

                # Modelado
                html.Div([
                    html.H3(
                        "Modelado & IA",
                        style={
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'color': COLORES['primario'],
                            'marginBottom': '16px'
                        }
                    ),
                    html.Ul([
                        html.Li("Ecuaciones Diferenciales"),
                        html.Li("Simulaciones Numéricas"),
                        html.Li("Integración con LLMs"),
                        html.Li("Análisis Estadístico")
                    ], style={'paddingLeft': '20px', 'color': COLORES['texto_primario']})
                ], style={'flex': '1', 'minWidth': '250px'})

            ], style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'gap': '40px',
                'justifyContent': 'space-around'
            })
        ], style={
            'maxWidth': '1000px',
            'margin': '0 auto',
            'padding': '60px 40px'
        })
    ], style={
        'backgroundColor': COLORES['fondo_oscuro'],
        'borderBottom': f"1px solid {COLORES['borde']}"
    }),

    # Sección CTA final
    html.Div([
        html.Div([
            html.H2(
                "¿Listo para Colaborar?",
                style={
                    'fontSize': '32px',
                    'fontWeight': '700',
                    'color': COLORES['primario'],
                    'marginBottom': '16px',
                    'textAlign': 'center'
                }
            ),
            html.P(
                "Tengo experiencia en proyectos complejos de modelado matemático, "
                "desarrollo de aplicaciones web y análisis de datos. "
                "Hagamos realidad tu próximo proyecto.",
                style={
                    'fontSize': '16px',
                    'color': COLORES['texto_secundario'],
                    'textAlign': 'center',
                    'marginBottom': '32px',
                    'maxWidth': '600px',
                    'margin': '0 auto 32px'
                }
            ),
            html.Div([
                html.A(
                    "Iniciar Proyecto",
                    href="mailto:tu.email@ejemplo.com",
                    style={
                        **ESTILO_BTN_PRIMARIO,
                        'padding': '14px 32px',
                        'fontSize': '16px'
                    }
                ),
                html.A(
                    "Ver Portafolio",
                    href="/portafolio",
                    style={
                        **ESTILO_BTN_SECUNDARIO,
                        'padding': '14px 32px',
                        'fontSize': '16px'
                    }
                )
            ], style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'})
        ], style={
            'maxWidth': '800px',
            'margin': '0 auto',
            'padding': '60px 40px',
            'textAlign': 'center'
        })
    ], style={
        'backgroundColor': f"rgba(44, 90, 160, 0.05)",
        'borderTop': f"1px solid {COLORES['borde']}"
    })

], style={
    'padding': '0px',
    'backgroundColor': COLORES['fondo_oscuro'],
    'fontFamily': 'Segoe UI, Arial, sans-serif',
    'minHeight': '100vh'
})