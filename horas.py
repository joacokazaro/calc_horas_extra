import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
from datetime import date
import calendar
from PIL import Image, ImageTk
from tkinter import Toplevel
# Feriados nacionales de Argentina en 2025
FERIADOS_COLES_2025 = [
    date(2025, 1, 1), date(2025, 3, 3), date(2025, 3, 4), date(2025, 3, 24),
    date(2025, 4, 2), date(2025, 4, 17), date(2025, 4, 18), date(2025, 5, 1),
    date(2025, 5, 25), date(2025, 6, 20), date(2025, 7, 9),
    date(2025, 12, 8), date(2025, 12, 25)
]

FERIADOS_SUPER_2025 = [
    date(2025, 1, 1), date(2025, 3, 3), date(2025, 3, 4), date(2025, 3, 24),
    date(2025, 4, 2), date(2025, 4, 18), date(2025, 5, 1), date(2025, 6, 20), date(2025, 7, 9),
    date(2025, 12, 8), date(2025, 12, 25)
]

# Estilos
BG_COLOR = "#E6F7FF"  # Celeste suave
BTN_COLOR = "#2197e6"
FONT = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

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

    # Crear ventana emergente
    popup = Toplevel()
    popup.title("Resultado del cálculo")
    popup.configure(bg="white")
    popup.resizable(False, False)
    popup.attributes('-topmost', True)  # Siempre visible

    # Centrar ventana
    ancho_ventana = 370
    alto_ventana = 260
    pantalla_ancho = popup.winfo_screenwidth()
    pantalla_alto = popup.winfo_screenheight()
    x = int((pantalla_ancho / 2) - (ancho_ventana / 2))
    y = int((pantalla_alto / 2) - (alto_ventana / 2))
    popup.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    # Encabezado de color
    marco = tk.Frame(popup, bg=color, height=8)
    marco.pack(fill="x", side="top")

    # Título
    tk.Label(popup, text="Resumen del mes", font=("Segoe UI", 14, "bold"),
             fg=color, bg="white", pady=12).pack()

    # Datos
    info = (
        f"🕓 Horas realizadas:  {horas_realizadas:.2f} h\n"
        f"📘 Horas teóricas:    {horas_teoricas:.2f} h\n"
        f"📊 Diferencia:         {diferencia:+.2f} h"
    )

    tk.Label(popup, text=info, font=("Segoe UI", 11),
             bg="white", justify="left", padx=20).pack()

    # Mensaje final
    tk.Label(popup, text=mensaje_final, font=("Segoe UI", 12, "bold"),
             fg=color, bg="white", pady=12).pack()

    # Botón cerrar
    tk.Button(popup, text="Cerrar", command=popup.destroy,
              bg=color, fg="white", font=("Segoe UI", 10),
              activebackground="#21867a", relief="flat", padx=10, pady=5).pack(pady=5)

def obtener_dias_laborales(servicio, año, mes):
    dias_laborales = []
    cal = calendar.Calendar()
    for dia in cal.itermonthdates(año, mes):
        if dia.month != mes:
            continue
        if servicio in ["Supermercado", "Hospital", "Cuadrilla CA Cristina", "Predio Nuccetelli", "Cuadrilla CA Diana", "Cuadrilla CA Gustavo"] and dia not in FERIADOS_SUPER_2025:
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
        ausencias = int(entry_ausencias.get())
        mes = MESES.index(combo_mes.get()) + 1
        año = 2025
        servicio = combo_servicio.get()

        dias_laborales = obtener_dias_laborales(servicio, año, mes)

        if servicio in ["Supermercado", "Cuadrilla CA Cristina", "Predio Nuccetelli", "Cuadrilla CA Diana", "Hospital", "Cuadrilla CA Gustavo"]:
            if jornada_semanal == 44:
                dias_laborales = dias_laborales[:-6]  # 6 francos
            else:
                dias_laborales = dias_laborales[:-8] # 8 francos 

        dias_laborales_teoricos = len(dias_laborales) - ausencias
        if servicio in ["Supermercado", "Hospital", "Cuadrilla CA Cristina", "Predio Nuccetelli", "Cuadrilla CA Diana", "Cuadrilla CA Gustavo"]:
            if jornada_semanal == 44 or jornada_semanal == 40:
                horas_diarias = 8
            elif jornada_semanal == 30:
                horas_diarias = 6
            elif jornada_semanal == 20:
                horas_diarias = 4
        elif servicio in ["Lunes a Sábado", "Cuadrilla CA Natalia"]:
            if jornada_semanal == 44 or jornada_semanal == 40:
                horas_diarias = 8
            elif jornada_semanal == 30:
                horas_diarias = 6
            elif jornada_semanal == 20:
                horas_diarias = 4
        else:
            horas_diarias = jornada_semanal / 5  # Suponiendo 5 días por semana
        horas_teoricas = dias_laborales_teoricos * horas_diarias
        
        

        mostrar_resultado_personalizado(horas_trabajadas, horas_teoricas)


    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

