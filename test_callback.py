"""Test para verificar que los callbacks funcionan correctamente."""
import sys
sys.path.insert(0, 'c:\\Users\\slotzs\\Desktop\\dashtv')

from pages.aplicacion_sir_unmsm_v2 import (
    ModeloSIRClasico,
    ModeloSIR,
    GeneradorGraficos,
    CalculadoraMetricas,
    params
)

# Simular el callback de influenza
N = params.POBLACION_FLU
beta = params.TASA_TRANSMISION_FLU
gamma = params.TASA_RECUPERACION_FLU

print(f"Población: {N}, β: {beta}, γ: {gamma}")

try:
    # Condiciones iniciales
    I0, R0 = 1, 0
    S0 = N - I0 - R0
    
    print(f"S0: {S0}, I0: {I0}, R0: {R0}")
    
    # Resolución
    t, S, I, R = ModeloSIR.resolver(
        N, S0, I0, R0, 40,
        ModeloSIRClasico.ecuaciones,
        beta=beta, gamma=gamma
    )
    
    print(f"✓ Simulación completada: t={len(t)} puntos")
    print(f"  - S: {S[:5]}")
    print(f"  - I: {I[:5]}")
    print(f"  - R: {R[:5]}")
    
    # Métricas
    metricas = CalculadoraMetricas.calcular_metricas_influenza(t, I, beta, gamma)
    print(f"✓ Métricas calculadas: {list(metricas.keys())}")
    
    # Gráfico
    fig = GeneradorGraficos.crear_grafico_sir(
        t, S, I, R,
        f'Brote de Influenza en Población de {N:,} Personas',
        {'S': 'Susceptibles', 'I': 'Infectados', 'R': 'Recuperados'},
        altura=500
    )
    print(f"✓ Gráfico creado: {type(fig).__name__}")
    
    # Gráfico de fase
    fig_fase = GeneradorGraficos.crear_grafico_fase(S, I, "Plano de Fase: Influenza (S vs I)")
    print(f"✓ Gráfico de fase creado: {type(fig_fase).__name__}")
    
    print("\n✓✓✓ TODO FUNCIONA CORRECTAMENTE ✓✓✓")
    
except Exception as e:
    print(f"✗ ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
