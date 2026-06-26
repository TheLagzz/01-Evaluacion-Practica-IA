import streamlit as st
import random
import time

"""Módulo para el entorno de Frozen Lake, un laberinto con obstáculos (H) y una meta (G). El agente inicia en S y debe encontrar la ruta a G evitando los agujeros."""
def obtener_vecinos_laberinto(posicion_actual, mapa_laberinto):
	"""fila_actual y columna_actual representan la posición del agente."""
	fila_actual, columna_actual = posicion_actual
	vecinos_validos = []
	"""Movimientos posibles: arriba, abajo, izquierda, derecha. Se mezclan para que DFS no siempre explore en el mismo orden."""
	movimientos_posibles = [(-1, 0), (1, 0), (0, -1), (0, 1)]
	random.shuffle(movimientos_posibles)

	numero_filas = len(mapa_laberinto)
	numero_columnas = len(mapa_laberinto[0])
	"""delta_fila y delta_columna representan el cambio en la posición para cada movimiento."""
	for delta_fila, delta_columna in movimientos_posibles:
		nueva_fila, nueva_columna = fila_actual + delta_fila, columna_actual + delta_columna
		if 0 <= nueva_fila < numero_filas and 0 <= nueva_columna < numero_columnas:
			if mapa_laberinto[nueva_fila][nueva_columna] != 'H':
				vecinos_validos.append((nueva_fila, nueva_columna))
	return vecinos_validos

"""La función principal que ejecuta la búsqueda BFS o DFS y devuelve la ruta encontrada y los nodos visitados para animar el proceso."""
def buscar_ruta_laberinto(mapa_laberinto, estado_inicio, estado_meta, algoritmo_busqueda):
	"""Ejecuta BFS o DFS y devuelve la ruta encontrada y los nodos visitados."""
	frontera = [(estado_inicio, [estado_inicio])]
	estados_visitados = set([estado_inicio])
	nodos_expandidos = []

	while frontera:
		if algoritmo_busqueda == "BFS":
			estado_actual, ruta_actual = frontera.pop(0) # BFS: se saca el primer elemento (cola)
		else:
			estado_actual, ruta_actual = frontera.pop(-1) # DFS: se saca el último elemento (pila)

		nodos_expandidos.append(estado_actual)

		if estado_actual == estado_meta:
			return nodos_expandidos, ruta_actual

		for estado_vecino in obtener_vecinos_laberinto(estado_actual, mapa_laberinto):
			if estado_vecino not in estados_visitados:
				estados_visitados.add(estado_vecino)
				frontera.append((estado_vecino, ruta_actual + [estado_vecino]))

	return nodos_expandidos, []

"""Función para mostrar el entorno de Frozen Lake, permitir al usuario seleccionar el algoritmo y animar la búsqueda paso a paso."""
def mostrar_frozen_lake():
	st.header("🧊 Laberinto Frozen Lake")
	st.subheader("Búsqueda No Informada")
	algoritmo_busqueda = st.radio("Selecciona el algoritmo:", ("BFS", "DFS"), horizontal=True)

	mapa_laberinto = [
		['S', 'F', 'H', 'F', 'F', 'F'],
		['F', 'F', 'H', 'F', 'H', 'F'],
		['H', 'F', 'F', 'F', 'H', 'F'],
		['F', 'H', 'F', 'H', 'H', 'F'],
		['F', 'F', 'F', 'F', 'F', 'F'],
		['F', 'H', 'F', 'H', 'H', 'G']
	]

	iconos_celdas = {'S': '🧍‍♂️', 'F': '🧊', 'H': '🕳️', 'G': '🏆'}
	numero_filas = len(mapa_laberinto)
	numero_columnas = len(mapa_laberinto[0])

	estado_inicio = None
	estado_meta = None
	for fila_indice in range(numero_filas):
		for columna_indice in range(numero_columnas):
			if mapa_laberinto[fila_indice][columna_indice] == 'S': estado_inicio = (fila_indice, columna_indice)
			elif mapa_laberinto[fila_indice][columna_indice] == 'G': estado_meta = (fila_indice, columna_indice)

	st.write("### Mapa del entorno")

	pesos_columnas = [1] * numero_columnas + [4]

	for fila_tablero in mapa_laberinto:
		columnas_visuales = st.columns(pesos_columnas)
		for indice_columna, tipo_celda in enumerate(fila_tablero):
			with columnas_visuales[indice_columna]:
				st.button(iconos_celdas[tipo_celda], key=f"celda_{id(fila_tablero)}_{indice_columna}", use_container_width=True, disabled=True)

	st.markdown("---")

	if st.button("▶️ Ejecutar Búsqueda y Animar", key="btn_animar_frozen", type="primary"):
		nodos_expandidos, ruta_encontrada = buscar_ruta_laberinto(mapa_laberinto, estado_inicio, estado_meta, algoritmo_busqueda)

		if ruta_encontrada:
			st.success(f"¡Ruta encontrada usando {algoritmo_busqueda}! Reproduciendo...")
			st.write(f"**Nodos explorados:** {len(nodos_expandidos)} (Nota cómo DFS se atora en los callejones)")

			contenedor_animacion = st.empty()

			for indice_paso, estado_en_ruta in enumerate(ruta_encontrada):
				with contenedor_animacion.container():
					st.write(f"**Paso actual:** {indice_paso} / {len(ruta_encontrada)-1}")

					for fila_indice in range(numero_filas):
						columnas_visuales = st.columns(pesos_columnas)
						for columna_indice in range(numero_columnas):
							tipo_celda = mapa_laberinto[fila_indice][columna_indice]

							if (fila_indice, columna_indice) == estado_en_ruta:
								icono_mostrar = '🧍‍♂️'
							elif (fila_indice, columna_indice) in ruta_encontrada[:indice_paso]:
								icono_mostrar = '🐾'
							else:
								icono_mostrar = iconos_celdas[tipo_celda]

							with columnas_visuales[columna_indice]:
								st.button(icono_mostrar, key=f"anim_fl_{fila_indice}_{columna_indice}_{indice_paso}", use_container_width=True, disabled=True)
				time.sleep(0.5)

			st.balloons()
		else:
			st.error("No se encontró ninguna ruta a la meta.")
