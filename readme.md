# 🕓 Calculadora de Horas Extra – Kazaró

## 📌 Descripción
Aplicación de escritorio desarrollada en **Python** con **Tkinter** que calcula automáticamente las horas extra realizadas por un colaborador en un mes.  
El cálculo considera:
- Horas trabajadas.
- Servicio asignado.
- Tipo de contrato (jornada semanal).
- Ausencias registradas.
- Feriados nacionales (dependiendo del servicio).

Este sistema reemplaza el cálculo manual, reduciendo errores y agilizando el proceso.

---

## 🚀 Características
- Interfaz gráfica intuitiva.
- Selección de ausencias mediante calendario.
- Mensajes motivacionales o de advertencia según el resultado.
- Adaptación de cálculo según el servicio y jornada semanal.
- Soporte para diferentes esquemas laborales y días de franco.

---

## 🛠 Tecnologías utilizadas
**Lenguaje:** Python 3.x

**Librerías estándar**
- `tkinter` – Interfaz gráfica.
- `calendar` – Manejo de calendarios.
- `datetime` – Manipulación de fechas.

**Librerías externas**
- [`tkcalendar`](https://github.com/j4321/tkcalendar) – Selector de fechas en Tkinter.
- [`Pillow`](https://pillow.readthedocs.io/en/stable/) – Manipulación de imágenes.

---

## 📂 Estructura del código
- **Variables globales:** configuración de colores, fuentes, feriados y lista de ausencias.
- **Funciones principales:**
  - `abrir_calendario_ausencias()` – Selección y gestión de ausencias.
  - `filtrar_ausencias_validas()` – Filtra ausencias que coinciden con días laborales.
  - `obtener_dias_laborales()` – Genera la lista de días laborales según el servicio.
  - `calcular()` – Procesa los datos y calcula las horas extra.
  - `mostrar_resultado_personalizado()` – Muestra un resumen visual del cálculo.
  - `actualizar_francos()` – Informa sobre días de franco según servicio y jornada.
- **Interfaz gráfica:** construida con Tkinter y widgets `ttk`.

---

## 📥 Instalación
1. Clonar el repositorio o descargar el código:
   ```bash
   git clone https://github.com/tuusuario/calculadora-horas-extra.git
