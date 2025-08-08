import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
from datetime import date
import calendar
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from tkinter import Toplevel
from datetime import date, timedelta

#Inicializo novedades y ausencias
ausencias_novedades = []

#Funcion de selección de novedades
def abrir_calendario_ausencias():
    def agregar_rango():
        desde = date_desde.get_date()
        hasta = date_hasta.get_date()
        if desde > hasta:
            messagebox.showwarning("Rango inválido", "La fecha 'desde' no puede ser posterior a 'hasta'.")
            return

        nuevas_fechas = []
        actual = desde
        while actual <= hasta:
            if actual not in ausencias_novedades:
                ausencias_novedades.append(actual)
                nuevas_fechas.append(actual)
            actual += timedelta(days=1)

        nuevas_fechas.sort()
        for f in nuevas_fechas:
            lista_fechas.insert(tk.END, f.strftime("%d/%m/%Y"))

    def eliminar_fecha():
        seleccion = lista_fechas.curselection()
        if seleccion:
            index = seleccion[0]
            fecha_texto = lista_fechas.get(index)
            fecha = date(int(fecha_texto.split("/")[2]), int(fecha_texto.split("/")[1]), int(fecha_texto.split("/")[0]))
            ausencias_novedades.remove(fecha)
            lista_fechas.delete(index)

    ventana = Toplevel(root)
    ventana.title("Seleccionar fechas de ausencias")
    ventana.configure(bg="white")
    ventana.resizable(False, False)

    # Centrado
    ancho_ventana = 370
    alto_ventana = 420
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho_ventana / 2))
    y = int((pantalla_alto / 2) - (alto_ventana / 2))
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    tk.Frame(ventana, bg=BTN_COLOR, height=8).pack(fill="x", side="top")
    tk.Label(ventana, text="Seleccionar rango de fechas", font=TITLE_FONT, bg="white", fg=BTN_COLOR, pady=10).pack()

    frame_rango = tk.Frame(ventana, bg="white")
    frame_rango.pack(pady=5)

    # Calendario DESDE
    date_desde = DateEntry(frame_rango, width=12, style="my.DateEntry", font=FONT,
                       background="#2197e6", foreground="white", borderwidth=2,
                       headersbackground="#2197e6", headersforeground="white",
                       selectbackground="#2A9D8F", selectforeground="white")
    date_desde.pack(side="left", padx=5)

    # Calendario HASTA
    date_hasta = DateEntry(frame_rango, width=12, style="my.DateEntry", font=FONT,
                       background="#2197e6", foreground="white", borderwidth=2,
                       headersbackground="#2197e6", headersforeground="white",
                       selectbackground="#2A9D8F", selectforeground="white")
    date_hasta.pack(side="left", padx=5)

    tk.Button(ventana, text="Agregar rango", command=agregar_rango,
              bg=BTN_COLOR, fg="white", font=FONT, relief="flat", padx=10, pady=5).pack(pady=5)

    tk.Button(ventana, text="Eliminar seleccionada", command=eliminar_fecha,
              bg="#e63946", fg="white", font=FONT, relief="flat", padx=10, pady=5).pack(pady=5)

    tk.Label(ventana, text="Fechas seleccionadas:", bg="white", font=FONT_BOLD).pack(pady=(10, 0))

    lista_fechas = tk.Listbox(ventana, font=("Segoe UI", 10), height=10, bd=1, relief="solid")
    lista_fechas.pack(pady=5, padx=10, fill="both", expand=True)

    for f in sorted(ausencias_novedades):
        lista_fechas.insert(tk.END, f.strftime("%d/%m/%Y"))

    tk.Button(ventana, text="Cerrar", command=ventana.destroy,
              bg=BTN_COLOR, fg="white", font=("Segoe UI", 10),
              activebackground="#21867a", relief="flat", padx=10, pady=5).pack(pady=10)


#Filtrar ausencias validas
def filtrar_ausencias_validas(servicio, año, mes):
    dias_laborales = obtener_dias_laborales(servicio, año, mes)
    return [fecha for fecha in ausencias_novedades if fecha in dias_laborales]


