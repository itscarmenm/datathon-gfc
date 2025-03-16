#- `main.py`: Archivo principal que gestiona la interacción y coordina los módulos anteriores.

if __name__ == "__main__":
    from data_loader import cargar_datos, normalizar_nombre
    from conversation import responder_pregunta

    dataframes, pacientes_dict, nombres_originales = cargar_datos()  # Cargamos los datos

    nombre_paciente_actual = None
    paciente_id_actual = None

    print("Bienvenido al asistente IA.")
    print("Se le pedirá el nombre del paciente la primera vez. Para cambiar de paciente, escriba 'otro paciente'.")

    while True:
        pregunta = input("Médico: ")
        if pregunta.lower() == "salir":
            break

        if pregunta.lower() == "otro paciente":
            nombre_paciente_actual = None
            paciente_id_actual = None
            print("Asistente IA: Por favor, ingrese el nombre del nuevo paciente.")
            continue

        if nombre_paciente_actual is None:
            nombre_paciente = input("Ingrese el nombre y apellidos del paciente: ").strip().lower()

            # Normalizar el nombre ingresado antes de buscarlo
            nombre_paciente_normalizado = normalizar_nombre(nombre_paciente)
            
            paciente_id = pacientes_dict.get(nombre_paciente_normalizado)
            if not paciente_id:
                print("Asistente IA: No se encontró un paciente con ese nombre. Inténtelo de nuevo.")
                continue
            else:
                nombre_paciente_actual = nombres_originales.get(paciente_id, nombre_paciente)
                paciente_id_actual = paciente_id
        
        if paciente_id_actual:
            respuesta = responder_pregunta(pregunta, paciente_id_actual, dataframes, pacientes_dict)
            print(f"Asistente IA: {respuesta}")
        elif nombre_paciente_actual is None:
            print("Asistente IA: Por favor, ingrese el nombre del paciente.")
