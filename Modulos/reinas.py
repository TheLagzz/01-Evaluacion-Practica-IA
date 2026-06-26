import streamlit as st
import random
import math
import time


def calcular_ataques(estado_reinas):
	"""
	Calcula cuántos pares de reinas se están atacando.
	Un estado perfecto devolverá 0.
	"""
	cantidad_ataques = 0
	for columna_actual in range(8):
		for otra_columna in range(columna_actual + 1, 8):
			if estado_reinas[columna_actual] == estado_reinas[otra_columna]: #Si dos reinas están en la misma fila, se cuentan como un ataque.
				cantidad_ataques += 1
			elif abs(columna_actual - otra_columna) == abs(estado_reinas[columna_actual] - estado_reinas[otra_columna]): #Si dos reinas están en la misma diagonal, se cuentan como un ataque. La condición abs(i - j) == abs(estado[i] - estado[j]) verifica si las reinas en las columnas i y j están en la misma diagonal, lo que ocurre cuando la diferencia de filas es igual a la diferencia de columnas.
				cantidad_ataques += 1
	return cantidad_ataques


def ejecutar_paso_hill_climbing(estado_reinas):
	"""
	Evalúa todos los vecinos posibles (mover una reina en su columna)
	y selecciona el que tenga el menor número de ataques.
	"""
	estado_mejor = list(estado_reinas)
	menor_cantidad_ataques = calcular_ataques(estado_reinas)
	hubo_mejora = False

	for columna_actual in range(8):
		for fila_objetivo in range(8):
			if fila_objetivo != estado_reinas[columna_actual]:
				estado_vecino = list(estado_reinas)
				estado_vecino[columna_actual] = fila_objetivo
				cantidad_ataques_vecino = calcular_ataques(estado_vecino)

				if cantidad_ataques_vecino < menor_cantidad_ataques:
					menor_cantidad_ataques = cantidad_ataques_vecino
					estado_mejor = list(estado_vecino)
					hubo_mejora = True

	return estado_mejor, hubo_mejora


def ejecutar_paso_recocido_simulado(estado_reinas, temperatura_actual):
	"""
	Toma un vecino al azar. Si es mejor, lo acepta.
	Si es peor, lo acepta con una probabilidad P = e^(-ΔE / T).
	"""
	ataques_actuales = calcular_ataques(estado_reinas)

	columna_aleatoria = random.randint(0, 7)
	fila_aleatoria = random.randint(0, 7)

	while fila_aleatoria == estado_reinas[columna_aleatoria]:
		fila_aleatoria = random.randint(0, 7)

	estado_vecino = list(estado_reinas)
	estado_vecino[columna_aleatoria] = fila_aleatoria
	ataques_vecino = calcular_ataques(estado_vecino)

	delta_energia = ataques_vecino - ataques_actuales # Si delta_e es negativo, el vecino es mejor (menos ataques). Si es positivo, el vecino es peor (más ataques).
	aceptado = False

	if delta_energia < 0:
		aceptado = True
	else:
		if temperatura_actual > 0.01:
			probabilidad = math.exp(-delta_energia / temperatura_actual)
			if random.random() < probabilidad:
				aceptado = True

	nueva_temperatura = temperatura_actual * 0.95

	estado_final = estado_vecino if aceptado else estado_reinas
	return estado_final, aceptado, nueva_temperatura


def auto_resolver_reinas(estado_inicial_reinas, algoritmo, temperatura_inicial=10.0):
	"""
	Calcula toda la secuencia de movimientos hasta encontrar la solución perfecta (0 ataques).
	reinicios aleatorios automáticos si el algoritmo se estanca.
	"""
	historial_fotogramas = []
	estado_actual = list(estado_inicial_reinas)
	temperatura_actual = temperatura_inicial
	ataques_actuales = calcular_ataques(estado_actual)

	historial_fotogramas.append((list(estado_actual), ataques_actuales, temperatura_actual))

	iteracion_actual = 0
	while ataques_actuales > 0 and iteracion_actual < 1000:
		if algoritmo == "Hill Climbing":
			estado_siguiente, hubo_mejora = ejecutar_paso_hill_climbing(estado_actual)
			if hubo_mejora:
				estado_actual = estado_siguiente
			else:
				estado_actual = [random.randint(0, 7) for _ in range(8)]

		elif algoritmo == "Recocido Simulado":
			estado_siguiente, aceptado, temperatura_actual = ejecutar_paso_recocido_simulado(estado_actual, temperatura_actual)
			estado_actual = estado_siguiente
			"""Si la temperatura es muy baja y aún no se ha encontrado la solución, se reinicia con una nueva posición aleatoria para evitar estancarse en un óptimo local."""
			if temperatura_actual < 0.001 and calcular_ataques(estado_actual) > 0:
				estado_actual = [random.randint(0, 7) for _ in range(8)]
				temperatura_actual = 10.0

		ataques_actuales = calcular_ataques(estado_actual)
		historial_fotogramas.append((list(estado_actual), ataques_actuales, temperatura_actual))
		iteracion_actual += 1

	return historial_fotogramas