# GUI
root = tk.Tk()
root.title("Calculadora de horas extra - KAZARÓ")
root.configure(bg=BG_COLOR)

frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=20)
frame.pack(side="left", fill="y", expand=True)

# Logo a la derecha
try:
    logo_img = Image.open("KZRO.png")
    logo_img = logo_img.resize((300,300 ), Image.Resampling.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo_img)
    label_logo = tk.Label(root, image=logo_tk, bg=BG_COLOR)
    label_logo.pack(side="right", padx=20, pady=20)
except:
    pass  # Si no hay logo, que no crashee

# Función para actualizar la etiqueta de francos
def actualizar_francos(*args):
    servicio = combo_servicio.get()
    try:
        jornada = int(combo_jornada.get())
    except ValueError:
        jornada = None

    if servicio == "Supermercado" and jornada is not None:
        if jornada == 44:
            texto_francos = "Corresponden 6 días de FRANCO"
        else:
            texto_francos = "Corresponden 8 días de FRANCO"
        label_francos.config(text=texto_francos, fg="red")
        label_francos.grid(row=5, column=0, columnspan=2, sticky="w", pady=(5, 0))
    else:
        label_francos.grid_remove()

# Widgets
tk.Label(frame, text="Horas trabajadas:", bg=BG_COLOR, font=FONT_BOLD).grid(row=0, column=0, sticky="w", pady=10)
entry_horas = tk.Entry(frame, font=FONT, bd=2, relief="groove", width=20)
entry_horas.grid(row=0, column=1)

tk.Label(frame, text="Servicio:", bg=BG_COLOR, font=FONT_BOLD).grid(row=1, column=0, sticky="w", pady=10)
combo_servicio = ttk.Combobox(frame, values=
                              ["Supermercado",
                                "Colegio",
                                "Hospital",
                                "Lunes a Sábado",
                                "Cuadrilla CA Dani F",
                                "Cuadrilla EV Dani F",
                                "Cuadrilla CA Cristina",
                                "Predio Nuccetelli",
                                "Cuadrilla CA Felipe",
                                "Cuadrilla CA Ricardo",
                                "Cuadrilla CA Diana",
                                "Cuadrilla EV Diana",
                                "Cuadrilla CA Natalia",
                                "Cuadrilla CA Gustavo",
                                "Puerto del águila",
                                "FADEA"]#Listado de servicios
                              , state="readonly", font=FONT_BOLD)
combo_servicio.current(0)
combo_servicio.grid(row=1, column=1)
combo_servicio.bind("<<ComboboxSelected>>", actualizar_francos)

tk.Label(frame, text="Jornada semanal (hs):", bg=BG_COLOR, font=FONT_BOLD).grid(row=2, column=0, sticky="w", pady=10)
combo_jornada = ttk.Combobox(frame, values=[20, 30, 40, 42, 44], state="readonly", font=FONT)
combo_jornada.current(1)
combo_jornada.grid(row=2, column=1)
combo_jornada.bind("<<ComboboxSelected>>", actualizar_francos)

tk.Label(frame, text="Ausencias (días):", bg=BG_COLOR, font=FONT_BOLD).grid(row=3, column=0, sticky="w", pady=10)
entry_ausencias = tk.Entry(frame, font=FONT, bd=2, relief="groove", width=20)
entry_ausencias.insert(0, "0")
entry_ausencias.grid(row=3, column=1)

tk.Label(frame, text="Mes:", bg=BG_COLOR, font=FONT_BOLD).grid(row=4, column=0, sticky="w", pady=10)
combo_mes = ttk.Combobox(frame, values=MESES, state="readonly", font=FONT)
combo_mes.current(0)
combo_mes.grid(row=4, column=1)

label_francos = tk.Label(frame, bg=BG_COLOR, font=FONT)
label_francos.grid(row=5, column=0, columnspan=2, sticky="w", pady=(5, 0))
label_francos.grid_remove()

btn_calcular = tk.Button(frame, text="Calcular", command=calcular, bg=BTN_COLOR, fg="white", font=FONT, relief="flat", width=20)
btn_calcular.grid(row=6, column=0, columnspan=2, pady=15)

icono = PhotoImage(file="KZRO.png")
root.iconphoto(True, icono)

root.mainloop()
