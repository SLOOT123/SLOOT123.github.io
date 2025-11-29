# Técnicas de Modelamiento Matemático - Dashboard Interactivo

Dashboard educativo interactivo construido con **Dash** y **Plotly** para simular y visualizar modelos matemáticos aplicados a fenómenos reales.

## 📋 Descripción

Este proyecto implementa un dashboard web interactivo que permite explorar y comprender:
- **Modelos de crecimiento** (Exponencial, Logístico)
- **Modelo SIR** (Susceptibles-Infectados-Recuperados)
- **Aplicaciones prácticas** del modelo SIR en diferentes contextos

## 🎯 Características

### Páginas Disponibles

1. **Inicio** - Página de bienvenida
2. **Crecimiento Exponencial** - Simulación de crecimiento exponencial
3. **Crecimiento Logístico** - Simulación con límite de capacidad
4. **Modelo SIR Clásico** - Propagación de enfermedades
5. **Modelo Propuesto** - Caso de estudio: Adopción de Crocs
6. **Propagación de Rumores** - Dinámica de rumores en poblaciones
7. **Comparación de Escenarios** - Análisis comparativo
8. **Aplicación SIR v2** - Aplicaciones integradas (Influenza, Rumores, Apps Móviles)

### Funcionalidades

✅ Simulaciones interactivas en tiempo real  
✅ Gráficos dinámicos con Plotly  
✅ Controles deslizantes y entradas numéricas  
✅ Cálculo automático de métricas epidemiológicas  
✅ Visualización de planos de fase  
✅ Interfaz responsive y moderna

## 🛠️ Tecnologías

- **Python 3.11+**
- **Dash 3.2.0** - Framework web interactivo
- **Plotly** - Visualización de gráficos
- **SciPy** - Integración numérica (odeint)
- **NumPy** - Computación numérica
- **Pandas** - Manipulación de datos
- **dash-bootstrap-components** - Componentes Bootstrap

## 📦 Instalación

### Requisitos
- Python 3.11+
- pip

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/SLOOT123/dashtv.git
cd dashtv
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
python dina.py
```

5. **Acceder a la aplicación**
```
Abre http://127.0.0.1:8050/ en tu navegador
```

## 📁 Estructura del Proyecto

```
dashtv/
├── dina.py                          # Punto de entrada principal
├── modelo.py                        # Adaptador de modelos
├── requirements.txt                 # Dependencias
├── .gitignore                      # Archivos ignorados por Git
├── pages/                          # Páginas Dash
│   ├── __init__.py
│   ├── inicio.py
│   ├── clase1.py                   # Crecimiento exponencial
│   ├── clase2.py                   # Crecimiento logístico
│   ├── clase7.py                   # Modelo SIR básico
│   ├── Modelo propuesto.py         # Caso de estudio personalizado
│   ├── modelosir_rumor.py          # Dinámica de rumores
│   ├── comparacion_escenariospy.py # Análisis comparativo
│   └── aplicacion_sir_unmsm_v2.py  # Aplicaciones integradas
├── assets/
│   ├── css/
│   │   └── images/
│   │       └── style.css
│   └── images/
└── scripts/
    ├── fetch_root.py
    ├── inspect_pages.py
    └── print_index.py
```

## 🔧 Configuración

### Modelos Implementados

#### Crecimiento Exponencial
$$\frac{dP}{dt} = rP$$

#### Crecimiento Logístico
$$\frac{dP}{dt} = rP\left(1 - \frac{P}{K}\right)$$

#### Modelo SIR
$$\frac{dS}{dt} = -\beta \frac{SI}{N}$$
$$\frac{dI}{dt} = \beta \frac{SI}{N} - \gamma I$$
$$\frac{dR}{dt} = \gamma I$$

## 🚀 Uso

1. Navega a través del menú superior
2. Selecciona un modelo matemático
3. Ajusta los parámetros con los controles deslizantes
4. Observa cómo cambian los gráficos en tiempo real
5. Analiza las métricas calculadas automáticamente

## 📊 Ejemplos de Simulaciones

### Influenza
- Simula la propagación de un virus respiratorio
- Parámetros: Población, tasa de transmisión, tasa de recuperación
- Visualiza: Curva SIR, plano de fase, pico de infectados

### Propagación de Rumores
- Modeloa cómo un rumor se propaga en una población
- Distingue entre personas que creen, propagan y racionales
- Analiza la duración total del rumor

### Adopción de App Móvil
- Simula la adopción de una aplicación móvil
- Calcula viralidad y retención
- Predice usuarios máximos y ciclo de vida

## 📝 Autor

Proyecto desarrollado para **Universidad Nacional Mayor de San Marcos (UNMSM)**  
Curso: Técnicas de Modelamiento Matemático

## 📄 Licencia

Este proyecto es de código abierto. Ver detalles en el repositorio.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para reportar problemas o sugerencias, crea un issue en el repositorio.

---

**Última actualización:** 28 de noviembre de 2025
