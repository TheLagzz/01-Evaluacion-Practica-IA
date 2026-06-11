import streamlit as st
import random
import math
import time


def calcular_ataques(estado):
	"""
	Calcula cuántos pares de reinas se están atacando.
	Un estado perfecto devolverá 0.
	"""
	ataques = 0
	for i in range(8):
		for j in range(i + 1, 8):
			if estado[i] == estado[j]:
				ataques += 1
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

	for col in range(8):
		for fila in range(8):
			if fila != estado[col]:
				vecino = list(estado)
				vecino[col] = fila
				ataques_vecino = calcular_ataques(vecino)

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

	col_random = random.randint(0, 7)
	fila_random = random.randint(0, 7)

	while fila_random == estado[col_random]:
		fila_random = random.randint(0, 7)

	vecino = list(estado)
	vecino[col_random] = fila_random
	ataque_vecino = calcular_ataques(vecino)

	delta_e = ataque_vecino - ataque_actual
	aceptado = False

	if delta_e < 0:
		aceptado = True
	else:
		if temperatura > 0.01:
			probabilidad = math.exp(-delta_e / temperatura)
			if random.random() < probabilidad:
				aceptado = True

	nueva_temperatura = temperatura * 0.95

	estado_final = vecino if aceptado else estado
	return estado_final, aceptado, nueva_temperatura


def auto_resolver_reinas(estado_inicial, algoritmo, temp_inicial=10.0):
	"""
	Calcula toda la secuencia de movimientos hasta encontrar la solución perfecta (0 ataques).
	Incluye reinicios aleatorios automáticos si el algoritmo se estanca.
	"""
	historial = []
	estado_actual = list(estado_inicial)
	temp = temp_inicial
	ataques = calcular_ataques(estado_actual)

	historial.append((list(estado_actual), ataques, temp))

	iteracion = 0
	while ataques > 0 and iteracion < 1000:
		if algoritmo == "Hill Climbing":
			nuevo_estado, mejoro = ejecutar_paso_hill_climbing(estado_actual)
			if mejoro:
				estado_actual = nuevo_estado
			else:
				estado_actual = [random.randint(0, 7) for _ in range(8)]

		elif algoritmo == "Recocido Simulado":
			nuevo_estado, aceptado, temp = ejecutar_paso_recocido_simulado(estado_actual, temp)
			estado_actual = nuevo_estado
			if temp < 0.001 and calcular_ataques(estado_actual) > 0:
				estado_actual = [random.randint(0, 7) for _ in range(8)]
				temp = 10.0

		ataques = calcular_ataques(estado_actual)
		historial.append((list(estado_actual), ataques, temp))
		iteracion += 1

	return historial


def mostrar_reinas():
	st.header("8 Reinas")
	st.subheader("Búsqueda Local")
	algoritmo = st.radio("Selecciona el algoritmo:", ("Hill Climbing", "Recocido Simulado"), horizontal=True)

	if 'estado_reinas' not in st.session_state:
		st.session_state.estado_reinas = [0, 1, 2, 3, 4, 5, 6, 7]
	if 'temperatura' not in st.session_state:
		st.session_state.temperatura = 10.0

	contenedor_tablero = st.empty()

	def renderizar_tablero(estado, ataques, temp):
		color_texto = "green" if ataques == 0 else "red"

		if algoritmo == "Recocido Simulado":
			html = f"### Tablero Actual | <span style='color:{color_texto}'>Ataques: {ataques}</span> | 🌡️ Temp: {temp:.2f}"
		else:
			html = f"### Tablero Actual | <span style='color:{color_texto}'>Ataques: {ataques}</span>"

		html += "<br><div style='display: grid; grid-template-columns: repeat(8, 50px); width: 400px; border: 3px solid black; box-shadow: 5px 5px 15px rgba(0,0,0,0.3);'>"
		for fila in range(8):
			for col in range(8):
				es_blanca = (fila + col) % 2 == 0
				color_fondo = "#FFCE9E" if es_blanca else "#D18B47"
				hay_reina = estado[col] == fila
				icono = "👑" if hay_reina else "&nbsp;"
				html += f"<div style='width: 50px; height: 50px; background-color: {color_fondo}; display: flex; justify-content: center; align-items: center; font-size: 32px;'>{icono}</div>"
		html += "</div><br>"
		return html

	ataques_actuales = calcular_ataques(st.session_state.estado_reinas)
	with contenedor_tablero.container():
		st.markdown(renderizar_tablero(st.session_state.estado_reinas, ataques_actuales, st.session_state.temperatura), unsafe_allow_html=True)

	st.markdown("---")
	cols = st.columns([1, 1, 1])

	with cols[0]:
		if st.button("🔀 Posición Aleatoria", key="btn_random_reinas", use_container_width=True):
			st.session_state.estado_reinas = [random.randint(0, 7) for _ in range(8)]
			st.session_state.temperatura = 10.0
			st.rerun()

	with cols[1]:
		if st.button("▶️ Ejecutar Paso", key="btn_ejecutar_paso", use_container_width=True):
			if ataques_actuales == 0:
				st.success("¡Máximo Global alcanzado! 0 ataques.")
			else:
				if algoritmo == "Hill Climbing":
					nuevo_estado, mejoro = ejecutar_paso_hill_climbing(st.session_state.estado_reinas)
					if mejoro:
						st.session_state.estado_reinas = nuevo_estado
						st.rerun()
					else:
						st.error("❌ Atascado en un Óptimo Local. Usa la posición aleatoria o el Auto-Resolver.")

				elif algoritmo == "Recocido Simulado":
					nuevo_estado, aceptado, nueva_temp = ejecutar_paso_recocido_simulado(st.session_state.estado_reinas, st.session_state.temperatura)
					st.session_state.temperatura = nueva_temp
					if aceptado:
						st.session_state.estado_reinas = nuevo_estado
						st.rerun()
					else:
						st.warning(f"Movimiento peor rechazado. Temperatura bajando a {nueva_temp:.2f}")

	with cols[2]:
		if st.button("🚀 Auto-Resolver", key="btn_auto_reinas", type="primary", use_container_width=True):
			if ataques_actuales == 0:
				st.success("El tablero ya está resuelto.")
			else:
				st.info("Calculando ruta óptima con reinicios aleatorios...")
				historial_fotogramas = auto_resolver_reinas(st.session_state.estado_reinas, algoritmo, st.session_state.temperatura)

				for estado_fotograma, ataques_fotograma, temp_fotograma in historial_fotogramas:
					with contenedor_tablero.container():
						st.markdown(renderizar_tablero(estado_fotograma, ataques_fotograma, temp_fotograma), unsafe_allow_html=True)
					time.sleep(0.25)

				st.session_state.estado_reinas = historial_fotogramas[-1][0]
				st.session_state.temperatura = historial_fotogramas[-1][2]
				st.balloons()
				st.success(f"¡Solución encontrada en {len(historial_fotogramas)} iteraciones!")
