import streamlit as st
import random
import heapq


def obtener_distancia_manhattan(posiciones_cajas, posiciones_metas):
	"""
	Función Heurística h(n): Suma de las distancias en cruz
	desde cada caja hasta su meta más cercana.
	"""
	distancia_total = 0
	for posicion_caja in posiciones_cajas:
		distancia_total += min(abs(posicion_caja[0] - posicion_meta[0]) + abs(posicion_caja[1] - posicion_meta[1]) for posicion_meta in posiciones_metas) #Es la formula de la distancia Manhattan, que calcula la distancia entre dos puntos en una cuadrícula sumando las diferencias absolutas de sus coordenadas. En este caso, se calcula la distancia desde cada caja hasta su meta más cercana y se suma para obtener la heurística total.
	return distancia_total


def resolver_sokoban_astar(mapa_inicial):
	"""Algoritmo A* que evalúa f(n) = g(n) + h(n). Dinámico para cualquier tamaño de mapa."""
	posiciones_paredes = set()
	posiciones_metas = set()
	posicion_inicial_jugador = None
	posiciones_iniciales_cajas = set()

	numero_filas = len(mapa_inicial)
	numero_columnas = len(mapa_inicial[0])

	for fila_indice in range(numero_filas):
		for columna_indice in range(numero_columnas):
			tipo_celda = mapa_inicial[fila_indice][columna_indice]
			if tipo_celda == 'W': posiciones_paredes.add((fila_indice, columna_indice))
			elif tipo_celda == 'T': posiciones_metas.add((fila_indice, columna_indice))
			elif tipo_celda == 'B': posiciones_iniciales_cajas.add((fila_indice, columna_indice))
			elif tipo_celda == 'P': posicion_inicial_jugador = (fila_indice, columna_indice)

	posiciones_iniciales_cajas = tuple(sorted(posiciones_iniciales_cajas)) # Se usa inicio_cajas como una tupla ordenada para garantizar que el estado sea hashable y se pueda almacenar en el conjunto de visitados.

	heuristica_inicial = obtener_distancia_manhattan(posiciones_iniciales_cajas, posiciones_metas)
	frontera = [(heuristica_inicial, 0, posicion_inicial_jugador, posiciones_iniciales_cajas, [(posicion_inicial_jugador, posiciones_iniciales_cajas)])]
	estados_visitados = set([(posicion_inicial_jugador, posiciones_iniciales_cajas)])
	movimientos_posibles = [(-1, 0), (1, 0), (0, -1), (0, 1)]

	while frontera: #open_set es un arbol
		"""Es un arbol de búsqueda, cada nodo es un estado del juego (posición del jugador y posiciones de las cajas). Se utiliza una cola de prioridad (heap) para expandir primero los nodos con menor f(n)."""
		_, costo_acumulado, posicion_jugador, posiciones_cajas, ruta = heapq.heappop(frontera) # Se usa para saber si ya gano o no, si gano se devuelve la ruta, si no se siguen expandiendo nodos, es un arbol binario
		"""Convierte las coordenadas de las cajas en una tupla ordenada para garantizar que el estado sea hashable y se pueda almacenar en el conjunto de visitados."""
		if set(posiciones_cajas) == posiciones_metas:
			return ruta

		fila_jugador, columna_jugador = posicion_jugador
		for delta_fila, delta_columna in movimientos_posibles:

			posicion_siguiente_jugador = (fila_jugador + delta_fila, columna_jugador + delta_columna)#Sirve para calcular la nueva posición del jugador después de aplicar el movimiento (df, dc) al estado actual (f_j, c_j).

			if posicion_siguiente_jugador in posiciones_paredes: continue #Si la nueva posición del jugador cae en una pared, se ignora esa acción y se continúa con el siguiente movimiento posible.

			if posicion_siguiente_jugador in posiciones_cajas:
				posicion_siguiente_caja = (posicion_siguiente_jugador[0] + delta_fila, posicion_siguiente_jugador[1] + delta_columna)
				if posicion_siguiente_caja in posiciones_paredes or posicion_siguiente_caja in posiciones_cajas: continue
				"""Se usa una tupla ordenada para las cajas para garantizar que el estado sea hashable y se pueda almacenar en el conjunto de visitados."""
				posiciones_cajas_actualizadas = tuple(sorted([posicion_siguiente_caja if posicion_caja == posicion_siguiente_jugador else posicion_caja for posicion_caja in posiciones_cajas]))
			else:
				posiciones_cajas_actualizadas = posiciones_cajas

			estado_siguiente = (posicion_siguiente_jugador, posiciones_cajas_actualizadas)

			if estado_siguiente not in estados_visitados:
				estados_visitados.add(estado_siguiente)
				costo_nuevo = costo_acumulado + 1
				heuristica_nueva = obtener_distancia_manhattan(posiciones_cajas_actualizadas, posiciones_metas)
				costo_total_estimado = costo_nuevo + heuristica_nueva # f(n) = g(n) + h(n) Formula de A* para evaluar el costo total estimado del camino a la solución
				heapq.heappush(frontera, (costo_total_estimado, costo_nuevo, posicion_siguiente_jugador, posiciones_cajas_actualizadas, ruta + [estado_siguiente])) #Heurística A* para priorizar estados más prometedores

	return []


