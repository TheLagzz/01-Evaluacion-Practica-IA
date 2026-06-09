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
    """Obtiene las coordenadas válidas a las que se puede mover (Arriba, Abajo, Izq, Der)."""
    f, c = estado
    vecinos = []
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Arriba, Abajo, Izquierda, Derecha
    
    for df, dc in movimientos:
        nf, nc = f + df, c + dc
        # 1. Validar que no se salga del mapa 4x4
        if 0 <= nf < 4 and 0 <= nc < 4:
            # 2. Validar que la celda no sea un hoyo ('H')
            if mapa[nf][nc] != 'H':
                vecinos.append((nf, nc))
    return vecinos

def buscar_ruta_laberinto(mapa, inicio, meta, algoritmo):
    """Ejecuta BFS o DFS y devuelve la ruta encontrada y los nodos visitados."""
    # Guardamos tuplas de (estado_actual, ruta_hasta_aqui)
    estructura_datos = [(inicio, [inicio])] 
    visitados = set([inicio])
    nodos_expandidos = []

    while estructura_datos:
        # AQUÍ ESTÁ LA MAGIA DE LA IA NO INFORMADA:
        if algoritmo == "BFS":
            actual, ruta = estructura_datos.pop(0) # COLA: Extrae del inicio
        else: # DFS
            actual, ruta = estructura_datos.pop(-1) # PILA: Extrae del final

        nodos_expandidos.append(actual)

        # Prueba de meta
        if actual == meta:
            return nodos_expandidos, ruta

        # Expansión de vecinos
        for vecino in obtener_vecinos_laberinto(actual, mapa):
            if vecino not in visitados:
                visitados.add(vecino)
                estructura_datos.append((vecino, ruta + [vecino]))

    return nodos_expandidos, [] # Retorna vacío si no hay solución

