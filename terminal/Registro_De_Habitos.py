import json, os
from datetime import date, datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / 'data' / 'terminal'
REPORT_DIR = BASE / 'reportes'
HABITOS = [
    'Despertar temprano','Hacer la cama','Higiene personal','Desayuno saludable','Estiramientos','Beber agua','Ejercicio ligero','Meditación','Lectura diaria','Estudio / Trabajo productivo','Pausas activas','Almuerzo balanceado','Siesta corta','Hidratación continua','Ocio digital controlado','No redes después de 8 p.m.','Rutina relajante','Dormir antes de las 11 p.m.','Evitar comida chatarra','Registro de gastos','Reflexión diaria'
]
RESET='\033[0m'; GREEN='\033[92m'; CYAN='\033[96m'; YELLOW='\033[93m'; RED='\033[91m'; BOLD='\033[1m'
USER='usuario'; FILE=None

def clear(): os.system('cls' if os.name == 'nt' else 'clear')
def pause(): input(f'\n{YELLOW}Presiona ENTER para continuar...{RESET}')
def box(title):
    print(f'{GREEN}╔' + '═'*56 + '╗')
    print('║' + title.center(56) + '║')
    print('╚' + '═'*56 + f'╝{RESET}')
def load():
    if FILE and FILE.exists():
        try:
            with FILE.open('r', encoding='utf-8') as f: data=json.load(f)
            return data if isinstance(data,dict) else {}
        except (json.JSONDecodeError,OSError):
            print(f'{RED}No se pudo leer el archivo de datos. No se sobrescribió.{RESET}')
            pause()
    return {}
