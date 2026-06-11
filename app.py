import streamlit as st
import random # Asegúrate de que esta línea esté hasta arriba en tu app.py con los otros imports
import math # Asegúrate de que esté hasta arriba
import heapq # Para la cola de prioridad en A* 
import time # Para simular tiempos de espera en la visualización

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# (Debe ser el primer comando de Streamlit)
# ==========================================
st.set_page_config(page_title="IA Visualizer | ESCOM", page_icon="🧠", layout="wide")

# ==========================================
# MÓDULOS DE LA INTERFAZ (Vistas vacías)
# ==========================================
def obtener_vecinos_laberinto(estado, mapa):
    """Obtiene las coordenadas válidas a las que se puede mover (dinámico al tamaño del mapa)."""
    f, c = estado
    vecinos = []
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    random.shuffle(movimientos)
    
    filas = len(mapa)
    columnas = len(mapa[0])
    
    for df, dc in movimientos:
        nf, nc = f + df, c + dc
        if 0 <= nf < filas and 0 <= nc < columnas:
            if mapa[nf][nc] != 'H':
                vecinos.append((nf, nc))
    return vecinos

def buscar_ruta_laberinto(mapa, inicio, meta, algoritmo):
    """Ejecuta BFS o DFS y devuelve la ruta encontrada y los nodos visitados."""
    estructura_datos = [(inicio, [inicio])] 
    visitados = set([inicio])
    nodos_expandidos = []

    while estructura_datos:
        if algoritmo == "BFS":
            actual, ruta = estructura_datos.pop(0) # Cola
        else:
            actual, ruta = estructura_datos.pop(-1) # Pila

        nodos_expandidos.append(actual)

        if actual == meta:
            return nodos_expandidos, ruta

        for vecino in obtener_vecinos_laberinto(actual, mapa):
            if vecino not in visitados:
                visitados.add(vecino)
                estructura_datos.append((vecino, ruta + [vecino]))

    return nodos_expandidos, []

def mostrar_frozen_lake():
    st.header("🧊 Laberinto Frozen Lake")
    st.subheader("Búsqueda No Informada")
    algoritmo = st.radio("Selecciona el algoritmo:", ("BFS", "DFS"), horizontal=True)
    
    # 1. Nuevo mapa 6x6 con trampas y un callejón sin salida profundo a la derecha
    mapa = [
        ['S', 'F', 'H', 'F', 'F', 'F'],
        ['F', 'F', 'H', 'F', 'H', 'F'],
        ['H', 'F', 'F', 'F', 'H', 'F'],
        ['F', 'H', 'H', 'H', 'H', 'F'],
        ['F', 'F', 'F', 'F', 'F', 'F'],
        ['H', 'H', 'F', 'H', 'H', 'G']
    ]
    
    iconos = {'S': '🧍‍♂️', 'F': '🧊', 'H': '🕳️', 'G': '🏆'}
    filas = len(mapa)
    columnas = len(mapa[0])
    
    # Buscamos dónde están S y G automáticamente
    inicio = None
    meta = None
    for f in range(filas):
        for c in range(columnas):
            if mapa[f][c] == 'S': inicio = (f, c)
            elif mapa[f][c] == 'G': meta = (f, c)

    st.write("### Mapa del entorno")
    
    # Generamos los pesos de las columnas dinámicamente: ej. [1, 1, 1, 1, 1, 1, 4]
    pesos_cols = [1] * columnas + [4]
    
    for fila in mapa:
        cols = st.columns(pesos_cols) 
        for j, celda in enumerate(fila):
            with cols[j]:
                st.button(iconos[celda], key=f"celda_{id(fila)}_{j}", use_container_width=True, disabled=True)
                
    st.markdown("---")
    
    if st.button("▶️ Ejecutar Búsqueda y Animar", key="btn_animar_frozen", type="primary"):
        expandidos, ruta = buscar_ruta_laberinto(mapa, inicio, meta, algoritmo)
        
        if ruta:
            st.success(f"¡Ruta encontrada usando {algoritmo}! Reproduciendo...")
            st.write(f"**Nodos explorados:** {len(expandidos)} (Nota cómo DFS se atora en los callejones)")
            
            contenedor_animacion = st.empty()
            
            for i, paso_actual in enumerate(ruta):
                with contenedor_animacion.container():
                    st.write(f"**Paso actual:** {i} / {len(ruta)-1}")
                    
                    for f in range(filas):
                        cols = st.columns(pesos_cols)
                        for c in range(columnas):
                            celda = mapa[f][c]
                            
                            if (f, c) == paso_actual:
                                icono_mostrar = '🧍‍♂️'
                            elif (f, c) in ruta[:i]:
                                icono_mostrar = '🐾'
                            else:
                                icono_mostrar = iconos[celda]
                                
                            with cols[c]:
                                st.button(icono_mostrar, key=f"anim_fl_{f}_{c}_{i}", use_container_width=True, disabled=True)
                time.sleep(0.5)
            
            st.balloons()
        else:
            st.error("No se encontró ninguna ruta a la meta.")

