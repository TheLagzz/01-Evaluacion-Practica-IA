import streamlit as st
import math


def verificar_estado_gato(tablero):
	"""
	Evalúa si el juego terminó y devuelve la utilidad.
	MAX (X) busca +1, MIN (O) busca -1. Empate es 0.
	"""
	lineas_ganadoras = [
		[0, 1, 2], [3, 4, 5], [6, 7, 8],
		[0, 3, 6], [1, 4, 7], [2, 5, 8],
		[0, 4, 8], [2, 4, 6]
	]

	for linea in lineas_ganadoras:
		a, b, c = linea
		if tablero[a] == tablero[b] == tablero[c] and tablero[a] != ' ':
			return 1 if tablero[a] == 'X' else -1

	if ' ' not in tablero:
		return 0

	return None


def minimax_clasico(tablero, es_maximizador):
	"""Fuerza bruta: Simula todas las jugadas posibles sin cortes."""
	st.session_state.nodos_evaluados += 1
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
	st.session_state.nodos_evaluados += 1
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
				if beta <= alfa: break
		return mejor_valor
	else:
		mejor_valor = math.inf
		for i in range(9):
			if tablero[i] == ' ':
				tablero[i] = 'O'
				mejor_valor = min(mejor_valor, minimax_alfa_beta_gato(tablero, profundidad + 1, True, alfa, beta))
				tablero[i] = ' '
				beta = min(beta, mejor_valor)
				if beta <= alfa: break
		return mejor_valor


def mejor_movimiento_ia(tablero, algoritmo):
	mejor_valor = math.inf
	mejor_movimiento = -1
	st.session_state.nodos_evaluados = 0

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

	algoritmo = st.radio("Selecciona el algoritmo de la IA:", ("Minimax Clásico", "Poda Alfa-Beta"), horizontal=True)
	st.info("Juegas como MAX (X). La IA juega como MIN (O). Observa la diferencia de nodos evaluados.")

	if 'tablero_gato' not in st.session_state:
		st.session_state.tablero_gato = [' '] * 9
		st.session_state.ganador_gato = None
	if 'nodos_evaluados' not in st.session_state:
		st.session_state.nodos_evaluados = 0

	st.write(f"**Nodos evaluados en el último turno de la IA:** `{st.session_state.nodos_evaluados}`")

	st.write("### Tablero de Juego")
	cols = st.columns([1, 1, 1, 3])

	for i in range(9):
		with cols[i % 3]:
			etiqueta = st.session_state.tablero_gato[i] if st.session_state.tablero_gato[i] != ' ' else '...'
			deshabilitado = st.session_state.tablero_gato[i] != ' ' or st.session_state.ganador_gato is not None

			if st.button(etiqueta, key=f"casilla_{i}", use_container_width=True, disabled=deshabilitado):
				st.session_state.tablero_gato[i] = 'X'
				st.session_state.ganador_gato = verificar_estado_gato(st.session_state.tablero_gato)

				if st.session_state.ganador_gato is None:
					movimiento_ia = mejor_movimiento_ia(st.session_state.tablero_gato, algoritmo)
					if movimiento_ia != -1:
						st.session_state.tablero_gato[movimiento_ia] = 'O'
						st.session_state.ganador_gato = verificar_estado_gato(st.session_state.tablero_gato)

				st.rerun()

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
