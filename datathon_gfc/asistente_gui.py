import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from data_loader import cargar_datos
from conversation import responder_pregunta, normalizar_nombre, generar_grafico_laboratorio

class AsistenteApp(ft.Column):
    def __init__(self):
        super().__init__(expand=True)

        self.dataframes, self.pacientes_dict, self.nombres_originales = cargar_datos()
        self.current_patient = None  

        self.chat_display = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
            auto_scroll=True
        )

        self.user_input = ft.TextField(
            hint_text="Escribe tu pregunta aquí...",
            expand=True,
            bgcolor=ft.Colors.BLUE_GREY_800,
            color=ft.Colors.WHITE,
            on_submit=self.handle_send
        )

        self.send_button = ft.ElevatedButton(
            "Enviar",
            on_click=self.handle_send,
            bgcolor=ft.Colors.BLUE_500,
            color=ft.Colors.WHITE
        )

        self.controls = [
            ft.Container(
                content=self.chat_display,
                expand=True,
                border_radius=ft.border_radius.all(10),
                border=ft.border.all(1, ft.Colors.GREY_700),
                padding=10,
            ),
            ft.Row(controls=[self.user_input, self.send_button]),
        ]

    def extraer_nombre_paciente(self, question: str):
        palabras = question.split()
        if len(palabras) >= 2:
            candidato = palabras[-2] + " " + palabras[-1]
            candidato_norm = normalizar_nombre(candidato)
            if candidato_norm in self.pacientes_dict:
                return candidato_norm
        return None

    def add_message(self, message, sender):
        if sender == "medico":
            msg = ft.Container(
                content=ft.Text(message, color=ft.Colors.WHITE, size=14),
                alignment=ft.alignment.center_right,
                bgcolor=ft.Colors.BLUE_700,
                padding=10,
                border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15),
                margin=ft.margin.only(left=50)
            )
        else:  
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

        if question.lower() == "otro paciente":
            self.current_patient = None
            self.add_message("Florence: Listo, ahora indícame el nombre del nuevo paciente.", "ia")
            self.user_input.value = ""
            self.user_input.update()
            return

        self.add_message(f"Médico: {question}", "medico")

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

        nombre_detectado = self.extraer_nombre_paciente(question)
        if nombre_detectado:
            self.current_patient = nombre_detectado
            paciente_id = self.pacientes_dict[nombre_detectado]
        else:
            paciente_id = self.pacientes_dict.get(self.current_patient, None)

        if any(word in question.lower() for word in ["gráfica", "grafica"]) and paciente_id:
            chart = generar_grafico_laboratorio(self.dataframes, paciente_id)
            if chart:
                self.chat_display.controls.append(
                    ft.Row(  # 👈 Usamos Row para alinear a la izquierda
                        [
                            ft.Container(
                                content=chart,
                                width=500,  # 👈 Reduce el ancho para que no ocupe todo
                                height=350,  # 👈 Ajusta el alto si es necesario
                                bgcolor=ft.Colors.LIGHT_BLUE_100,
                                padding=10,
                                border_radius=ft.border_radius.all(10),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START,  # 👈 Asegura que quede a la izquierda
                    )
                )
                self.chat_display.update()
                answer = "Aquí tienes la gráfica de laboratorio del paciente."
            else:
                answer = "No se encontraron datos de laboratorio para este paciente."
        elif paciente_id:
            answer = responder_pregunta(question, paciente_id, self.dataframes, self.pacientes_dict)
        else:
            answer = "No se encontró un paciente en el contexto. Por favor, menciona el nombre del paciente."

        self.chat_display.controls.remove(loading_msg)
        self.chat_display.update()
        self.add_message(f"Florence: {answer}", "ia")

        self.user_input.value = ""
        self.user_input.update()


def main(page: ft.Page):
    page.title = "Florence - Asistente Virtual Médico"
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.vertical_alignment = "stretch"
    page.horizontal_alignment = "stretch"

    app = AsistenteApp()
    page.add(app)

    app.add_message(
        "Bienvenidx a Florence, tu asistente médica virtual 😊. "
        "Puedes consultar datos de un paciente mencionando su nombre!🩺", 
        "ia"
    )

    page.update()


ft.app(target=main)