def mostrar_frozen_lake():
    st.header("🧊 Laberinto Frozen Lake")
    st.subheader("Búsqueda No Informada")
    algoritmo = st.radio("Selecciona el algoritmo:", ("BFS", "DFS"), horizontal=True)
    
    # 1. Nuevo mapa 6x6 con trampas y un callejón sin salida profundo a la derecha
    mapa = [
        ['S', 'F', 'H', 'F', 'F', 'F'],
        ['F', 'F', 'H', 'F', 'H', 'F'],
        ['H', 'F', 'F', 'F', 'H', 'F'],
        ['F', 'H', 'F', 'H', 'H', 'F'],
        ['F', 'F', 'F', 'F', 'F', 'F'],
        ['F', 'H', 'F', 'H', 'H', 'G']
    ]
    
    iconos = {'S': '🧍‍♂️', 'F': '🧊', 'H': '🕳️', 'G': '🏆'}
    filas = len(mapa)
    columnas = len(mapa[0])
    
    # Buscamos dónde están S y G automáticamente
    inicio = None
    meta = None
    for f in range(filas):
        for c in range(columnas):
            if mapa[f][c] == 'S': inicio = (f, c)
            elif mapa[f][c] == 'G': meta = (f, c)

    st.write("### Mapa del entorno")
    
    # Generamos los pesos de las columnas dinámicamente: ej. [1, 1, 1, 1, 1, 1, 4]
    pesos_cols = [1] * columnas + [4]
    
    for fila in mapa:
        cols = st.columns(pesos_cols) 
        for j, celda in enumerate(fila):
            with cols[j]:
                st.button(iconos[celda], key=f"celda_{id(fila)}_{j}", use_container_width=True, disabled=True)
                
    st.markdown("---")
    
    if st.button("▶️ Ejecutar Búsqueda y Animar", key="btn_animar_frozen", type="primary"):
        expandidos, ruta = buscar_ruta_laberinto(mapa, inicio, meta, algoritmo)
        
        if ruta:
            st.success(f"¡Ruta encontrada usando {algoritmo}! Reproduciendo...")
            st.write(f"**Nodos explorados:** {len(expandidos)} (Nota cómo DFS se atora en los callejones)")
            
            contenedor_animacion = st.empty()
            
            for i, paso_actual in enumerate(ruta):
                with contenedor_animacion.container():
                    st.write(f"**Paso actual:** {i} / {len(ruta)-1}")
                    
                    for f in range(filas):
                        cols = st.columns(pesos_cols)
                        for c in range(columnas):
                            celda = mapa[f][c]
                            
                            if (f, c) == paso_actual:
                                icono_mostrar = '🧍‍♂️'
                            elif (f, c) in ruta[:i]:
                                icono_mostrar = '🐾'
                            else:
                                icono_mostrar = iconos[celda]
                                
                            with cols[c]:
                                st.button(icono_mostrar, key=f"anim_fl_{f}_{c}_{i}", use_container_width=True, disabled=True)
                time.sleep(0.5)
            
            st.balloons()
        else:
            st.error("No se encontró ninguna ruta a la meta.")