def save(data):
    if FILE:
        FILE.parent.mkdir(parents=True,exist_ok=True)
        tmp=FILE.with_suffix('.tmp')
        with tmp.open('w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2)
        tmp.replace(FILE)
def day_record(data, day=None):
    key=day or str(date.today())
    data.setdefault(key, {'habitos':{},'reflexion':{}})
    data[key].setdefault('habitos',{}); data[key].setdefault('reflexion',{})
    return data[key]
def done_count(data, day): return sum(int(data.get(day,{}).get('habitos',{}).get(h,0))==1 for h in HABITOS)
def pct_habit(data,h):
    days=list(data)
    return round(sum(int(data[d].get('habitos',{}).get(h,0))==1 for d in days)*100/len(days)) if days else 0
def streaks(data,h):
    successful=[]
    for key, record in data.items():
        try:
            parsed=date.fromisoformat(key)
        except (TypeError, ValueError):
            continue
        if int(record.get('habitos',{}).get(h,0))==1:
            successful.append(parsed)
    successful.sort()
    best=run=0; prev=None
    for d in successful:
        run=run+1 if prev and d-prev==timedelta(days=1) else 1
        best=max(best,run); prev=d
    current=0; cursor=date.today()
    # La racha sigue vigente si el hábito se cumplió hoy o ayer.
    if int(data.get(str(cursor),{}).get('habitos',{}).get(h,0))!=1:
        cursor-=timedelta(days=1)
    while str(cursor) in data and int(data[str(cursor)].get('habitos',{}).get(h,0))==1:
        current+=1; cursor-=timedelta(days=1)
    return best,current

def register():
    data=load(); key=str(date.today())
    clear(); box('REGISTRO DIARIO DE HÁBITOS')
    current=data.get(key,{}).get('habitos',{})
    if key in data: print(f'{YELLOW}Ya existe un registro de hoy. Puedes actualizarlo.{RESET}')
    answers={}
    for i,h in enumerate(HABITOS,1):
        default='1' if int(current.get(h,0))==1 else '0'
        while True:
            r=input(f'{CYAN}{i:02}. {h} [1=Sí / 0=No] (actual {default}): {RESET}').strip()
            if not r: r=default
            if r in ('0','1'): answers[h]=int(r); break
            print(f'{RED}Escribe 1 o 0.{RESET}')
    record=day_record(data,key); record['habitos']=answers
    print(f'\n{BOLD}REFLEXIÓN DIARIA{RESET}')
    prompts={'logro':'¿Qué fue lo mejor que hiciste hoy? ','obstaculo':'¿Qué te dificultó cumplir hábitos? ','aprendizaje':'¿Qué aprendiste hoy? ','intencion':'¿Cuál es tu intención para mañana? ','estado':'¿Cómo te sentiste hoy? '}
    for k,prompt in prompts.items():
        old=record['reflexion'].get(k,''); val=input(f'{CYAN}{prompt}{RESET}[Enter conserva lo anterior] ')
        if val.strip(): record['reflexion'][k]=val.strip()
        elif k not in record['reflexion']: record['reflexion'][k]=old
    save(data); print(f'{GREEN}Registro guardado. Cumplimiento de hoy: {done_count(data,key)}/{len(HABITOS)}.{RESET}'); pause()

def weekly():
    data=load(); clear(); box('VISTA DE LOS ÚLTIMOS 7 DÍAS')
    days=[date.today()-timedelta(days=i) for i in range(6,-1,-1)]
    print('HÁBITO'.ljust(31)+' '.join(d.strftime('%a')[:2] for d in days))
    print('-'*53)
    for h in HABITOS:
        marks=['✓' if int(data.get(str(d),{}).get('habitos',{}).get(h,0))==1 else ('·' if str(d) in data else '—') for d in days]
        print(f'{h[:29]:29}  '+'  '.join(marks))
    pause()
def stats():
    data=load(); clear(); box('ESTADÍSTICAS DE CUMPLIMIENTO')
    if not data:
        print('Aún no hay registros.'); pause(); return
    rows=sorted(((pct_habit(data,h),h) for h in HABITOS),reverse=True)
    for p,h in rows:
        filled=round(p/5)
        bar='█'*filled+'░'*(20-filled)
        print(f'{h[:29]:29} {bar} {p:3}%')
    total=sum(done_count(data,d) for d in data); possible=len(data)*len(HABITOS)
    print(f'\nDías registrados: {len(data)} | Cumplimiento global: {round(total*100/possible) if possible else 0}%')
    print(f'Hábito más cumplido: {rows[0][1]} ({rows[0][0]}%)')
    print(f'Hábito por fortalecer: {rows[-1][1]} ({rows[-1][0]}%)')
    pause()

def streak_report():
    data=load(); clear(); box('RACHAS POR HÁBITO')
    if not data:
        print('Aún no hay registros.'); pause(); return
    for h in HABITOS:
        best,current=streaks(data,h)
        print(f'{h[:31]:31} mejor: {best:3} días | actual: {current:3} días')
    pause()

def reminders():
    clear(); box('RECORDATORIOS Y RUTINA')
    hour=datetime.now().hour
    if hour<8: msg='Bebe agua y haz unos estiramientos para empezar.'
    elif hour<12: msg='Organiza tus prioridades y registra tus avances.'
    elif hour<18: msg='Haz una pausa activa y muévete un poco.'
    elif hour<20: msg='Empieza a bajar el ritmo y limita las distracciones.'
    else: msg='Prepara una rutina relajante y descansa.'
    print(f'\nSugerencia para este momento: {msg}\n')
    for t,m in [('07:00','Agua y estiramientos'),('12:00','Pausa consciente y revisión'),('18:00','Ejercicio o movimiento'),('21:00','Desconexión y descanso')]: print(f'  {t}  •  {m}')
    print('\nNota: son recordatorios dentro de la aplicación, no alarmas del sistema.')
    pause()

def export_report():
    data=load(); clear(); box('EXPORTAR REPORTE')
    if not data:
        print('Aún no hay registros para exportar.'); pause(); return
    REPORT_DIR.mkdir(parents=True,exist_ok=True)
    start=date.today()-timedelta(days=6); days=[str(start+timedelta(days=i)) for i in range(7)]
    relevant=[d for d in days if d in data]
    lines=['REPORTE DE HÁBITOS — ÚLTIMOS 7 DÍAS',f'Generado: {datetime.now():%Y-%m-%d %H:%M}',f'Registros en el período: {len(relevant)}','', 'CUMPLIMIENTO POR HÁBITO (PERÍODO)']
    for h in HABITOS:
        pct=round(sum(int(data[d].get('habitos',{}).get(h,0))==1 for d in relevant)*100/len(relevant)) if relevant else 0
        lines.append(f'{h}: {pct}%')
    lines+=['','REGISTROS DIARIOS']
    for d in days:
        lines.append(f'{d}: {done_count(data,d)}/{len(HABITOS)} hábitos' if d in data else f'{d}: Sin registro')
    out=REPORT_DIR/f'reporte_habitos_{USER}_{date.today()}.txt'; out.write_text('\n'.join(lines),encoding='utf-8')
    print(f'Reporte creado: {out}'); pause()

def backup_json():
    data=load(); REPORT_DIR.mkdir(parents=True,exist_ok=True)
    out=REPORT_DIR/f"respaldo_habitos_{USER}_{date.today()}.json"
    out.write_text(json.dumps({'user':USER,'records':data},ensure_ascii=False,indent=2),encoding='utf-8')
    clear(); box('RESPALDO DE DATOS')
    print(f'\nRespaldo JSON creado correctamente:\n{out}\n')
    print('Guarda una copia de este archivo en un lugar seguro.')
    pause()

def main():
    global USER, FILE
    DATA_DIR.mkdir(parents=True,exist_ok=True); clear(); box('REGISTRO DE HÁBITOS · TERMINAL')
    USER=input('Nombre de usuario: ').strip().lower()
    USER=''.join(c for c in USER if c.isalnum() or c in ('-','_')) or 'default'
    FILE=DATA_DIR/f'habitos_{USER}.json'
    while True:
        clear(); box('REGISTRO DE HÁBITOS · MENÚ PRINCIPAL')
        print(f' Usuario: {USER}\n Archivo de datos: data/terminal/habitos_{USER}.json\n')
        print('  SEGUIMIENTO')
        print('  1. Registrar o actualizar hábitos de hoy')
        print('  2. Vista semanal por hábito')
        print('  3. Estadísticas de cumplimiento')
        print('  4. Rachas por hábito')
        print('  HERRAMIENTAS')
        print('  5. Recordatorios y rutina')
        print('  6. Exportar reporte semanal')
        print('  7. Crear respaldo JSON')
        print('  8. Salir')
        choice=input('\nSelecciona una opción: ').strip()
        if choice=='1': register()
        elif choice=='2': weekly()
        elif choice=='3': stats()
        elif choice=='4': streak_report()
        elif choice=='5': reminders()
        elif choice=='6': export_report()
        elif choice=='7': backup_json()
        elif choice=='8': print('¡Gracias! Tus registros permanecen guardados.'); break
        else: print('Opción no válida.'); pause()

if __name__=='__main__':
    try: main()
    except KeyboardInterrupt: print('\nSalida solicitada. Los registros guardados se conservan.')