def mostrar_frozen_lake():
    st.header("Laberinto Frozen Lake")
    st.subheader("Búsqueda No Informada")
    algoritmo = st.radio("Selecciona el algoritmo:", ("BFS", "DFS"), horizontal=True)
    
    # 1. Definir el mapa fijo del laberinto 4x4
    # S: Start (Inicio), F: Frozen (Seguro), H: Hole (Agujero), G: Goal (Meta)
    mapa = [
        ['S', 'F', 'F', 'F'],
        ['F', 'H', 'F', 'H'],
        ['F', 'F', 'F', 'H'],
        ['H', 'F', 'F', 'G']
    ]
    
    # Diccionario visual para transformar las letras en emojis
    iconos = {
        'S': '🧍‍♂️', # Jugador en el inicio
        'F': '🧊', # Hielo seguro
        'H': '🕳️', # Hoyo
        'G': '🏆'  # Meta
    }

    st.write("### Mapa del entorno")
    
    # 2. Dibujar la cuadrícula en Streamlit
    # Usamos columnas para simular el tablero 4x4
    for fila in mapa:
        cols = st.columns([1, 1, 1, 1, 4]) # 4 casillas y un espacio en blanco al final
        for j, celda in enumerate(fila):
            with cols[j]:
                # Pintamos el cuadro como un botón deshabilitado solo para que se vea como un "bloque"
                st.button(iconos[celda], key=f"celda_{id(fila)}_{j}", use_container_width=True, disabled=True)
                
    st.markdown("---")
    
    # 3. Controles
    if st.button("▶️ Ejecutar Búsqueda y Animar", key="btn_animar_frozen", type="primary"):
        inicio = (0, 0)
        meta = (3, 3)
        
        # Ejecutamos el algoritmo matemático
        expandidos, ruta = buscar_ruta_laberinto(mapa, inicio, meta, algoritmo)
        
        if ruta:
            st.success(f"¡Ruta encontrada usando {algoritmo}! Reproduciendo...")
            st.write(f"**Nodos explorados:** {len(expandidos)}")
            
            # 4. LA MAGIA DE LA ANIMACIÓN
            # Creamos un contenedor vacío en la pantalla
            contenedor_animacion = st.empty()
            
            # Recorremos la ruta paso por paso (creando fotogramas)
            for i, paso_actual in enumerate(ruta):
                with contenedor_animacion.container():
                    st.write(f"**Paso actual:** {i} / {len(ruta)-1}")
                    
                    for fila in range(4):
                        cols = st.columns([1, 1, 1, 1, 4])
                        for col in range(4):
                            celda = mapa[fila][col]
                            
                            # Lógica para decidir qué pintar en este fotograma
                            if (fila, col) == paso_actual:
                                icono_mostrar = '🧍‍♂️'  # El jugador moviéndose
                            elif (fila, col) in ruta[:i]:
                                icono_mostrar = '🐾'  # Las huellas pasadas
                            else:
                                icono_mostrar = iconos[celda] # El mapa original
                                
                            with cols[col]:
                                # Key dinámica obligatoria para que Streamlit no tire error en el loop
                                st.button(icono_mostrar, key=f"anim_fl_{fila}_{col}_{i}", use_container_width=True, disabled=True)
                
                # Pausamos medio segundo antes de sobreescribir con el siguiente paso
                time.sleep(0.5)
            
            st.balloons() # Efecto de victoria al llegar a la meta
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
    """
    Algoritmo A* que evalúa f(n) = g(n) + h(n).
    Devuelve una lista de tuplas con el estado completo (jugador, cajas) de cada paso.
    """
    paredes = set()
    metas = set()
    inicio_jugador = None
    inicio_cajas = set()

    for f in range(5):
        for c in range(5):
            celda = mapa_inicial[f][c]
            if celda == 'W': paredes.add((f, c))
            elif celda == 'T': metas.add((f, c))
            elif celda == 'B': inicio_cajas.add((f, c))
            elif celda == 'P': inicio_jugador = (f, c)

    inicio_cajas = tuple(sorted(inicio_cajas))
    
    # La ruta ahora almacena el historial de estados completos: [(jugador, cajas), ...]
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

            if n_j in paredes:
                continue

            if n_j in cajas:
                n_caja = (n_j[0] + df, n_j[1] + dc)
                if n_caja in paredes or n_caja in cajas:
                    continue
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
    st.header("Sokoban")
    st.subheader("Búsqueda Informada (A*)")
    algoritmo = st.radio("Selecciona el algoritmo:", ("A*",), horizontal=True)
    
    # 1. Definir el mapa 5x5 del nivel
    # W: Wall (Pared), E: Empty (Vacio), P: Player (Jugador)
    # B: Box (Caja), T: Target (Objetivo)
    mapa_sokoban = [
        ['W', 'W', 'W', 'W', 'W'],
        ['W', 'E', 'T', 'E', 'W'],
        ['W', 'E', 'B', 'E', 'W'],
        ['W', 'E', 'P', 'E', 'W'],
        ['W', 'W', 'W', 'W', 'W']
    ]
    
    # Diccionario visual
    iconos_soko = {
        'W': '🧱',
        'E': '⬛',
        'P': '🧍',
        'B': '📦',
        'T': '🎯'
    }

    st.write("### Nivel 1")
    
    # 2. Renderizar el nivel
    for fila in mapa_sokoban:
        # 5 columnas para el mapa y una vacía para dar espacio
        cols = st.columns([1, 1, 1, 1, 1, 3]) 
        for j, celda in enumerate(fila):
            with cols[j]:
                st.button(iconos_soko[celda], key=f"soko_{id(fila)}_{j}", use_container_width=True, disabled=True)
                
    st.markdown("---")
    
    # 3. Controles
    if st.button("▶️ Resolver Nivel", key="btn_resolver_sokoban", type="primary"):
        # Ejecutamos el motor de búsqueda A*
        ruta_pasos = resolver_sokoban_astar(mapa_sokoban)
        
        if ruta_pasos:
            st.success(f"¡Nivel resuelto de manera óptima por A* en {len(ruta_pasos)-1} pasos!")
            
            # Mostramos un resumen de las coordenadas calculadas en el árbol
            st.write(f"**Secuencia de movimientos calculada:** {ruta_pasos}")
        else:
            st.error("No se encontró una secuencia de empujes válida para resolver el mapa.")
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