# ========================================== Parte de Sokoban (con mapa visual) ==========================================
def obtener_distancia_manhattan(cajas, metas):
    """
    Función Heurística h(n): Suma de las distancias en cruz
    desde cada caja hasta su meta más cercana.
    """
    distancia_total = 0
    for box in cajas:
        distancia_total += min(abs(box[0] - t[0]) + abs(box[1] - t[1]) for t in metas)
    return distancia_total

def resolver_sokoban_astar(mapa_inicial):
    """Algoritmo A* que evalúa f(n) = g(n) + h(n). Dinámico para cualquier tamaño de mapa."""
    paredes = set()
    metas = set()
    inicio_jugador = None
    inicio_cajas = set()

    filas = len(mapa_inicial)
    columnas = len(mapa_inicial[0])

    for f in range(filas):
        for c in range(columnas):
            celda = mapa_inicial[f][c]
            if celda == 'W': paredes.add((f, c))
            elif celda == 'T': metas.add((f, c))
            elif celda == 'B': inicio_cajas.add((f, c))
            elif celda == 'P': inicio_jugador = (f, c)

    inicio_cajas = tuple(sorted(inicio_cajas))
    
    h_inicial = obtener_distancia_manhattan(inicio_cajas, metas)
    open_set = [(h_inicial, 0, inicio_jugador, inicio_cajas, [(inicio_jugador, inicio_cajas)])]
    visitados = set([(inicio_jugador, inicio_cajas)])
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_set:
        _, g, jugador, cajas, ruta = heapq.heappop(open_set)

        if set(cajas) == metas:
            return ruta

        f_j, c_j = jugador
        for df, dc in movimientos:
            n_j = (f_j + df, c_j + dc)

            if n_j in paredes: continue

            if n_j in cajas:
                n_caja = (n_j[0] + df, n_j[1] + dc)
                if n_caja in paredes or n_caja in cajas: continue
                nuevas_cajas = tuple(sorted([n_caja if c == n_j else c for c in cajas]))
            else:
                nuevas_cajas = cajas

            nuevo_estado = (n_j, nuevas_cajas)

            if nuevo_estado not in visitados:
                visitados.add(nuevo_estado)
                g_nuevo = g + 1
                h_nuevo = obtener_distancia_manhattan(nuevas_cajas, metas)
                f_nuevo = g_nuevo + h_nuevo
                heapq.heappush(open_set, (f_nuevo, g_nuevo, n_j, nuevas_cajas, ruta + [nuevo_estado]))

    return []

