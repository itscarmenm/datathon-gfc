import flet as ft
from data_loader import cargar_datos
from conversation import responder_pregunta, normalizar_nombre

class AsistenteApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.dataframes, self.pacientes_dict, self.nombres_originales = cargar_datos()
        # Variable para guardar el paciente actual de la conversación
        self.current_patient = None

        # Área de chat con desplazamiento habilitado manualmente
        self.chat_display = ft.ListView(
            expand=True, spacing=10, padding=10, auto_scroll=True
        )

        # Caja de texto estilizada
        self.user_input = ft.TextField(
            hint_text="Escribe tu pregunta aquí...",
            expand=True,
            bgcolor=ft.Colors.BLUE_GREY_800,
            color=ft.Colors.WHITE,
            on_submit=self.handle_send
        )

        # Botón destacado
        self.send_button = ft.ElevatedButton(
            "Enviar",
            on_click=self.handle_send,
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE
        )

        # Estructura de la app
        self.controls = [
            ft.Container(
                content=self.chat_display,
                expand=True,
                border_radius=ft.border_radius.all(10),
                border=ft.border.all(1, ft.Colors.GREY_700),
                padding=10,
                height=400,  # 📌 Tamaño fijo para permitir el scroll
            ),
            ft.Row(controls=[self.user_input, self.send_button]),
        ]

    def extraer_nombre_paciente(self, question: str):
        """
        Intenta extraer el nombre del paciente asumiendo que se encuentran
        en las dos últimas palabras de la pregunta. Si se encuentra y es válido,
        se devuelve el nombre normalizado; de lo contrario, se retorna None.
        """
        palabras = question.split()
        if len(palabras) >= 2:
            candidato = palabras[-2] + " " + palabras[-1]
            candidato_norm = normalizar_nombre(candidato)
            if candidato_norm in self.pacientes_dict:
                return candidato_norm
        return None

    def add_message(self, message, sender):
        """Agrega mensajes al chat, alineados según quién lo envía."""
        if sender == "medico":
            msg = ft.Container(
                content=ft.Text(message, color=ft.Colors.WHITE, size=14),
                alignment=ft.alignment.center_right,
                bgcolor=ft.Colors.BLUE_700,
                padding=10,
                border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15),
                margin=ft.margin.only(left=50)
            )
        else:  # Mensaje de la IA
            msg = ft.Container(
                content=ft.Text(message, color=ft.Colors.BLACK, size=14),
                alignment=ft.alignment.center_left,
                bgcolor=ft.Colors.LIGHT_BLUE_100,
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
            content=ft.Text("Florence está pensando...", color=ft.Colors.GREY_500, italic=True),
            alignment=ft.alignment.center_left,
            bgcolor=ft.Colors.GREY_300,
            padding=10,
            border_radius=ft.border_radius.all(10),
            margin=ft.margin.only(right=50)
        )
        self.chat_display.controls.append(loading_msg)
        self.chat_display.update()

        # Intentar extraer un nuevo nombre de paciente de la pregunta
        nombre_detectado = self.extraer_nombre_paciente(question)
        if nombre_detectado:
            # Se actualiza el paciente actual
            self.current_patient = nombre_detectado
            paciente_id = self.pacientes_dict[nombre_detectado]
        else:
            # Si no se detecta un nombre, se usa el paciente actual del contexto
            if self.current_patient:
                paciente_id = self.pacientes_dict[self.current_patient]
            else:
                paciente_id = None

        # Procesar respuesta basándonos en el paciente identificado
        if paciente_id:
            answer = responder_pregunta(question, paciente_id, self.dataframes, self.pacientes_dict)
        else:
            answer = "No se encontró un paciente en el contexto. Por favor, menciona el nombre del paciente (por ejemplo, 'juan perez')."

        # Eliminar el mensaje de "Cargando..."
        self.chat_display.controls.remove(loading_msg)
        self.chat_display.update()

        # Agregar respuesta de la IA
        self.add_message(f"Florence {answer}", "ia")

        # Limpiar la caja de texto
        self.user_input.value = ""
        self.user_input.update()


def main(page: ft.Page):
    page.title = "Florence - Asistente Virtual Médico"
    page.bgcolor = ft.Colors.BLUE_GREY_900

    app = AsistenteApp()

    page.add(app)

    # Mensaje inicial
    app.add_message("Bienvenidx a Florence, tu asistente virtual médica. Puedes consultar datos de un paciente mencionando su nombre, y luego seguir haciendo preguntas sin repetirlo.", "ia")

    page.update()


ft.app(target=main)
