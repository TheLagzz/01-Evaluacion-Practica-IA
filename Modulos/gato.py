import streamlit as st
import math


def verificar_estado_gato(tablero_juego):
	"""
	Evalúa si el juego terminó y devuelve la utilidad.
	MAX (X) busca +1, MIN (O) busca -1. Empate es 0.
	"""
	lineas_ganadoras = [
		[0, 1, 2], [3, 4, 5], [6, 7, 8],
		[0, 3, 6], [1, 4, 7], [2, 5, 8],
		[0, 4, 8], [2, 4, 6]
	]

	for linea_ganadora in lineas_ganadoras:
		indice_casilla_1, indice_casilla_2, indice_casilla_3 = linea_ganadora
		if tablero_juego[indice_casilla_1] == tablero_juego[indice_casilla_2] == tablero_juego[indice_casilla_3] and tablero_juego[indice_casilla_1] != ' ':
			return 1 if tablero_juego[indice_casilla_1] == 'X' else -1

	if ' ' not in tablero_juego:
		return 0

	return None


def minimax_clasico(tablero_juego, es_turno_maximizador):
	"""Fuerza bruta: Simula todas las jugadas posibles sin cortes."""
	st.session_state.nodos_evaluados += 1
	utilidad = verificar_estado_gato(tablero_juego)
	if utilidad is not None: return utilidad

	if es_turno_maximizador:
		valor_mejor = -math.inf
		for indice_casilla in range(9):
			if tablero_juego[indice_casilla] == ' ':
				tablero_juego[indice_casilla] = 'X'
				valor_mejor = max(valor_mejor, minimax_clasico(tablero_juego, False))
				tablero_juego[indice_casilla] = ' '
		return valor_mejor
	else:
		valor_mejor = math.inf
		for indice_casilla in range(9):
			if tablero_juego[indice_casilla] == ' ':
				tablero_juego[indice_casilla] = 'O'
				valor_mejor = min(valor_mejor, minimax_clasico(tablero_juego, True))
				tablero_juego[indice_casilla] = ' '
		return valor_mejor


def minimax_alfa_beta_gato(tablero_juego, profundidad, es_turno_maximizador, limite_inferior, limite_superior):
	"""Optimizado: Utiliza Poda Alfa-Beta para descartar ramas inútiles."""
	st.session_state.nodos_evaluados += 1
	utilidad = verificar_estado_gato(tablero_juego)

	if utilidad is not None:
		if utilidad == 1: return utilidad - (profundidad * 0.1)
		elif utilidad == -1: return utilidad + (profundidad * 0.1)
		else: return 0

	if es_turno_maximizador:
		valor_mejor = -math.inf
		for indice_casilla in range(9):
			if tablero_juego[indice_casilla] == ' ':
				tablero_juego[indice_casilla] = 'X'
				valor_mejor = max(valor_mejor, minimax_alfa_beta_gato(tablero_juego, profundidad + 1, False, limite_inferior, limite_superior))
				tablero_juego[indice_casilla] = ' '
				limite_inferior = max(limite_inferior, valor_mejor)
				if limite_superior <= limite_inferior: break
		return valor_mejor
	else:
		valor_mejor = math.inf
		for indice_casilla in range(9):
			if tablero_juego[indice_casilla] == ' ':
				tablero_juego[indice_casilla] = 'O'
				valor_mejor = min(valor_mejor, minimax_alfa_beta_gato(tablero_juego, profundidad + 1, True, limite_inferior, limite_superior))
				tablero_juego[indice_casilla] = ' '
				limite_superior = min(limite_superior, valor_mejor)
				if limite_superior <= limite_inferior: break
		return valor_mejor


def mejor_movimiento_ia(tablero_juego, algoritmo_ia):
	valor_mejor = math.inf
	mejor_movimiento = -1
	st.session_state.nodos_evaluados = 0

	for indice_casilla in range(9):
		if tablero_juego[indice_casilla] == ' ':
			tablero_juego[indice_casilla] = 'O'

			if algoritmo_ia == "Minimax Clásico":
				valor = minimax_clasico(tablero_juego, True)
			else:
				valor = minimax_alfa_beta_gato(tablero_juego, 0, True, -math.inf, math.inf)

			tablero_juego[indice_casilla] = ' '
			if valor < valor_mejor:
				valor_mejor = valor
				mejor_movimiento = indice_casilla

	return mejor_movimiento


def mostrar_gato():
	st.header("Gato / Tic-Tac-Toe")
	st.subheader("Búsqueda Adversaria")

	algoritmo_ia = st.radio("Selecciona el algoritmo de la IA:", ("Minimax Clásico", "Poda Alfa-Beta"), horizontal=True)
	st.info("Juegas como MAX (X). La IA juega como MIN (O). Observa la diferencia de nodos evaluados.")

	if 'tablero_partida_gato' not in st.session_state:
		st.session_state.tablero_partida_gato = [' '] * 9
		st.session_state.resultado_gato = None
	if 'nodos_evaluados' not in st.session_state:
		st.session_state.nodos_evaluados = 0

	st.write(f"**Nodos evaluados en el último turno de la IA:** `{st.session_state.nodos_evaluados}`")

	st.write("### Tablero de Juego")
	columnas_tablero = st.columns([1, 1, 1, 3])

	for indice_casilla in range(9):
		with columnas_tablero[indice_casilla % 3]:
			texto_casilla = st.session_state.tablero_partida_gato[indice_casilla] if st.session_state.tablero_partida_gato[indice_casilla] != ' ' else '...'
			casilla_deshabilitada = st.session_state.tablero_partida_gato[indice_casilla] != ' ' or st.session_state.resultado_gato is not None

			if st.button(texto_casilla, key=f"casilla_{indice_casilla}", use_container_width=True, disabled=casilla_deshabilitada):
				st.session_state.tablero_partida_gato[indice_casilla] = 'X'
				st.session_state.resultado_gato = verificar_estado_gato(st.session_state.tablero_partida_gato)

				if st.session_state.resultado_gato is None:
					movimiento_ia = mejor_movimiento_ia(st.session_state.tablero_partida_gato, algoritmo_ia)
					if movimiento_ia != -1:
						st.session_state.tablero_partida_gato[movimiento_ia] = 'O'
						st.session_state.resultado_gato = verificar_estado_gato(st.session_state.tablero_partida_gato)

				st.rerun()

	if st.session_state.resultado_gato is not None:
		st.markdown("---")
		if st.session_state.resultado_gato == 1:
			st.success("¡Ganaste! (Esto es imposible contra Minimax perfecto)")
		elif st.session_state.resultado_gato == -1:
			st.error("¡La IA (MIN) gana!")
		else:
			st.warning("¡Empate! (Suma Cero)")

	st.markdown("---")
	if st.button("🔄 Reiniciar Tablero", type="primary"):
		st.session_state.tablero_partida_gato = [' '] * 9
		st.session_state.resultado_gato = None
		st.session_state.nodos_evaluados = 0
		st.rerun()