def mostrar_sokoban():
    st.header("📦 Sokoban")
    st.subheader("Búsqueda Informada (A*)")
    
    # Pool de niveles
    mapas_pool = [
        # Nivel 1 (1 Caja)
        [['W', 'W', 'W', 'W', 'W'], ['W', 'E', 'T', 'E', 'W'], ['W', 'E', 'B', 'E', 'W'], ['W', 'E', 'P', 'E', 'W'], ['W', 'W', 'W', 'W', 'W']],
        # Nivel 2 (1 Caja)
        [['W', 'W', 'W', 'W', 'W'], ['W', 'T', 'E', 'E', 'W'], ['W', 'E', 'B', 'E', 'W'], ['W', 'E', 'E', 'P', 'W'], ['W', 'W', 'W', 'W', 'W']],
        # Nivel 3 (1 Caja)
        [['W', 'W', 'W', 'W', 'W'], ['W', 'E', 'E', 'T', 'W'], ['W', 'E', 'B', 'E', 'W'], ['W', 'P', 'E', 'E', 'W'], ['W', 'W', 'W', 'W', 'W']],
        # Nivel 4 (2 Cajas)
        [['W', 'W', 'W', 'W', 'W'], ['W', 'T', 'E', 'T', 'W'], ['W', 'E', 'B', 'B', 'W'], ['W', 'E', 'E', 'P', 'W'], ['W', 'W', 'W', 'W', 'W']],
        # ¡NUEVO! Nivel 5 (Nivel Difícil 6x6)
        # Nivel 5 (El Reto Final: 7x8, 2 Cajas, 2 Metas, Recorrido muy largo)
        [
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
            ['W', 'T', 'E', 'E', 'E', 'E', 'T', 'W'],
            ['W', 'E', 'W', 'W', 'W', 'W', 'E', 'W'],
            ['W', 'E', 'B', 'E', 'B', 'E', 'E', 'W'],
            ['W', 'E', 'W', 'P', 'W', 'W', 'E', 'W'],
            ['W', 'E', 'E', 'E', 'E', 'E', 'E', 'W'],
            ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']
        ]
    ]
    
    if 'index_mapa_soko' not in st.session_state: st.session_state.index_mapa_soko = 0
    if 'ruta_soko' not in st.session_state: st.session_state.ruta_soko = None
    if 'paso_actual_soko' not in st.session_state: st.session_state.paso_actual_soko = 0

    mapa_base = mapas_pool[st.session_state.index_mapa_soko]
    filas = len(mapa_base)
    columnas = len(mapa_base[0])

    paredes = set()
    metas = set()
    for f in range(filas):
        for c in range(columnas):
            if mapa_base[f][c] == 'W': paredes.add((f, c))
            if mapa_base[f][c] == 'T': metas.add((f, c))

    if st.session_state.ruta_soko and st.session_state.paso_actual_soko < len(st.session_state.ruta_soko):
        jugador_actual, cajas_actuales = st.session_state.ruta_soko[st.session_state.paso_actual_soko]
    else:
        jugador_actual = None
        cajas_actuales = set()
        for f in range(filas):
            for c in range(columnas):
                if mapa_base[f][c] == 'P': jugador_actual = (f, c)
                elif mapa_base[f][c] == 'B': cajas_actuales.add((f, c))
        cajas_actuales = tuple(cajas_actuales)

    iconos_soko = {'W': '🧱', 'E': '⬛', 'P': '🧍', 'B': '📦', 'T': '🎯', 'BT': '✅'}

    st.write(f"### Configuración del Tablero (Nivel {st.session_state.index_mapa_soko + 1})")
    
    # Renderizado dinámico adaptativo
    pesos_cols = [1] * columnas + [3]
    for f in range(filas):
        cols = st.columns(pesos_cols)
        for c in range(columnas):
            coord = (f, c)
            if coord in paredes: icono = iconos_soko['W']
            elif coord == jugador_actual: icono = iconos_soko['P']
            elif coord in cajas_actuales and coord in metas: icono = iconos_soko['BT']
            elif coord in cajas_actuales: icono = iconos_soko['B']
            elif coord in metas: icono = iconos_soko['T']
            else: icono = iconos_soko['E']
                
            with cols[c]:
                st.button(icono, key=f"soko_cell_{f}_{c}_{st.session_state.paso_actual_soko}", use_container_width=True, disabled=True)

    st.markdown("---")
    
    # Barra de botones de interacción
    cols_control = st.columns([1, 1, 1])
    
    with cols_control[0]:
        if st.button("🔀 Nivel Aleatorio", key="btn_soko_random"):
            # Selecciona un mapa diferente al actual
            opciones = [i for i in range(len(mapas_pool)) if i != st.session_state.index_mapa_soko]
            st.session_state.index_mapa_soko = random.choice(opciones)
            st.session_state.ruta_soko = None
            st.session_state.paso_actual_soko = 0
            st.rerun()
            
    with cols_control[1]:
        if st.button("🧠 Calcular Ruta (A*)", key="btn_soko_calcular"):
            st.session_state.ruta_soko = resolver_sokoban_astar(mapa_base)
            st.session_state.paso_actual_soko = 0
            if st.session_state.ruta_soko:
                st.success("¡Estrategia óptima calculada!")
            else:
                st.error("Este mapa no tiene solución.")
            st.rerun()

    with cols_control[2]:
        if st.session_state.ruta_soko:
            total_pasos = len(st.session_state.ruta_soko) - 1
            
            if st.session_state.paso_actual_soko < total_pasos:
                if st.button(f"➡️ Siguiente Paso ({st.session_state.paso_actual_soko}/{total_pasos})", key="btn_soko_step"):
                    st.session_state.paso_actual_soko += 1
                    st.rerun()
            else:
                st.success("🎉 ¡Objetivo alcanzado!")
                if st.button("🔄 Reiniciar Nivel", key="btn_soko_reset"):
                    st.session_state.ruta_soko = None
                    st.session_state.paso_actual_soko = 0
                    st.rerun()
