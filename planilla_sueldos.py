
from datetime import datetime, timedelta

# Función para convertir cadena "hh.mm.ss" a timedelta
def convertir_a_timedelta(cadena):
    horas_str, minutos_str, segundos_str = cadena.split('.')
    horas = int(horas_str)
    minutos = int(minutos_str)
    segundos = int(segundos_str)
    return timedelta(hours=horas, minutes=minutos, seconds=segundos)

# Función para calcular horas especiales dentro del rango 20:00 - 22:00
def calcular_horas_especiales(entrada_td, salida_td):
    inicio_especial = timedelta(hours=20)
    fin_especial = timedelta(hours=22)
    if salida_td < entrada_td:
        salida_td += timedelta(days=1)
    inicio_interseccion = max(entrada_td, inicio_especial)
    fin_interseccion = min(salida_td, fin_especial)
    if inicio_interseccion >= fin_interseccion:
        return 0
    horas_especiales = (fin_interseccion - inicio_interseccion).total_seconds() / 3600
    return horas_especiales

while True:
    valor_por_hora_input = input("Ingrese el valor por hora (Enter para usar 11.660 Gs o 'fin' para salir): ").strip()
    if valor_por_hora_input.lower() == 'fin':
        exit()
    if valor_por_hora_input == '':
        valor_por_hora = 11.660
        break
    try:
        valor_por_hora = float(valor_por_hora_input)
        break
    except:
        print("⚠️ Valor no válido. Ingrese un número válido o 'fin'.")

registros = []

while True:
    while True:
        nombre_empleado = input("\nIngrese el nombre del empleado (o 'fin' para terminar): ").strip()
        if nombre_empleado.lower() == 'fin':
            exit()
        elif nombre_empleado == '' or nombre_empleado.isdigit():
            print("⚠️ Nombre inválido. Ingrese un nombre correcto o 'fin'.")
        else:
            break

    while True:
        dias_trabajados_input = input(f"Ingrese cuántos días trabajó {nombre_empleado} (o 'fin' para salir): ").strip()
        if dias_trabajados_input.lower() == 'fin':
            exit()
        if dias_trabajados_input.isdigit() and int(dias_trabajados_input) > 0:
            dias_trabajados = int(dias_trabajados_input)
            break
        else:
            print("⚠️ Ingrese un número válido o 'fin'.")

    while True:
        fecha_inicial_str = input(f"Ingrese la fecha inicial (dd/mm/aa) para {nombre_empleado} (o 'fin'): ").strip()
        if fecha_inicial_str.lower() == 'fin':
            exit()
        try:
            fecha_inicial = datetime.strptime(fecha_inicial_str, "%d/%m/%y").date()
            break
        except:
            print("⚠️ Fecha incorrecta. Intente nuevamente o 'fin'.")

    registros_empleado = []
    total_horas_empleado = 0
    total_sueldo_empleado = 0
    total_recargo_horas_especiales = 0

    for dia in range(1, dias_trabajados + 1):
        fecha_dia = fecha_inicial + timedelta(days=dia - 1)
        print(f"\nDía {dia} ({fecha_dia.strftime('%d/%m/%y')}) para {nombre_empleado}")

        while True:
            entrada_str = input("  Ingrese la hora de ENTRADA (hh.mm.ss) o 'fin': ").strip()
            if entrada_str.lower() == 'fin':
                exit()
            try:
                entrada = convertir_a_timedelta(entrada_str)
                break
            except:
                print("⚠️ Hora inválida. Intente nuevamente o 'fin'.")

        while True:
            salida_str = input("  Ingrese la hora de SALIDA (hh.mm.ss) o 'fin': ").strip()
            if salida_str.lower() == 'fin':
                exit()
            try:
                salida = convertir_a_timedelta(salida_str)
                break
            except:
                print("⚠️ Hora inválida. Intente nuevamente o 'fin'.")

        duracion = salida - entrada
        if duracion.total_seconds() < 0:
            duracion += timedelta(days=1)

        horas_totales = duracion.total_seconds() / 3600
        horas_especiales = calcular_horas_especiales(entrada, salida)
        horas_normales = horas_totales - horas_especiales

        sueldo_normal = horas_normales * valor_por_hora
        recargo = horas_especiales * valor_por_hora * 0.30
        sueldo_especial = horas_especiales * valor_por_hora + recargo
        sueldo_dia = sueldo_normal + sueldo_especial

        total_horas_empleado += horas_totales
        total_sueldo_empleado += sueldo_dia
        total_recargo_horas_especiales += recargo

        registros_empleado.append({
            'nombre': nombre_empleado,
            'dia': dia,
            'fecha': fecha_dia.strftime('%d/%m/%y'),
            'entrada': entrada_str,
            'salida': salida_str,
            'horas': horas_totales,
            'horas_especiales': horas_especiales,
            'sueldo': sueldo_dia,
            'recargo': recargo,
            'feriado': False
        })

print("\n======== REPORTE GENERAL ========")
empleados_unicos = set([reg['nombre'] for reg in registros])
for empleado in empleados_unicos:
    horas = sum(reg['horas'] for reg in registros if reg['nombre'] == empleado)
    sueldo = sum(reg['sueldo'] for reg in registros if reg['nombre'] == empleado)
    print(f"{empleado}: {horas:.2f} horas | {sueldo:.2f} Gs.")
print("=================================")
