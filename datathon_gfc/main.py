if __name__ == "__main__":
    from data_loader import cargar_datos
    from conversation import responder_pregunta

    dataframes, pacientes_dict = cargar_datos()  # Cargamos los datos

    while True:
        pregunta = input("Médico: ")
        if pregunta.lower() == "salir":
            break
        
        nombre_paciente = input("Ingrese el nombre y apellidos del paciente: ").strip().lower()
        
        paciente_id = pacientes_dict.get(nombre_paciente)
        if not paciente_id:
            print("Asistente IA: No se encontró un paciente con ese nombre. Inténtelo de nuevo.")
            continue

        respuesta = responder_pregunta(pregunta, paciente_id, dataframes)
        print(f"Asistente IA: {respuesta}")
