import streamlit as st
import random
import time


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
			actual, ruta = estructura_datos.pop(0)
		else:
			actual, ruta = estructura_datos.pop(-1)

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

	inicio = None
	meta = None
	for f in range(filas):
		for c in range(columnas):
			if mapa[f][c] == 'S': inicio = (f, c)
			elif mapa[f][c] == 'G': meta = (f, c)

	st.write("### Mapa del entorno")

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