# Feriados nacionales de Argentina en 2025
FERIADOS_COLES_2025 = [
    date(2025, 1, 1), date(2025, 3, 3), date(2025, 3, 4), date(2025, 3, 24),
    date(2025, 4, 2), date(2025, 4, 17), date(2025, 4, 18), date(2025, 5, 1),
    date(2025, 5, 25), date(2025, 6, 16), date(2025, 6, 20), date(2025, 7, 9),
    date(2025, 12, 8), date(2025, 12, 25)
]

FERIADOS_SUPER_2025 = [
    date(2025, 1, 1),
    date(2025, 5, 1),
    date(2025, 12, 25)
]

# Estilos
BG_COLOR = "#E6F7FF"
PANEL_COLOR = "white"
HEADER_COLOR = "#2197e6"
BTN_COLOR = "#2197e6"
FONT = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")
TITLE_FONT = ("Segoe UI", 14, "bold")

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Funciones existentes
def mostrar_resultado_personalizado(horas_realizadas, horas_teoricas):
    diferencia = horas_realizadas - horas_teoricas
    if diferencia > 0:
        mensaje_final = "✅ ¡Has realizado horas extra!\n💪 ¡Buen trabajo!"
        color = "#2A9D8F"
    elif diferencia < 0:
        mensaje_final = "⚠️ Te faltan horas por cumplir.\n⏳ Revisa tu jornada."
        color = "#E76F51"
    else:
        mensaje_final = "🎯 Has cumplido exactamente tu horario.\n✔️ ¡Perfecto!"
        color = "#264653"

    popup = Toplevel()
    popup.title("Resultado del cálculo")
    popup.configure(bg="white")
    popup.resizable(False, False)
    popup.attributes('-topmost', True)
    ancho_ventana = 370
    alto_ventana = 260
    pantalla_ancho = popup.winfo_screenwidth()
    pantalla_alto = popup.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho_ventana / 2))
    y = int((pantalla_alto / 2) - (alto_ventana / 2))
    popup.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    tk.Frame(popup, bg=color, height=8).pack(fill="x", side="top")
    tk.Label(popup, text="Resumen del mes", font=TITLE_FONT, fg=color, bg="white", pady=12).pack()

    info = (
        f"🕓 Horas realizadas:  {horas_realizadas:.2f} h\n"
        f"📘 Horas teóricas:    {horas_teoricas:.2f} h\n"
        f"📊 Diferencia:         {diferencia:+.2f} h"
    )

    tk.Label(popup, text=info, font=("Segoe UI", 11), bg="white", justify="left", padx=20).pack()
    tk.Label(popup, text=mensaje_final, font=FONT_BOLD, fg=color, bg="white", pady=12).pack()
    tk.Button(popup, text="Cerrar", command=popup.destroy, bg=color, fg="white", font=("Segoe UI", 10),
              activebackground="#21867a", relief="flat", padx=10, pady=5).pack(pady=5)

def obtener_dias_laborales(servicio, año, mes):
    dias_laborales = []
    cal = calendar.Calendar()
    for dia in cal.itermonthdates(año, mes):
        if dia.month != mes:
            continue
        if servicio in ["Supermercado", "Hospital", "Cuadrilla CA Cristina", "Predio Nuccetelli", "Cuadrilla CA Diana", "Cuadrilla CA Gustavo", "Vilaut"] and dia not in FERIADOS_SUPER_2025:
            dias_laborales.append(dia)
        elif servicio in ["Colegio", "Cuadrilla CA Dani F", "Cuadrilla EV Dani F", "Cuadrilla CA Felipe", "Cuadrilla CA Ricardo", "Puerto del águila"]:
            if dia.weekday() < 5 and dia not in FERIADOS_COLES_2025:
                dias_laborales.append(dia)
        elif servicio in ["Lunes a Sábado", "Cuadrilla CA Natalia"]:
            if dia.weekday() < 6 and dia not in FERIADOS_COLES_2025:
                dias_laborales.append(dia)
        elif servicio in ["Cuadrilla EV Diana", "FADEA"]:
            if dia.weekday() < 5 and dia not in FERIADOS_SUPER_2025:
                dias_laborales.append(dia)
    return dias_laborales