def mostrar_reinas():
	st.header("8 Reinas")
	st.subheader("Búsqueda Local")
	algoritmo_seleccionado = st.radio("Selecciona el algoritmo:", ("Hill Climbing", "Recocido Simulado"), horizontal=True)

	if 'estado_tablero_reinas' not in st.session_state:
		st.session_state.estado_tablero_reinas = [0, 1, 2, 3, 4, 5, 6, 7]
	if 'temperatura_recocido_reinas' not in st.session_state:
		st.session_state.temperatura_recocido_reinas = 10.0

	contenedor_tablero = st.empty()

	def renderizar_tablero(estado_reinas, cantidad_ataques, temperatura_actual):
		color_texto = "green" if cantidad_ataques == 0 else "red"

		if algoritmo_seleccionado == "Recocido Simulado":
			html = f"### Tablero Actual | <span style='color:{color_texto}'>Ataques: {cantidad_ataques}</span> | 🌡️ Temp: {temperatura_actual:.2f}"
		else:
			html = f"### Tablero Actual | <span style='color:{color_texto}'>Ataques: {cantidad_ataques}</span>"

		html += "<br><div style='display: grid; grid-template-columns: repeat(8, 50px); width: 400px; border: 3px solid black; box-shadow: 5px 5px 15px rgba(0,0,0,0.3);'>"
		for fila_indice in range(8):
			for columna_indice in range(8):
				es_blanca = (fila_indice + columna_indice) % 2 == 0
				color_fondo = "#FFCE9E" if es_blanca else "#D18B47"
				hay_reina = estado_reinas[columna_indice] == fila_indice
				icono = "👑" if hay_reina else "&nbsp;"
				html += f"<div style='width: 50px; height: 50px; background-color: {color_fondo}; display: flex; justify-content: center; align-items: center; font-size: 32px;'>{icono}</div>"
		html += "</div><br>"
		return html

	ataques_actuales = calcular_ataques(st.session_state.estado_tablero_reinas)
	with contenedor_tablero.container():
		st.markdown(renderizar_tablero(st.session_state.estado_tablero_reinas, ataques_actuales, st.session_state.temperatura_recocido_reinas), unsafe_allow_html=True)

	st.markdown("---")
	columnas_botones = st.columns([1, 1, 1])

	with columnas_botones[0]:
		if st.button("🔀 Posición Aleatoria", key="btn_random_reinas", use_container_width=True):
			st.session_state.estado_tablero_reinas = [random.randint(0, 7) for _ in range(8)]
			st.session_state.temperatura_recocido_reinas = 10.0
			st.rerun()

	with columnas_botones[1]:
		if st.button("▶️ Ejecutar Paso", key="btn_ejecutar_paso", use_container_width=True):
			if ataques_actuales == 0:
				st.success("¡Máximo Global alcanzado! 0 ataques.")
			else:
				if algoritmo_seleccionado == "Hill Climbing":
					estado_siguiente, hubo_mejora = ejecutar_paso_hill_climbing(st.session_state.estado_tablero_reinas)
					if hubo_mejora:
						st.session_state.estado_tablero_reinas = estado_siguiente
						st.rerun()
					else:
						st.error("❌ Atascado en un Óptimo Local. Usa la posición aleatoria o el Auto-Resolver.")

				elif algoritmo_seleccionado == "Recocido Simulado":
					estado_siguiente, aceptado, nueva_temperatura = ejecutar_paso_recocido_simulado(st.session_state.estado_tablero_reinas, st.session_state.temperatura_recocido_reinas)
					st.session_state.temperatura_recocido_reinas = nueva_temperatura
					if aceptado:
						st.session_state.estado_tablero_reinas = estado_siguiente
						st.rerun()
					else:
						st.warning(f"Movimiento peor rechazado. Temperatura bajando a {nueva_temperatura:.2f}")

	with columnas_botones[2]:
		if st.button("🚀 Auto-Resolver", key="btn_auto_reinas", type="primary", use_container_width=True):
			if ataques_actuales == 0:
				st.success("El tablero ya está resuelto.")
			else:
				st.info("Calculando ruta óptima con reinicios aleatorios...")
				historial_fotogramas = auto_resolver_reinas(st.session_state.estado_tablero_reinas, algoritmo_seleccionado, st.session_state.temperatura_recocido_reinas)

				for estado_fotograma, ataques_fotograma, temperatura_fotograma in historial_fotogramas:
					with contenedor_tablero.container():
						st.markdown(renderizar_tablero(estado_fotograma, ataques_fotograma, temperatura_fotograma), unsafe_allow_html=True)
					time.sleep(0.25)

				st.session_state.estado_tablero_reinas = historial_fotogramas[-1][0]
				st.session_state.temperatura_recocido_reinas = historial_fotogramas[-1][2]
				st.balloons()
				st.success(f"¡Solución encontrada en {len(historial_fotogramas)} iteraciones!")
