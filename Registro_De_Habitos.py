import os
import json
from datetime import date, timedelta, datetime

# ============================================================
#                  COLORES (ESTILO HACKER)
# ============================================================
RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"

# ============================================================
#                  CONFIGURACIÓN
# ============================================================
USUARIO = None

HABITOS = [
    "Despertar temprano / Estiramientos",
    "Ejercicio ligero",
    "Estudio / Trabajo productivo",
    "Ocio digital controlado",
    "No redes después de 8 p.m.",
    "Rutina relajante",
    "Dormir antes de las 11 p.m.",
    "Registro de gastos",
    "Reflexión diaria"
]

# ============================================================
#                  UTILIDADES
# ============================================================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(YELLOW + "\n▶ Presione ENTER para continuar..." + RESET)

def seleccionar_usuario():
    global USUARIO
    clear()
    print(GREEN + BOLD + "╔═══════════════════════════╗")
    print("║  👤 SELECCIÓN DE USUARIO  ║")
    print("╚═══════════════════════════╝" + RESET)

    nombre = input(CYAN + "Ingrese su nombre de usuario: " + RESET).strip().lower()
    if not nombre:
        nombre = "default"

    USUARIO = f"habitos_{nombre}.json"

def cargar():
    if USUARIO and os.path.exists(USUARIO):
        with open(USUARIO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar(datos):
    if USUARIO:
        with open(USUARIO, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

# ============================================================
#                  ⏰ ALARMAS REALES
# ============================================================
def alarmas_reales():
    hora = datetime.now().hour
    print(GREEN + BOLD + "╔═══════════════════════════╗")
    print("║         ⏰ ALARMA         ║")
    print("╚═══════════════════════════╝" + RESET)

    if hora < 8:
        print(CYAN + "💧 Agua + estiramientos. Buen inicio." + RESET)
    elif hora < 12:
        print(YELLOW + "📚 Enfoque productivo." + RESET)
    elif hora < 18:
        print(GREEN + "🏃 Momento ideal para moverte." + RESET)
    elif hora < 20:
        print(YELLOW + "📵 Prepárate para desconectar." + RESET)
    else:
        print(CYAN + "🧘 Rutina relajante. Descansa." + RESET)

    pause()

# ============================================================
#                  📝 REGISTRO GUIADO (NUEVA ESTÉTICA)
# ============================================================
def registrar_dia():
    datos = cargar()
    hoy = str(date.today())

    if hoy in datos:
        print(RED + "⚠ Hoy ya fue registrado." + RESET)
        pause()
        return

    clear()
    print(GREEN + BOLD + "╔══════════════════════════════════════╗")
    print("║     📝 REGISTRO GUIADO DE HÁBITOS    ║")
    print("╠══════════════════════════════════════╣")
    print("║      Responda con 1 (Sí) o 0 (No)    ║")
    print("╚══════════════════════════════════════╝" + RESET)

    datos[hoy] = {"habitos": {}, "reflexion": {}}

    for h in HABITOS:
        while True:
            r = input(CYAN + f"✔ {h}: " + RESET)
            if r in ("0", "1"):
                datos[hoy]["habitos"][h] = int(r)
                break
            print(RED + "✖ Solo se permite 1 o 0." + RESET)

    # 🧠 REFLEXIÓN GUIADA AVANZADA
    print(GREEN + BOLD + "\n╔══════════════════════════════════╗")
    print("║    🧠 REFLEXIÓN DIARIA GUIADA    ║")
    print("╚══════════════════════════════════╝" + RESET)

    datos[hoy]["reflexion"]["logro"] = input(
        CYAN + "✔ ¿Qué fue lo mejor que hiciste hoy? " + RESET
    )
    datos[hoy]["reflexion"]["obstaculo"] = input(
        CYAN + "⚠ ¿Qué te dificultó cumplir hábitos? " + RESET
    )
    datos[hoy]["reflexion"]["aprendizaje"] = input(
        CYAN + "🧩 ¿Qué aprendiste hoy? " + RESET
    )
    datos[hoy]["reflexion"]["intencion"] = input(
        CYAN + "🎯 ¿Cuál es tu intención para mañana? " + RESET
    )
    datos[hoy]["reflexion"]["estado"] = input(
        CYAN + "😌 ¿Cómo te sentiste hoy? " + RESET
    )

    guardar(datos)
    print(GREEN + "\n✔ Registro completo y guardado correctamente." + RESET)
    pause()

# ============================================================
#                  📅 VISTA SEMANAL MEJORADA
# ============================================================
def vista_semanal():
    datos = cargar()
    clear()

    hoy = date.today()
    semana = [(hoy - timedelta(days=i)) for i in range(6, -1, -1)]  # Últimos 7 días

    # Nombres de los días en español
    dias_semana = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]
    dias_mostrar = [dias_semana[d.weekday()] for d in semana]

    # Cabecera
    print(GREEN + "╔" + "═" * 32 + "╦" + "═" * (7*5) + "╗" + RESET)
    print(CYAN + "║   HÁBITO   📅 VISTA SEMANAL".ljust(32) + "║", end="")
    for d in dias_mostrar:
        print(CYAN + d.center(5), end="")
    print(CYAN + "║" + RESET)
    print(GREEN + "╠" + "═" * 32 + "╬" + "═" * (7*5) + "╣" + RESET)

    # Mostrar hábitos con marcas
    for h in HABITOS:
        print(YELLOW + f"║ {h[:30]:<30} ", end="╦")
        for i, d in enumerate(semana):
            fecha_str = str(d)  # La fecha real para acceder a los datos
            marca = "✔" if fecha_str in datos and datos[fecha_str]["habitos"].get(h, 0) == 1 else "·"
            color = GREEN if marca == "✔" else RED
            print(color + marca.center(5) + RESET, end="")
        print(YELLOW + "║" + RESET)

    print(GREEN + "╚" + "═" * 32 + "╩" + "═" * (7*5) + "╝" + RESET)
    pause()

# ============================================================
#                  📊 ESTADÍSTICAS + GRÁFICO
# ============================================================
def estadisticas_avanzadas():
    datos = cargar()
    if not datos:
        print(RED + "⚠ No hay registros para mostrar estadísticas." + RESET)
        pause()
        return

    clear()
    total_dias = len(datos)
    total_ok = 0
    print(GREEN + BOLD + "╔" + "═" * 58 + "╗" + RESET)
    print(GREEN + BOLD + "║     📊 ESTADÍSTICAS AVANZADAS % CUMPLIMIENTO HÁBITOS     ║" + RESET)
    print(GREEN + BOLD + "╚" + "═" * 58 + "╝" + RESET)

    max_rachas = {h: 0 for h in HABITOS}
    cumplimientos = {}

    # Cabecera tabla
    print(GREEN + "╔" + "═" * 58 + "╗" + RESET)
    print(CYAN + "║    SEGUIMIENTO DE HÁBITOS    │       CUMPLIMIENTO %      ║" + RESET)
    print(GREEN + "╠" + "═" * 30 + "╪" + "═" * 27 + "╣" + RESET)

    for h in HABITOS:
        consecutivo = 0
        ok = 0
        for d in sorted(datos):
            valor = datos[d]["habitos"].get(h, 0)
            if valor == 1:
                ok += 1
                consecutivo += 1
            else:
                consecutivo = 0
            if consecutivo > max_rachas[h]:
                max_rachas[h] = consecutivo
        total_ok += ok
        pct = int((ok / total_dias) * 100)
        cumplimientos[h] = pct

        # Barra fija de 20 bloques con gradiente
        bloques = 20
        llenos = int(pct / 5)
        barra = ""
        for i in range(bloques):
            if i < llenos:
                if i < 5:
                    barra += RED + "█" + RESET
                elif i < 10:
                    barra += YELLOW + "█" + RESET
                elif i < 15:
                    barra += CYAN + "█" + RESET
                else:
                    barra += GREEN + "█" + RESET
            else:
                barra += "░"

        # Emoji dinámico según porcentaje
        if pct >= 90:
            emoji = "🏆"
        elif pct >= 75:
            emoji = "🔥"
        elif pct >= 50:
            emoji = "⚡"
        else:
            emoji = "🌱"

        # Color del porcentaje según nivel
        if pct >= 75:
            pct_color = GREEN
        elif pct >= 50:
            pct_color = YELLOW
        else:
            pct_color = RED

        # Imprimir barra con porcentaje alineado + emoji
        print(CYAN + f"║ {h[:28]:<28} │ " + f"{barra} {pct_color}{pct:>3}%{RESET} {emoji}" + " ║" + RESET)

    print(GREEN + "╚" + "═" * 30 + "╧" + "═" * 27 + "╝" + RESET)

    # Hábito más cumplido y más fallado
    h_max = max(cumplimientos, key=lambda k: cumplimientos[k])
    h_min = min(cumplimientos, key=lambda k: cumplimientos[k])

    print(YELLOW + f"\n✔ Hábito más cumplido: {h_max} ({cumplimientos[h_max]}%)" + RESET)
    print(RED + f"⚠ Hábito más fallado: {h_min} ({cumplimientos[h_min]}%)" + RESET)

    pause()

# ============================================================
#                  🔥 RACHAS + NIVEL GLOBA
# ============================================================
def mostrar_rachas_y_nivel_global():
    datos = cargar()
    if not datos:
        print(RED + "⚠ No hay registros para mostrar estadísticas." + RESET)
        pause()
        return

    total_dias = len(datos)
    total_ok = 0
    max_rachas = {h: 0 for h in HABITOS}

    # Calcular rachas y total_ok
    for h in HABITOS:
        consecutivo = 0
        for d in sorted(datos):
            valor = datos[d]["habitos"].get(h, 0)
            if valor == 1:
                total_ok += 1
                consecutivo += 1
            else:
                consecutivo = 0
            if consecutivo > max_rachas[h]:
                max_rachas[h] = consecutivo

    # ===== Mostrar rachas enmarcadas =====
    clear()
    print(GREEN + "╔" + "═" * 32 + "╦" + "═" * 20 + "╗" + RESET)
    print(CYAN + "║      🔥 RACHAS POR HÁBITO      ║" + "    DÍAS DE RACHA   ║" + RESET)
    print(GREEN + "╠" + "═" * 32 + "╬" + "═" * 20 + "╣" + RESET)

    for h in HABITOS:
        print(YELLOW + f"║ {h[:30]:<30} ║" + YELLOW + f"{max_rachas[h]:^5}" + RESET + YELLOW + "DÍAS SEGUIDOS  ║" + RESET)

    print(GREEN + "╚" + "═" * 32 + "╩" + "═" * 20 + "╝" + RESET)

    # ===== Nivel global =====
    total_posible = total_dias * len(HABITOS)
    global_pct = int((total_ok / total_posible) * 100)
    print(YELLOW + f"\n✔ Cumplimiento global: {global_pct}%" + RESET)

    if global_pct >= 90:
        nivel = "🏆 MAESTRO"
    elif global_pct >= 75:
        nivel = "🔥 DISCIPLINADO"
    elif global_pct >= 50:
        nivel = "⚡ CONSTANTE"
    else:
        nivel = "🌱 NOVATO"

    print(GREEN + f"Nivel global: {nivel}" + RESET)
    pause()

# ============================================================
#                  🧾 REPORTE SEMANAL
# ============================================================
def exportar_reporte():
    datos = cargar()
    if not datos:
        pause()
        return

    nombre = USUARIO.replace("habitos_", "").replace(".json", "")
    archivo = f"reporte_{nombre}.txt"

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("REPORTE SEMANAL DE HÁBITOS\n")
        f.write("=" * 40 + "\n\n")
        for h in HABITOS:
            ok = sum(datos[d]["habitos"][h] for d in datos)
            pct = int((ok / len(datos)) * 100)
            f.write(f"{h}: {pct}%\n")

    print(GREEN + f"✔ Reporte exportado: {archivo}" + RESET)
    pause()

# ============================================================
#                  ⏰ ALARMAS Y RECORDATORIOS
# ============================================================
RECORDATORIOS = [
    {"hora": 7, "mensaje": "💧 Bebe agua"},
    {"hora": 9, "mensaje": "📚 Estudia o trabaja de manera productiva"},
    {"hora": 18, "mensaje": "🏃 Haz ejercicio o muévete un poco"},
]
# ============================================================
#             ⏰ ALARMAS Y RECORDATORIOS AUTOMÁTICOS
# ============================================================
def alarmas_y_recordatorios():
    hora = datetime.now().hour
    clear()
    print(GREEN + BOLD + "╔══════════════════════════════════╗")
    print("║    ⏰ ALARMAS & RECORDATORIOS    ║")
    print("╚══════════════════════════════════╝" + RESET)

    # Alarmas por hora
    if hora < 8:
        print(CYAN + "💧 Agua + estiramientos. Buen inicio." + RESET)
    elif hora < 12:
        print(YELLOW + "📚 Enfoque productivo." + RESET)
    elif hora < 18:
        print(GREEN + "🏃 Momento ideal para moverte." + RESET)
    elif hora < 20:
        print(YELLOW + "📵 Prepárate para desconectar." + RESET)
    else:
        print(CYAN + "🧘 Rutina relajante. Descansa." + RESET)

    # Recordatorios por hábito
    print(GREEN + BOLD + "\n💡 RECORDATORIOS DE HÁBITOS" + RESET)
    print(YELLOW + "💧 Beber agua" + RESET)
    print(YELLOW + "📚 Estudiar / Trabajo productivo" + RESET)
    print(YELLOW + "🧘 Rutina relajante antes de dormir" + RESET)
    print(YELLOW + "🛌 Dormir antes de las 11 p.m." + RESET)

    pause()

# ============================================================
#                  MENÚ PRINCIPAL
# ============================================================
def main():
    seleccionar_usuario()
    alarmas_reales()

    while True:
        clear()
        print(GREEN + BOLD + "╔══════════════════════════════╗")
        print("║  SISTEMA DE HÁBITOS PRO MAX  ║")
        print("╚══════════════════════════════╝" + RESET)
        print(CYAN + "1. Registrar hábitos de hoy")
        print("2. Vista semanal 📅")
        print("3. Estadísticas + gráfico 📊")
        print("4. Rachas + gráfico 📊")
        print("5. alarmas_y_recordatorios")
        print("6. Exportar reporte 🧾")
        print("7. ❌ Salir" + RESET)
        print(GREEN + "================================" + RESET)

        op = input(YELLOW + "Seleccione opción: " + RESET)
        if not op.isdigit():
            continue

        if op == "1":
            registrar_dia()
        elif op == "2":
            vista_semanal()
        elif op == "3":
            estadisticas_avanzadas()
        elif op == "4":
            mostrar_rachas_y_nivel_global()
        elif op == "5":
            alarmas_y_recordatorios()
        elif op == "6":
            exportar_reporte()
        elif op == "7":
            break

if __name__ == "__main__":
    main() 