def mostrar_sokoban():
	st.header("📦 Sokoban")
	st.subheader("Búsqueda Informada (A*)")

	lista_mapas = [
		[['W', 'W', 'W', 'W', 'W'], ['W', 'E', 'T', 'E', 'W'], ['W', 'E', 'B', 'E', 'W'], ['W', 'E', 'P', 'E', 'W'], ['W', 'W', 'W', 'W', 'W']],
		[['W', 'W', 'W', 'W', 'W'], ['W', 'T', 'E', 'E', 'W'], ['W', 'E', 'B', 'E', 'W'], ['W', 'E', 'E', 'P', 'W'], ['W', 'W', 'W', 'W', 'W']],
		[['W', 'W', 'W', 'W', 'W'], ['W', 'E', 'E', 'T', 'W'], ['W', 'E', 'B', 'E', 'W'], ['W', 'P', 'E', 'E', 'W'], ['W', 'W', 'W', 'W', 'W']],
		[['W', 'W', 'W', 'W', 'W'], ['W', 'T', 'E', 'T', 'W'], ['W', 'E', 'B', 'B', 'W'], ['W', 'E', 'E', 'P', 'W'], ['W', 'W', 'W', 'W', 'W']],
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

	if 'indice_mapa_sokoban' not in st.session_state: st.session_state.indice_mapa_sokoban = 0
	if 'ruta_sokoban' not in st.session_state: st.session_state.ruta_sokoban = None
	if 'indice_paso_sokoban' not in st.session_state: st.session_state.indice_paso_sokoban = 0

	mapa_actual = lista_mapas[st.session_state.indice_mapa_sokoban]
	numero_filas = len(mapa_actual)
	numero_columnas = len(mapa_actual[0])

	posiciones_paredes = set()
	posiciones_metas = set()
	for fila_indice in range(numero_filas):
		for columna_indice in range(numero_columnas):
			if mapa_actual[fila_indice][columna_indice] == 'W': posiciones_paredes.add((fila_indice, columna_indice))
			if mapa_actual[fila_indice][columna_indice] == 'T': posiciones_metas.add((fila_indice, columna_indice))

	if st.session_state.ruta_sokoban and st.session_state.indice_paso_sokoban < len(st.session_state.ruta_sokoban):
		posicion_jugador_actual, posiciones_cajas_actuales = st.session_state.ruta_sokoban[st.session_state.indice_paso_sokoban]
	else:
		posicion_jugador_actual = None
		posiciones_cajas_actuales = set()
		for fila_indice in range(numero_filas):
			for columna_indice in range(numero_columnas):
				if mapa_actual[fila_indice][columna_indice] == 'P': posicion_jugador_actual = (fila_indice, columna_indice)
				elif mapa_actual[fila_indice][columna_indice] == 'B': posiciones_cajas_actuales.add((fila_indice, columna_indice))
		posiciones_cajas_actuales = tuple(posiciones_cajas_actuales)

	iconos_sokoban = {'W': '🧱', 'E': '⬛', 'P': '🧍', 'B': '📦', 'T': '🎯', 'BT': '✅'}

	st.write(f"### Configuración del Tablero (Nivel {st.session_state.indice_mapa_sokoban + 1})")

	pesos_columnas = [1] * numero_columnas + [3]
	for fila_indice in range(numero_filas):
		columnas_visuales = st.columns(pesos_columnas)
		for columna_indice in range(numero_columnas):
			coordenada = (fila_indice, columna_indice)
			if coordenada in posiciones_paredes: icono = iconos_sokoban['W']
			elif coordenada == posicion_jugador_actual: icono = iconos_sokoban['P']
			elif coordenada in posiciones_cajas_actuales and coordenada in posiciones_metas: icono = iconos_sokoban['BT']
			elif coordenada in posiciones_cajas_actuales: icono = iconos_sokoban['B']
			elif coordenada in posiciones_metas: icono = iconos_sokoban['T']
			else: icono = iconos_sokoban['E']

			with columnas_visuales[columna_indice]:
				st.button(icono, key=f"soko_cell_{fila_indice}_{columna_indice}_{st.session_state.indice_paso_sokoban}", use_container_width=True, disabled=True)

	st.markdown("---")

	cols_control = st.columns([1, 1, 1])

	with cols_control[0]:
		if st.button("🔀 Nivel Aleatorio", key="btn_soko_random"):
			opciones_nivel = [indice_mapa for indice_mapa in range(len(lista_mapas)) if indice_mapa != st.session_state.indice_mapa_sokoban]
			st.session_state.indice_mapa_sokoban = random.choice(opciones_nivel)
			st.session_state.ruta_sokoban = None
			st.session_state.indice_paso_sokoban = 0
			st.rerun()

	with cols_control[1]:
		if st.button("🧠 Calcular Ruta (A*)", key="btn_soko_calcular"):
			st.session_state.ruta_sokoban = resolver_sokoban_astar(mapa_actual)
			st.session_state.indice_paso_sokoban = 0
			if st.session_state.ruta_sokoban:
				st.success("¡Estrategia óptima calculada!")
			else:
				st.error("Este mapa no tiene solución.")
			st.rerun()

	with cols_control[2]:
		if st.session_state.ruta_sokoban:
			total_pasos = len(st.session_state.ruta_sokoban) - 1

			if st.session_state.indice_paso_sokoban < total_pasos:
				if st.button(f"➡️ Siguiente Paso ({st.session_state.indice_paso_sokoban}/{total_pasos})", key="btn_soko_step"):
					st.session_state.indice_paso_sokoban += 1
					st.rerun()
			else:
				st.success("🎉 ¡Objetivo alcanzado!")
				if st.button("🔄 Reiniciar Nivel", key="btn_soko_reset"):
					st.session_state.ruta_sokoban = None
					st.session_state.indice_paso_sokoban = 0
					st.rerun()
