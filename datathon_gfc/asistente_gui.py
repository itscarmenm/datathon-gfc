import flet as ft
from data_loader import cargar_datos
from conversation import responder_pregunta  # Asegúrate de tener la importación correcta


class AsistenteApp(ft.Column):
    def __init__(self):
        super().__init__()
        # Cargamos los datos una vez al inicio
        self.dataframes, self.pacientes_dict, self.nombres_originales = cargar_datos()

        # Área de chat configurada para ser tipo chat
        self.chat_display = ft.ListView(expand=True, spacing=10, padding=10)

        # Caja de texto estilizada
        self.user_input = ft.TextField(
            hint_text="Escribe tu pregunta aquí...",
            expand=True,
            bgcolor=ft.colors.BLUE_GREY_800,
            color=ft.colors.WHITE
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
            self.chat_display,
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
        question = self.user_input.value
        if not question.strip():
            return

        # Agregar mensaje del médico a la derecha
        self.add_message(f"Médico: {question}", "medico")

        # Detectamos automáticamente el nombre del paciente
        nombre_paciente = question.split()[-2] + " " + question.split()[-1]
        paciente_id = self.pacientes_dict.get(nombre_paciente.lower())

        # Procesamos la respuesta de la IA
        if paciente_id:
            answer = responder_pregunta(question, paciente_id, self.dataframes, self.pacientes_dict)
        else:
            answer = f"No se encontró un paciente con el nombre '{nombre_paciente}'."

        # Agregar respuesta de la IA a la izquierda
        self.add_message(f"Asistente IA: {answer}", "ia")

        # Limpiamos el campo de entrada
        self.user_input.value = ""
        self.user_input.update()


def main(page: ft.Page):
    page.title = "Asistente Médico IA"
    page.bgcolor = ft.colors.BLUE_GREY_900

    app = AsistenteApp()
    
    # Aseguramos que la app se cargue antes de agregar los mensajes iniciales
    page.add(app)

    # Mensaje inicial después de que la página esté cargada
    app.add_message("Datos cargados correctamente.", "ia")
    
    page.update()


ft.app(target=main)