def calcular():
    try:
        horas_trabajadas = float(entry_horas.get())
        jornada_semanal = int(combo_jornada.get())

        mes = MESES.index(combo_mes.get()) + 1
        año = 2025
        servicio = combo_servicio.get()

        ausencias_validas = filtrar_ausencias_validas(servicio, año, mes)
        ausencias = len(ausencias_validas)

        dias_laborales = obtener_dias_laborales(servicio, año, mes)
        if servicio in ["Supermercado", "Cuadrilla CA Cristina", "Predio Nuccetelli", "Cuadrilla CA Diana", "Hospital", "Cuadrilla CA Gustavo"]:
            if jornada_semanal == 44:
                dias_laborales = dias_laborales[:-6]
            else:
                dias_laborales = dias_laborales[:-8]

        # Filtrar días laborales efectivos descontando ausencias
        dias_laborales_efectivos = [d for d in dias_laborales if d not in ausencias_validas]
        horas_teoricas = 0

        for dia in dias_laborales_efectivos:
            if servicio == "Lunes a Sábado" and jornada_semanal == 44:
                if dia.weekday() == 5:  # Sábado
                    horas_teoricas += 4
                else:
                    horas_teoricas += 8
            elif servicio == "Lunes a Sábado" and jornada_semanal == 34:
                if dia.weekday() == 5:  # Sábado
                    horas_teoricas += 4
                else:
                    horas_teoricas += 6
            elif servicio == "Lunes a Sábado" and jornada_semanal == 24:
                if dia.weekday() == 5:  # Sábado
                    horas_teoricas += 4
                else:
                    horas_teoricas += 4
            elif servicio == "Vilaut":
                    horas_teoricas += jornada_semanal / 7

            else:
                # Determinar horas diarias para otros servicios
                if servicio in ["Supermercado"]:
                    
                    if jornada_semanal in [40, 44]:
                        horas_diarias = 8
                    elif jornada_semanal == 30:
                        horas_diarias = 6
                    else:
                        horas_diarias = 4
                    
                elif servicio in ["Hospital", "Cuadrilla CA Cristina", "Predio Nuccetelli", "Cuadrilla CA Diana", "Cuadrilla CA Gustavo"]:
                    horas_diarias = 8 if jornada_semanal in [40, 44] else 6 if jornada_semanal == 30 else 4
                elif servicio in [ "Cuadrilla CA Natalia"]:
                    horas_diarias = 8 if jornada_semanal in [40, 44] else 6 if jornada_semanal == 30 else 4
                else:
                    horas_diarias = jornada_semanal / 5
                horas_teoricas += horas_diarias
        mostrar_resultado_personalizado(horas_trabajadas, horas_teoricas)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

        
# --- GUI ---

root = tk.Tk()
root.title("CALCULADORA DE HORAS EXTRA - KAZARÓ")
root.configure(bg=BG_COLOR)
root.resizable(False, False)
root.geometry("720x420")