# ========================================== Parte de las Reinas (con tablero visual) ==========================================
def calcular_ataques(estado):
    """
    Calcula cuántos pares de reinas se están atacando.
    Un estado perfecto devolverá 0.
    """
    ataques = 0
    # Comparamos todos los pares posibles de reinas (i, j)
    for i in range(8):
        for j in range(i + 1, 8):
            # 1. Checar si están en la misma fila
            if estado[i] == estado[j]:
                ataques += 1
            # 2. Checar si están en la misma diagonal
            # (diferencia de columnas == diferencia de filas)
            elif abs(i - j) == abs(estado[i] - estado[j]):
                ataques += 1
    return ataques

def ejecutar_paso_hill_climbing(estado):
    """
    Evalúa todos los vecinos posibles (mover una reina en su columna)
    y selecciona el que tenga el menor número de ataques.
    """
    mejor_estado = list(estado)
    mejor_ataque = calcular_ataques(estado)
    hubo_mejora = False

    # Exploramos los 56 vecinos posibles (8 columnas * 7 movimientos por columna)
    for col in range(8):
        for fila in range(8):
            if fila != estado[col]:
                # Creamos el estado vecino
                vecino = list(estado)
                vecino[col] = fila
                ataques_vecino = calcular_ataques(vecino)

                # Criterio estricto: solo aceptamos si es estrictamente menor
                if ataques_vecino < mejor_ataque:
                    mejor_ataque = ataques_vecino
                    mejor_estado = list(vecino)
                    hubo_mejora = True

    return mejor_estado, hubo_mejora

def ejecutar_paso_recocido_simulado(estado, temperatura):
    """
    Toma un vecino al azar. Si es mejor, lo acepta.
    Si es peor, lo acepta con una probabilidad P = e^(-ΔE / T).
    """
    ataque_actual = calcular_ataques(estado)

    # 1. Elegimos un solo vecino completamente al azar
    col_random = random.randint(0, 7)
    fila_random = random.randint(0, 7)
    
    # Validamos que de verdad sea un movimiento nuevo
    while fila_random == estado[col_random]:
        fila_random = random.randint(0, 7)

    vecino = list(estado)
    vecino[col_random] = fila_random
    ataque_vecino = calcular_ataques(vecino)

    # 2. Calculamos Delta E (Ataques nuevos - Ataques actuales)
    delta_e = ataque_vecino - ataque_actual
    aceptado = False

    # 3. Criterio de aceptación
    if delta_e < 0:
        aceptado = True # Mejora: se acepta automáticamente
    else:
        # Empeora: calculamos la probabilidad
        if temperatura > 0.01: # Evitar división por cero
            probabilidad = math.exp(-delta_e / temperatura)
            if random.random() < probabilidad:
                aceptado = True

    # 4. Enfriamiento (reducimos la temperatura un 5% por paso)
    nueva_temperatura = temperatura * 0.95

    estado_final = vecino if aceptado else estado
    return estado_final, aceptado, nueva_temperatura

