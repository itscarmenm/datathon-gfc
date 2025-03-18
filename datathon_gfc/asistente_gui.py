import flet as ft
from data_loader import cargar_datos
from conversation import responder_pregunta, normalizar_nombre


class AsistenteApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.dataframes, self.pacientes_dict, self.nombres_originales = cargar_datos()

        # Área de chat con desplazamiento
        self.chat_display = ft.ListView(expand=True, spacing=10, padding=10, auto_scroll=True)

        # Caja de texto estilizada
        self.user_input = ft.TextField(
            hint_text="Escribe tu pregunta aquí...",
            expand=True,
            bgcolor=ft.colors.BLUE_GREY_800,
            color=ft.colors.WHITE,
            on_submit=self.handle_send  # Permite enviar con "Enter"
        )

        # Botón destacado
        self.send_button = ft.ElevatedButton(
            "Enviar",
            on_click=self.handle_send,
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE
        )

        # Estructura de la app
        self.controls = [
            ft.Container(
                content=self.chat_display,
                expand=True,
                border_radius=ft.border_radius.all(10),
                border=ft.border.all(1, ft.colors.GREY_700),
                padding=10
            ),
            ft.Row(controls=[self.user_input, self.send_button]),
        ]

    def add_message(self, message, sender):
        """ Agrega mensajes al chat, alineados según quién lo envía. """
        if sender == "medico":
            msg = ft.Container(
                content=ft.Text(message, color=ft.colors.WHITE, size=14),
                alignment=ft.alignment.center_right,
                bgcolor=ft.colors.BLUE_700,
                padding=10,
                border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15),
                margin=ft.margin.only(left=50)
            )
        else:  # Mensaje de la IA
            msg = ft.Container(
                content=ft.Text(message, color=ft.colors.BLACK, size=14),
                alignment=ft.alignment.center_left,
                bgcolor=ft.colors.LIGHT_BLUE_100,
                padding=10,
                border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15),
                margin=ft.margin.only(right=50)
            )
        self.chat_display.controls.append(msg)
        self.chat_display.update()

    def handle_send(self, e):
        question = self.user_input.value.strip()
        if not question:
            return

        # Agregar mensaje del médico
        self.add_message(f"Médico: {question}", "medico")

        # Mostrar mensaje de "Cargando..."
        loading_msg = ft.Container(
            content=ft.Text("Asistente IA está procesando...", color=ft.colors.GREY_500, italic=True),
            alignment=ft.alignment.center_left,
            bgcolor=ft.colors.GREY_300,
            padding=10,
            border_radius=ft.border_radius.all(10),
            margin=ft.margin.only(right=50)
        )
        self.chat_display.controls.append(loading_msg)
        self.chat_display.update()

        # Detectar paciente y procesar respuesta
        nombre_paciente = question.split()[-2] + " " + question.split()[-1]
        nombre_paciente_normalizado = normalizar_nombre(nombre_paciente)
        paciente_id = self.pacientes_dict.get(nombre_paciente_normalizado)

        answer = responder_pregunta(question, paciente_id, self.dataframes, self.pacientes_dict) if paciente_id else f"No se encontró un paciente con el nombre '{nombre_paciente}'."

        # Eliminar el mensaje de "Cargando..."
        self.chat_display.controls.remove(loading_msg)
        self.chat_display.update()

        # Agregar respuesta de la IA
        self.add_message(f"Asistente IA: {answer}", "ia")

        # Limpiar la caja de texto
        self.user_input.value = ""
        self.user_input.update()


def main(page: ft.Page):
    page.title = "Asistente Médico IA"
    page.bgcolor = ft.colors.BLUE_GREY_900

    app = AsistenteApp()

    page.add(app)

    # Mensaje inicial
    app.add_message("Datos cargados correctamente.", "ia")

    page.update()


ft.app(target=main)
