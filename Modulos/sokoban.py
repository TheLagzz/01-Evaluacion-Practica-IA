import streamlit as st
import random
import heapq


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

	mapas_pool = [
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

	cols_control = st.columns([1, 1, 1])

	with cols_control[0]:
		if st.button("🔀 Nivel Aleatorio", key="btn_soko_random"):
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
