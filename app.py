import streamlit as st

from Modulos.frozen_lake import mostrar_frozen_lake
from Modulos.sokoban import mostrar_sokoban
from Modulos.reinas import mostrar_reinas
from Modulos.gato import mostrar_gato


st.set_page_config(page_title="IA Visualizer | ESCOM", page_icon="🧠", layout="wide")


def main():
    st.sidebar.title("Navegación")

    opcion = st.sidebar.radio(
        "Selecciona el problema a visualizar:",
        ("Inicio",
         "1. Frozen Lake (No Informada)",
         "2. Sokoban (Informada)",
         "3. 8 Reinas (Local)",
         "4. Gato (Adversaria)")
    )

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