def mostrar_reinas():
    st.header("8 Reinas")
    st.subheader("Búsqueda Local")
    algoritmo = st.radio("Selecciona el algoritmo:", ("Hill Climbing", "Recocido Simulado"), horizontal=True)
    # ... (debajo de tu st.radio de algoritmos) ...
    
    # Agregamos la Temperatura a la memoria
    if 'estado_reinas' not in st.session_state:
        st.session_state.estado_reinas = [0, 1, 2, 3, 4, 5, 6, 7]
    if 'temperatura' not in st.session_state:
        st.session_state.temperatura = 10.0 # Temperatura inicial
        
    ataques = calcular_ataques(st.session_state.estado_reinas)
    color_texto = "green" if ataques == 0 else "red"
    
    # Mostramos la temperatura en pantalla si está en Recocido Simulado
    if algoritmo == "Recocido Simulado":
        st.markdown(f"### Tablero Actual | <span style='color:{color_texto}'>Ataques: {ataques}</span> | 🌡️ Temp: {st.session_state.temperatura:.2f}", unsafe_allow_html=True)
    else:
        st.markdown(f"### Tablero Actual | <span style='color:{color_texto}'>Ataques: {ataques}</span>", unsafe_allow_html=True)

    # ... (El renderizado del tablero de HTML se queda exactamente igual) ...

    # --- ACTUALIZAR LOS CONTROLES ---
    st.markdown("---")
    cols = st.columns([1, 1, 2])
    
    with cols[0]:
        if st.button("🔀 Posición Aleatoria"):
            st.session_state.estado_reinas = [random.randint(0, 7) for _ in range(8)]
            st.session_state.temperatura = 10.0 # Reiniciamos la temperatura
            st.rerun()
            
    with cols[1]:
        if st.button("▶️ Ejecutar Paso"):
            if calcular_ataques(st.session_state.estado_reinas) == 0:
                st.success("¡Máximo Global alcanzado! 0 ataques.")
            else:
                if algoritmo == "Hill Climbing":
                    nuevo_estado, mejoro = ejecutar_paso_hill_climbing(st.session_state.estado_reinas)
                    if mejoro:
                        st.session_state.estado_reinas = nuevo_estado
                        st.rerun()
                    else:
                        st.error("❌ Atascado en un Óptimo Local.")
                
                elif algoritmo == "Recocido Simulado":
                    nuevo_estado, aceptado, nueva_temp = ejecutar_paso_recocido_simulado(
                        st.session_state.estado_reinas, 
                        st.session_state.temperatura
                    )
                    st.session_state.temperatura = nueva_temp
                    
                    if aceptado:
                        st.session_state.estado_reinas = nuevo_estado
                        st.rerun()
                    else:
                        st.warning(f"Movimiento peor rechazado. Temperatura bajando a {nueva_temp:.2f}")
    # Calculamos los ataques ANTES de dibujar el tablero
    if 'estado_reinas' not in st.session_state:
        st.session_state.estado_reinas = [0, 1, 2, 3, 4, 5, 6, 7]
        
    ataques = calcular_ataques(st.session_state.estado_reinas)
    
    # Mostramos el puntaje con un color dependiendo de qué tan mal está
    color_texto = "green" if ataques == 0 else "red"
    st.markdown(f"### Tablero Actual | <span style='color:{color_texto}'>Ataques: {ataques}</span>", unsafe_allow_html=True)
    st.write("### Tablero Actual")
    
    # 1. Estado inicial en la memoria
    # El índice es la columna (0-7), el valor es la fila (0-7)
    if 'estado_reinas' not in st.session_state:
        st.session_state.estado_reinas = [0, 1, 2, 3, 4, 5, 6, 7] # Empieza en diagonal
        
    # 2. Construcción visual del tablero con HTML/CSS
    # Usamos CSS grid para armar un cuadro de 8x8 perfecto
    tablero_html = "<div style='display: grid; grid-template-columns: repeat(8, 50px); width: 400px; border: 3px solid black; box-shadow: 5px 5px 15px rgba(0,0,0,0.3);'>"
    
    for fila in range(8):
        for col in range(8):
            # Pintar las casillas alternadas (estilo ajedrez de madera)
            es_blanca = (fila + col) % 2 == 0
            color_fondo = "#FFCE9E" if es_blanca else "#D18B47"
            
            # Verificar si en esta coordenada (columna, fila) hay una reina
            hay_reina = st.session_state.estado_reinas[col] == fila
            icono = "👑" if hay_reina else "&nbsp;"
            
            # Armar la casilla
            tablero_html += f"<div style='width: 50px; height: 50px; background-color: {color_fondo}; display: flex; justify-content: center; align-items: center; font-size: 32px;'>{icono}</div>"
            
    tablero_html += "</div><br>"
    
    # Renderizar el HTML en Streamlit
    st.markdown(tablero_html, unsafe_allow_html=True)
    
    # 3. Controles interactivos
    st.markdown("---")
    cols = st.columns([1, 1, 2])
    
    with cols[0]:
        if st.button("🔀 Posición Aleatoria", key="btn_random_reinas"):
            # Genera un nuevo vector con números al azar del 0 al 7
            st.session_state.estado_reinas = [random.randint(0, 7) for _ in range(8)]
            st.rerun()
            
    with cols[1]:
        if st.button("▶️ Ejecutar Paso", key="btn_ejecutar_paso"):
            if algoritmo == "Hill Climbing":
                # Verificamos si ya ganamos
                if calcular_ataques(st.session_state.estado_reinas) == 0:
                    st.success("¡Máximo Global alcanzado! 0 ataques.")
                else:
                    nuevo_estado, mejoro = ejecutar_paso_hill_climbing(st.session_state.estado_reinas)
                    
                    if mejoro:
                        st.session_state.estado_reinas = nuevo_estado
                        st.rerun() # Refresca la pantalla para ver el movimiento
                    else:
                        st.error("❌ Atascado en un Óptimo Local. Usa la posición aleatoria para reiniciar.")
            else:
                st.info("Próximamente: Recocido Simulado con temperatura y aceptación de movimientos peores.    ")