# Centrado en pantalla
root.update_idletasks()
ancho = 720
alto = 420
x = (root.winfo_screenwidth() // 2) - (ancho // 2)
y = (root.winfo_screenheight() // 2) - (alto // 2)
root.geometry(f"{ancho}x{alto}+{x}+{y}")

# Encabezado
header = tk.Frame(root, bg=HEADER_COLOR, height=10)
header.pack(fill="x", side="top")

# Contenedor principal blanco
main_frame = tk.Frame(root, bg=PANEL_COLOR, padx=20, pady=20)
main_frame.place(relx=0.02, rely=0.05, relheight=0.9, relwidth=0.6)

tk.Label(main_frame, text="Calculadora de horas extra - KAZARÓ", font=TITLE_FONT,
         fg=HEADER_COLOR, bg=PANEL_COLOR, pady=5).grid(row=0, column=0, columnspan=2)

# Widgets
tk.Label(main_frame, text="Horas trabajadas:", bg=PANEL_COLOR, font=FONT_BOLD).grid(row=1, column=0, sticky="w", pady=10)
entry_horas = tk.Entry(main_frame, font=FONT, bd=2, relief="groove", width=20)
entry_horas.grid(row=1, column=1)

tk.Label(main_frame, text="Servicio:", bg=PANEL_COLOR, font=FONT_BOLD).grid(row=2, column=0, sticky="w", pady=10)
combo_servicio = ttk.Combobox(main_frame, values=[
    "Supermercado", "Colegio", "Hospital", "Lunes a Sábado",
    "Cuadrilla CA Dani F", "Cuadrilla EV Dani F", "Cuadrilla CA Cristina", "Predio Nuccetelli",
    "Cuadrilla CA Felipe", "Cuadrilla CA Ricardo", "Cuadrilla CA Diana", "Cuadrilla EV Diana",
    "Cuadrilla CA Natalia", "Cuadrilla CA Gustavo", "Puerto del águila", "FADEA", "Vilaut"
], state="readonly", font=FONT_BOLD)
combo_servicio.current(0)
combo_servicio.grid(row=2, column=1)
combo_servicio.bind("<<ComboboxSelected>>", lambda e: actualizar_francos())

tk.Label(main_frame, text="Jornada semanal (hs):", bg=PANEL_COLOR, font=FONT_BOLD).grid(row=3, column=0, sticky="w", pady=10)
combo_jornada = ttk.Combobox(main_frame, values=[20, 24, 30, 34, 36, 40, 42, 44], state="readonly", font=FONT)
combo_jornada.current(1)
combo_jornada.grid(row=3, column=1)
combo_jornada.bind("<<ComboboxSelected>>", lambda e: actualizar_francos())

tk.Label(main_frame, text="Ausencias (días):", bg=PANEL_COLOR, font=FONT_BOLD).grid(row=4, column=0, sticky="w", pady=10)
btn_ausencias = tk.Button(main_frame, text="Seleccionar fechas", command=abrir_calendario_ausencias,
                          bg="#cccccc", font=FONT, relief="flat")
btn_ausencias.grid(row=4, column=1)


tk.Label(main_frame, text="Mes:", bg=PANEL_COLOR, font=FONT_BOLD).grid(row=5, column=0, sticky="w", pady=10)
combo_mes = ttk.Combobox(main_frame, values=MESES, state="readonly", font=FONT)
combo_mes.current(0)
combo_mes.grid(row=5, column=1)

label_francos = tk.Label(main_frame, bg=PANEL_COLOR, font=FONT)
label_francos.grid(row=6, column=0, columnspan=2, sticky="w", pady=(5, 0))
label_francos.grid_remove()

btn_calcular = tk.Button(main_frame, text="Calcular", command=calcular, bg=BTN_COLOR, fg="white",
                         font=FONT, relief="flat", width=20)
btn_calcular.grid(row=7, column=0, columnspan=2, pady=15)

# Logo a la derecha
try:
    logo_img = Image.open("KZRO.png").resize((250, 250), Image.Resampling.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo_img)
    label_logo = tk.Label(root, image=logo_tk, bg=BG_COLOR)
    label_logo.place(relx=0.65, rely=0.15)
except:
    pass

def actualizar_francos():
    servicio = combo_servicio.get()
    try:
        jornada = int(combo_jornada.get())
    except ValueError:
        jornada = None

    if servicio == "Supermercado" and jornada is not None:
        texto_francos = "Corresponden 6 días de FRANCO" if jornada == 44 else "Corresponden 8 días de FRANCO"
        label_francos.config(text=texto_francos, fg="red")
        label_francos.grid()
    else:
        label_francos.grid_remove()

# Icono de ventana
try:
    icono = PhotoImage(file="KZRO.png")
    root.iconphoto(True, icono)
except:
    pass

root.mainloop()