def ejecutar_paso_simulated_annealing(estado, temperatura):
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
    algoritmo = st.radio("Selecciona el algoritmo:", ("Hill Climbing", "Simulated Annealing"), horizontal=True)
    # ... (debajo de tu st.radio de algoritmos) ...
    
    # Agregamos la Temperatura a la memoria
    if 'estado_reinas' not in st.session_state:
        st.session_state.estado_reinas = [0, 1, 2, 3, 4, 5, 6, 7]
    if 'temperatura' not in st.session_state:
        st.session_state.temperatura = 10.0 # Temperatura inicial
        
    ataques = calcular_ataques(st.session_state.estado_reinas)
    color_texto = "green" if ataques == 0 else "red"
    
    # Mostramos la temperatura en pantalla si está en Simulated Annealing
    if algoritmo == "Simulated Annealing":
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
                
                elif algoritmo == "Simulated Annealing":
                    nuevo_estado, aceptado, nueva_temp = ejecutar_paso_simulated_annealing(
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
                st.info("Próximamente: Simulated Annealing")
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

# 2. Algoritmo Minimax (Recursivo)
def minimax_gato(tablero, es_maximizador):
    """
    Simula todas las jugadas posibles hasta las hojas y respalda el valor minimax.
    """
    utilidad = verificar_estado_gato(tablero)
    
    # Condición de paro: si es nodo terminal, devolver U(s)
    if utilidad is not None:
        return utilidad
        
    if es_maximizador:
        mejor_valor = -math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = 'X' # Acción de MAX
                valor = minimax_gato(tablero, False)
                tablero[i] = ' ' # Deshacer acción (Backtracking)
                mejor_valor = max(mejor_valor, valor) # Conservar el máximo
        return mejor_valor
    else:
        mejor_valor = math.inf
        for i in range(9):
            if tablero[i] == ' ':
                tablero[i] = 'O' # Acción de MIN
                valor = minimax_gato(tablero, True)
                tablero[i] = ' '
                mejor_valor = min(mejor_valor, valor) # Conservar el mínimo
        return mejor_valor

# 3. Función auxiliar para que la IA mueva
def mejor_movimiento_ia(tablero):
    mejor_valor = math.inf
    mejor_movimiento = -1
    
    for i in range(9):
        if tablero[i] == ' ':
            tablero[i] = 'O' # La IA es MIN
            valor = minimax_gato(tablero, True)
            tablero[i] = ' '
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = i
                
    return mejor_movimiento

def mostrar_gato():
    st.header("Gato / Tic-Tac-Toe")
    st.subheader("Búsqueda Adversaria")
    st.info("Juegas como MAX (X). La IA juega como MIN (O) usando Minimax perfecto.")
    
    # 1. Inicializamos el tablero en la memoria
    if 'tablero_gato' not in st.session_state:
        st.session_state.tablero_gato = [' '] * 9
        st.session_state.ganador_gato = None

    # 2. Dibujamos la cuadrícula 3x3
    st.write("### Tablero de Juego")
    cols = st.columns([1, 1, 1, 3]) 
    
    for i in range(9):
        with cols[i % 3]:
            etiqueta = st.session_state.tablero_gato[i] if st.session_state.tablero_gato[i] != ' ' else '...'
            
            # Bloquear botones si la casilla está ocupada o ya hay ganador
            deshabilitado = st.session_state.tablero_gato[i] != ' ' or st.session_state.ganador_gato is not None
            
            if st.button(etiqueta, key=f"casilla_{i}", use_container_width=True, disabled=deshabilitado):
                # Turno del Jugador (MAX)
                st.session_state.tablero_gato[i] = 'X'
                st.session_state.ganador_gato = verificar_estado_gato(st.session_state.tablero_gato)
                
                # Turno de la IA (MIN) si el juego no ha terminado
                if st.session_state.ganador_gato is None:
                    movimiento_ia = mejor_movimiento_ia(st.session_state.tablero_gato)
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