# ========================================== Parte del Gato (con tablero visual) ==========================================
# 1. Prueba Terminal y Función de Utilidad
def verificar_estado_gato(tablero):
    """
    Evalúa si el juego terminó y devuelve la utilidad.
    MAX (X) busca +1, MIN (O) busca -1. Empate es 0.
    """
    lineas_ganadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontales
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Verticales
        [0, 4, 8], [2, 4, 6]             # Diagonales
    ]
    
    for linea in lineas_ganadoras:
        a, b, c = linea
        if tablero[a] == tablero[b] == tablero[c] and tablero[a] != ' ':
            return 1 if tablero[a] == 'X' else -1
            
    if ' ' not in tablero:
        return 0 # Empate
        
    return None # El juego continúa

# 2. Algoritmos de Búsqueda Adversaria
def minimax_clasico(tablero, es_maximizador):
    """Fuerza bruta: Simula todas las jugadas posibles sin cortes."""
    st.session_state.nodos_evaluados += 1 # Contador de nodos
    utilidad = verificar_estado_gato(tablero)
    if utilidad is not None: return utilidad
        
    if es_maximizador:
        mejor_valor = -math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = 'X' 
                mejor_valor = max(mejor_valor, minimax_clasico(tablero, False))
                tablero[i] = ' ' 
        return mejor_valor
    else:
        mejor_valor = math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = 'O' 
                mejor_valor = min(mejor_valor, minimax_clasico(tablero, True))
                tablero[i] = ' '
        return mejor_valor

def minimax_alfa_beta_gato(tablero, profundidad, es_maximizador, alfa, beta):
    """Optimizado: Utiliza Poda Alfa-Beta para descartar ramas inútiles."""
    st.session_state.nodos_evaluados += 1 # Contador de nodos
    utilidad = verificar_estado_gato(tablero)
    
    if utilidad is not None:
        if utilidad == 1: return utilidad - (profundidad * 0.1)
        elif utilidad == -1: return utilidad + (profundidad * 0.1)
        else: return 0
        
    if es_maximizador:
        mejor_valor = -math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = 'X' 
                mejor_valor = max(mejor_valor, minimax_alfa_beta_gato(tablero, profundidad + 1, False, alfa, beta))
                tablero[i] = ' ' 
                alfa = max(alfa, mejor_valor)
                if beta <= alfa: break # PODA
        return mejor_valor
    else:
        mejor_valor = math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = 'O' 
                mejor_valor = min(mejor_valor, minimax_alfa_beta_gato(tablero, profundidad + 1, True, alfa, beta))
                tablero[i] = ' '
                beta = min(beta, mejor_valor)
                if beta <= alfa: break # PODA
        return mejor_valor

# 3. Función auxiliar para que la IA mueva según el algoritmo elegido
def mejor_movimiento_ia(tablero, algoritmo):
    mejor_valor = math.inf
    mejor_movimiento = -1
    st.session_state.nodos_evaluados = 0 # Reiniciamos el contador por cada turno
    
    for i in range(9):
        if tablero[i] == ' ':
            tablero[i] = 'O' 
            
            if algoritmo == "Minimax Clásico":
                valor = minimax_clasico(tablero, True)
            else:
                valor = minimax_alfa_beta_gato(tablero, 0, True, -math.inf, math.inf)
                
            tablero[i] = ' '
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = i
                
    return mejor_movimiento

