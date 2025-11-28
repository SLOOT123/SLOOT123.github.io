import dash
from dash import dcc, html
import logging

# Configurar logging para ver errores
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = dash.Dash(__name__, use_pages=True)
logger.info(f"Pages registered: {list(dash.page_registry.keys())}")

app.layout = html.Div([
	html.H1("Técnicas de Modelamiento Matemático", className='app-header'),
	html.Div([
		html.Div([
			html.Div([
				dcc.Link(f"{page['name']}", href=page["relative_path"] , className='nav-link')
				for page in dash.page_registry.values()
			], className='nav-links')
		], className='navigation'),
		dash.page_container
	], className='app-container')
])


if __name__ == '__main__':
	app.run(debug=True)