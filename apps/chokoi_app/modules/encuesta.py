import streamlit as st
import pandas as pd
import secrets
import re

from modules.database import engine


# =====================================================
# LIMPIEZA PRECIO
# =====================================================

def limpiar_precio(valor):

    if pd.isna(valor):

        return None

    valor = str(valor)

    valor = valor.replace("$", "")
    valor = valor.replace(",", "")
    valor = valor.replace("mxn", "")
    valor = valor.replace("MXN", "")

    valor = valor.strip()

    numeros = re.findall(r"\d+\.?\d*", valor)

    if len(numeros) == 0:

        return None

    return float(numeros[0])


# =====================================================
# REGISTRO
# =====================================================

def mostrar_registro():

    st.header("Registro de productor")

    with st.form("registro_productor"):

        # =============================================
        # PRODUCTOR
        # =============================================

        nombre = st.text_input(
            "Nombre del productor o emprendimiento"
        )

        ubicacion = st.text_input(
            "Ubicación"
        )

        celular = st.text_input(
            "Celular"
        )

        redes = st.text_input(
            "Redes sociales"
        )

        email = st.text_input(
            "Correo electrónico (privado)"
        )

        # =============================================
        # PRODUCTOS
        # =============================================

        st.subheader("Productos")

        st.caption(
            """
            Puedes agregar varios productos.
            El precio debe estar en MXN.
            """
        )

        productos_df = st.data_editor(

            pd.DataFrame(
                columns=[
                    "producto",
                    "precio",
                    "unidad"
                ]
            ),

            num_rows="dynamic",
            use_container_width=True
        )

        enviado = st.form_submit_button(
            "Registrar productor"
        )

    # =================================================
    # VALIDACIONES
    # =================================================

    if enviado:

        # =============================================
        # VALIDAR PRODUCTOR
        # =============================================

        if nombre.strip() == "":

            st.error(
                "El nombre del productor es obligatorio."
            )

            return

        if email.strip() == "":

            st.error(
                "El correo electrónico es obligatorio."
            )

            return

        # =============================================
        # VALIDAR PRODUCTOS
        # =============================================

        productos_limpios = []

        for _, row in productos_df.iterrows():

            producto = str(row["producto"]).strip()

            precio = limpiar_precio(
                row["precio"]
            )

            unidad = str(row["unidad"]).strip()

            # -----------------------------------------
            # IGNORAR FILAS VACÍAS
            # -----------------------------------------

            if (
                producto == ""
                and unidad == ""
                and precio is None
            ):

                continue

            # -----------------------------------------
            # VALIDAR CAMPOS
            # -----------------------------------------

            if producto == "":

                st.error(
                    "Todos los productos deben tener nombre."
                )

                return

            if precio is None:

                st.error(
                    f"Precio inválido para '{producto}'."
                )

                return

            if unidad == "":

                st.error(
                    f"Falta unidad para '{producto}'."
                )

                return

            productos_limpios.append({

                "producto": producto,
                "precio": precio,
                "unidad": unidad

            })

        # =============================================
        # VALIDAR AL MENOS UN PRODUCTO
        # =============================================

        if len(productos_limpios) == 0:

            st.error(
                "Debes registrar al menos un producto."
            )

            return

        # =============================================
        # TOKEN
        # =============================================

        edit_token = secrets.token_urlsafe(32)

        # =============================================
        # PRODUCTOR DF
        # =============================================

        productor_df = pd.DataFrame([{

            "nombre": nombre,
            "ubicacion": ubicacion,
            "celular": celular,
            "redes": redes,
            "email": email,
            "edit_token": edit_token

        }])

        # =============================================
        # INSERT PRODUCTOR
        # =============================================

        productor_df.to_sql(

            "productores",
            engine,
            if_exists="append",
            index=False

        )

        # =============================================
        # OBTENER ID
        # =============================================

        productor_id = pd.read_sql(

            "SELECT MAX(id) as id FROM productores",
            engine

        )["id"][0]

        # =============================================
        # PRODUCTOS DF
        # =============================================

        productos_final = pd.DataFrame(
            productos_limpios
        )

        productos_final["productor_id"] = productor_id

        # =============================================
        # INSERT PRODUCTOS
        # =============================================

        productos_final.to_sql(

            "productos",
            engine,
            if_exists="append",
            index=False

        )

        # =============================================
        # SUCCESS
        # =============================================

        st.success(
            "Productor registrado correctamente."
        )

        st.info(
            """
            Próximamente podrás editar
            tu información mediante correo electrónico.
            """
        )