def mostrar_gato():
    st.header("Gato / Tic-Tac-Toe")
    st.subheader("Búsqueda Adversaria")
    
    # Menú para comparar los algoritmos
    algoritmo = st.radio("Selecciona el algoritmo de la IA:", ("Minimax Clásico", "Poda Alfa-Beta"), horizontal=True)
    st.info("Juegas como MAX (X). La IA juega como MIN (O). Observa la diferencia de nodos evaluados.")
    
    # 1. Inicializamos la memoria
    if 'tablero_gato' not in st.session_state:
        st.session_state.tablero_gato = [' '] * 9
        st.session_state.ganador_gato = None
    if 'nodos_evaluados' not in st.session_state:
        st.session_state.nodos_evaluados = 0

    # Mostrar contador de eficiencia
    st.write(f"**Nodos evaluados en el último turno de la IA:** `{st.session_state.nodos_evaluados}`")

    # 2. Dibujamos la cuadrícula 3x3
    st.write("### Tablero de Juego")
    cols = st.columns([1, 1, 1, 3]) 
    
    for i in range(9):
        with cols[i % 3]:
            etiqueta = st.session_state.tablero_gato[i] if st.session_state.tablero_gato[i] != ' ' else '...'
            deshabilitado = st.session_state.tablero_gato[i] != ' ' or st.session_state.ganador_gato is not None
            
            if st.button(etiqueta, key=f"casilla_{i}", use_container_width=True, disabled=deshabilitado):
                # Turno MAX
                st.session_state.tablero_gato[i] = 'X'
                st.session_state.ganador_gato = verificar_estado_gato(st.session_state.tablero_gato)
                
                # Turno MIN
                if st.session_state.ganador_gato is None:
                    # Inyectamos el algoritmo seleccionado
                    movimiento_ia = mejor_movimiento_ia(st.session_state.tablero_gato, algoritmo)
                    if movimiento_ia != -1:
                        st.session_state.tablero_gato[movimiento_ia] = 'O'
                        st.session_state.ganador_gato = verificar_estado_gato(st.session_state.tablero_gato)
                
                st.rerun()

    # 3. Mostrar resultado
    if st.session_state.ganador_gato is not None:
        st.markdown("---")
        if st.session_state.ganador_gato == 1:
            st.success("¡Ganaste! (Esto es imposible contra Minimax perfecto)")
        elif st.session_state.ganador_gato == -1:
            st.error("¡La IA (MIN) gana!")
        else:
            st.warning("¡Empate! (Suma Cero)")

    st.markdown("---")
    if st.button("🔄 Reiniciar Tablero", type="primary"):
        st.session_state.tablero_gato = [' '] * 9
        st.session_state.ganador_gato = None
        st.session_state.nodos_evaluados = 0
        st.rerun()

# ==========================================
# CONTROLADOR PRINCIPAL (Sidebar y Navegación)
# ==========================================
def main():
    st.sidebar.title("Navegación")
    
    # Menú de selección
    opcion = st.sidebar.radio(
        "Selecciona el problema a visualizar:",
        ("Inicio", 
         "1. Frozen Lake (No Informada)", 
         "2. Sokoban (Informada)", 
         "3. 8 Reinas (Local)", 
         "4. Gato (Adversaria)")
    )

    # Ruteo de las opciones
    if opcion == "Inicio":
        st.title("Evaluación Práctica: Algoritmos de Búsqueda")
        st.markdown("### Objetivo")
        st.write("Desarrollar una aplicación interactiva que permita visualizar y comparar algoritmos de búsqueda aplicados a cuatro tipos de problemas clásicos.")
        st.markdown("---")
        st.write("**Utiliza el menú lateral para seleccionar un problema y comenzar.**")
        
    elif opcion == "1. Frozen Lake (No Informada)":
        mostrar_frozen_lake()
        
    elif opcion == "2. Sokoban (Informada)":
        mostrar_sokoban()
        
    elif opcion == "3. 8 Reinas (Local)":
        mostrar_reinas()
        
    elif opcion == "4. Gato (Adversaria)":
        mostrar_gato()

if __name__ == "__main__":
    main()