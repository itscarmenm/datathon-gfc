if __name__ == "__main__":
    from data_loader import cargar_datos
    from conversation import responder_pregunta
    
    dataframes = cargar_datos()
    
    while True:
        pregunta = input("Médico: ")
        if pregunta.lower() == "salir":
            break
        
        try:
            paciente_id = int(input("Ingrese ID del paciente: "))
        except ValueError:
            print("ID inválido. Intente nuevamente.")
            continue
        
        respuesta = responder_pregunta(pregunta, paciente_id, dataframes)
        print(f"Asistente IA: {respuesta}")