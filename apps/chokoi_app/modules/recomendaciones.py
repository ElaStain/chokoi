import streamlit as st
import pandas as pd

from modules.database import engine

def mostrar_directorio():

    st.header("Explorar productores")

    query = """

    SELECT

        p.nombre,
        p.ubicacion,
        p.celular,
        p.redes,

        pr.producto,
        pr.precio,
        pr.unidad

    FROM productores p

    JOIN productos pr
    ON p.id = pr.productor_id

    """

    df = pd.read_sql(query, engine)

    if len(df) == 0:

        st.warning(
            "Aún no hay productores registrados"
        )

        return

    busqueda = st.text_input(
        "Buscar producto o ubicación"
    )

    if busqueda != "":

        df = df[

            df["producto"]
            .str.contains(
                busqueda,
                case=False,
                na=False
            )

            |

            df["ubicacion"]
            .str.contains(
                busqueda,
                case=False,
                na=False
            )
        ]

    for _, row in df.iterrows():

        with st.container(border=True):

            st.subheader(row["nombre"])

            st.write(
                f"📍 {row['ubicacion']}"
            )

            st.write(
                f"🍫 {row['producto']}"
            )

            st.write(
                f"💰 ${row['precio']} MXN / {row['unidad']}"
            )

            st.write(
                f"📞 {row['celular']}"
            )

            if row["redes"] != "":

                st.write(
                    f"🌐 {row['redes']}"
                )

            st.button(
                "Editar información",
                disabled=True
            )

            st.caption(
                "La edición por correo estará disponible próximamente."
            )
