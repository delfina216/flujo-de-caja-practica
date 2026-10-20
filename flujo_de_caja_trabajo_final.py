nombre     = ""
sueldo     = 0.0
gremio_nom = ""
aumento    = 0.0
creditos   = []   
TIPOS_CREDITO = {
    "1": {"nombre": "Prestamo personal banco publico",   "tna": 64.0},
    "2": {"nombre": "Prestamo personal banco privado",   "tna": 95.0},
    "3": {"nombre": "Tarjeta de credito (financiacion)", "tna": 109.0},
    "4": {"nombre": "Credito hipotecario UVA",           "tna": 8.5},
    "5": {"nombre": "Prestamo prendario",                "tna": 78.0},
    "6": {"nombre": "Fintech / billetera virtual",       "tna": 145.0},
    "7": {"nombre": "Credito de consumo (comercio)",     "tna": 120.0},
    "0": {"nombre": "Ingresar TNA manualmente",          "tna": None},
}

def leer_archivo(nombre_archivo):
    nombres = []
    valores = []
    with open(nombre_archivo, "r") as archi:
        contenido = archi.read()
    lineas = contenido.split("\n")
    for linea in lineas:
        linea = linea.strip()
        if linea != "" and not linea.startswith("#"):
            partes = linea.split(";")
            nombres.append(partes[0])
            valores.append(float(partes[1]))
    return nombres, valores

def calcular_cuota(capital, tna, cuotas_totales):
    tasa_mensual  = (tna / 100) / 12
    interes_total = capital * tasa_mensual * cuotas_totales
    cuota         = (capital + interes_total) / cuotas_totales
    return cuota

def calcular_mora_diaria(saldo_vencido, tna_banco, dias):
    tasa_diaria = tna_banco / 365          
    recargo = saldo_vencido * (tasa_diaria / 100) * dias
    return round(recargo, 2)

def mostrar_tipos_credito():
    print("\n----- TIPO DE CREDITO -----")
    for k in TIPOS_CREDITO:
        t = TIPOS_CREDITO[k]
        if t["tna"] is not None:
            print(f"{k}) {t['nombre']}  (TNA {t['tna']}%)")
        else:
            print(f"{k}) {t['nombre']}")

    opc = input("Elegi una opcion: ")
    while opc not in TIPOS_CREDITO:
        print("Opcion no valida !!")
        opc = input("Elegi una opcion: ")
    return opc

def mostrar_menu(lista_nombres, lista_valores, titulo):
    print("\n----- " + titulo + " -----")
    for i in range(len(lista_nombres)):
        print(f"{i + 1}) {lista_nombres[i]}  ({lista_valores[i]}%)")
    print(f"{len(lista_nombres) + 1}) Otro (cargar manualmente)")

    opc = input("Elegi una opcion (numero): ")
    while opc.isdigit() == False or int(opc) < 1 or int(opc) > len(lista_nombres) + 1:
        print("Opcion no valida !!")
        opc = input("Elegi una opcion (numero): ")
    return int(opc)

def pantalla_inicio():
    global nombre
    print("==================================================")
    print("   EL DETERIORO DE TU SUELDO")
    print("==================================================")
    nombre = input("\nIngresa tu nombre: ").strip()
    if nombre == "":
        nombre = "Usuario"

def elegir_gremio():
    global gremio_nom, aumento
    gremios_nom, gremios_pct = leer_archivo("paritarias.txt")
    opc = mostrar_menu(gremios_nom, gremios_pct, "GREMIOS DISPONIBLES")

    if opc == len(gremios_nom) + 1:
        gremio_nom = input("Nombre de tu gremio: ")
        aumento    = float(input("Porcentaje de aumento mensual (%): "))
    else:
        gremio_nom = gremios_nom[opc - 1]
        aumento    = gremios_pct[opc - 1]

    print(f"\n✔ Gremio guardado: {gremio_nom} (+{aumento}% por mes)")

def cargar_sueldo():
    global sueldo
    print("\n----- CARGAR SUELDO NETO -----")
    if sueldo > 0:
        print(f"Sueldo actual cargado: ${sueldo}")
    sueldo = float(input("Ingresa tu sueldo neto mensual: $"))
    print(f"✔ Sueldo guardado: ${sueldo}")

def cargar_credito(numero):
    global creditos
    print(f"\n--- Datos del credito numero {numero} ---")

    bancos_nom, bancos_tna = leer_archivo("tasas_bancos.txt")
    opc_banco = mostrar_menu(bancos_nom, bancos_tna, "ENTIDADES FINANCIERAS")

    if opc_banco == len(bancos_nom) + 1:
        banco_nom = input("Nombre del banco o entidad: ")
        tna_banco = float(input("TNA del banco (%): "))   
    else:
        banco_nom = bancos_nom[opc_banco - 1]
        tna_banco = bancos_tna[opc_banco - 1]             

    opc_tipo = mostrar_tipos_credito()
    tipo_nom = TIPOS_CREDITO[opc_tipo]["nombre"]

    if opc_tipo == "0":
        tipo_nom = input("Nombre del tipo de credito: ")
        tna      = float(input("TNA anual (%): "))
    else:
        tna = TIPOS_CREDITO[opc_tipo]["tna"]

    print(f"  TNA del credito: {tna}%")

    capital = float(input("Monto del credito: $"))

    cuotas_totales = input("Cantidad total de cuotas: ")
    while cuotas_totales.isdigit() == False or int(cuotas_totales) < 1:
        print("Ingresa un numero entero mayor a 0.")
        cuotas_totales = input("Cantidad total de cuotas: ")
    cuotas_totales = int(cuotas_totales)

    cuotas_pagas = input("Cuotas que ya pagaste: ")
    while cuotas_pagas.isdigit() == False or int(cuotas_pagas) < 0 or int(cuotas_pagas) >= cuotas_totales:
        print(f"Ingresa un numero entre 0 y {cuotas_totales - 1}.")
        cuotas_pagas = input("Cuotas que ya pagaste: ")
    cuotas_pagas = int(cuotas_pagas)

    resp_mora = input("Esta en mora? (si / no): ").strip().lower()
    while resp_mora != "si" and resp_mora != "no":
        print("Escribi 'si' o 'no'.")
        resp_mora = input("Esta en mora? (si / no): ").strip().lower()

    if resp_mora == "si":
        en_mora = True
        cuotas_atrasadas = input("Cuantas cuotas estás atrasado?: ")
        while cuotas_atrasadas.isdigit() == False or int(cuotas_atrasadas) < 1:
            print("Ingresa un numero mayor a 0.")
            cuotas_atrasadas = input("Cuantas cuotas estás atrasado?: ")
        cuotas_atrasadas = int(cuotas_atrasadas)

        tasa_diaria = tna_banco / 365
        print(f"  Tasa de mora diaria del banco: {round(tasa_diaria, 4)}% (TNA {tna_banco}% / 365)")
    else:
        en_mora          = False
        cuotas_atrasadas = 0

    cuota = calcular_cuota(capital, tna, cuotas_totales)

    saldo_vencido = round(cuota * cuotas_atrasadas, 2)

    credito = {
        "banco":            banco_nom,
        "tipo":             tipo_nom,
        "capital":          capital,
        "tna":              tna,
        "cuota":            cuota,            
        "saldo_vencido":    saldo_vencido,     
        "tna_banco":        tna_banco,        
        "cuotas_totales":   cuotas_totales,
        "cuotas_pagas":     cuotas_pagas,
        "en_mora":          en_mora,
        "cuotas_atrasadas": cuotas_atrasadas
    }
    creditos.append(credito)

    print("✔ Credito agregado.")
    print(f"  Cuota mensual normal:  ${round(cuota, 2)}")
    if en_mora:
        print(f"  Saldo vencido: ${saldo_vencido}  ({cuotas_atrasadas} cuota/s atrasada/s)")
        print(f"  Tasa de mora: {round(tna_banco / 365, 4)}% diario  ->  el recargo se acumula cada mes hasta cancelar.")

def menu_creditos():
    while True:
        print("\n----- MENU CREDITOS -----")
        print("1) Agregar un credito")
        print("2) Ver creditos cargados")
        print("3) Volver al menu principal")

        opc = input("Elegi una opcion: ")
        while opc.isdigit() == False or int(opc) < 1 or int(opc) > 3:
            print("Opcion no valida !!")
            opc = input("Elegi una opcion: ")
        opc = int(opc)

        if opc == 1:
            cargar_credito(len(creditos) + 1)
        elif opc == 2:
            ver_lista_creditos()
        else:
            return

def ver_lista_creditos():
    if len(creditos) == 0:
        print("(No hay creditos cargados todavia)")
        return
    print("\n--- Creditos cargados ---")
    for i in range(len(creditos)):
        c = creditos[i]
        linea = f"{i + 1}) {c['tipo']} en {c['banco']}"
        linea = linea + f" - TNA: {c['tna']}%"
        linea = linea + f" - Cuota: ${round(c['cuota'], 2)}"
        linea = linea + f" - Restantes: {c['cuotas_totales'] - c['cuotas_pagas']}"
        if c["en_mora"]:
            linea = linea + f"  [!] EN MORA ({c['cuotas_atrasadas']} cuotas, {round(c['tna_banco'] / 365, 4)}%/dia)"
        print(linea)

def ver_cashflow():
    if sueldo == 0 or gremio_nom == "" or len(creditos) == 0:
        print("\n[!] Antes de ver el cash flow completa: sueldo, gremio y al menos un credito.")
        return

    print("\n==================================================")
    print(f"   CASH FLOW 12 MESES  -  {nombre.upper()}")
    print("==================================================")
    print(f"Gremio: {gremio_nom} (+{aumento}% por mes)")
    print(f"Sueldo inicial: ${sueldo}")
    print("Umbral de alerta: 40% disponible")
    print("--------------------------------------------------")

    sueldo_actual = sueldo

    for mes in range(1, 13):
        if mes > 1:
            sueldo_actual = sueldo_actual * (1 + aumento / 100)
        total_cuotas = 0
        total_mora   = 0
        for c in creditos:
            cuotas_restantes = c["cuotas_totales"] - c["cuotas_pagas"] - (mes - 1)
            if cuotas_restantes > 0:
                total_cuotas = total_cuotas + c["cuota"]
            if c["en_mora"]:
                dias_atraso = mes * 30
                mora = calcular_mora_diaria(c["saldo_vencido"],
                                            c["tna_banco"],
                                            dias_atraso)
                total_mora = total_mora + mora

        total_cuotas = total_cuotas + total_mora

        disponible = sueldo_actual - total_cuotas
        pct        = (disponible / sueldo_actual) * 100

        print(f"\nMes {mes}:")
        print(f"  Sueldo:      ${round(sueldo_actual, 2)}")
        print(f"  Cuotas:      ${round(total_cuotas, 2)}")

        if total_mora > 0:
            for c in creditos:
                if c["en_mora"]:
                    dias_atraso = mes * 30
                    mora = calcular_mora_diaria(c["saldo_vencido"],
                                                c["tna_banco"],
                                                dias_atraso)
                    print(f"    (incluye ${round(mora, 2)} de mora acumulada en {c['banco']} - {dias_atraso} dias)")

        print(f"  Disponible:  ${round(disponible, 2)}  ({round(pct, 1)}% del sueldo)")

        if disponible < 0:
            print("  *** INSOLVENTE: las cuotas superan el sueldo ***")
        elif pct < 40:
            print("  *** ALERTA: disponibilidad bajo el 40% ***")
        elif pct < 60:
            print("  (!) Atencion: disponibilidad entre 40% y 60%")

    print("\n--------------------------------------------------")
    print("RESUMEN DE DETERIORO")
    print("--------------------------------------------------")

    sueldo_final = sueldo
    for mes in range(12):
        sueldo_final = sueldo_final * (1 + aumento / 100)
    variacion = (sueldo_final / sueldo - 1) * 100

    suma_tna = 0
    for c in creditos:
        suma_tna = suma_tna + c["tna"]
    tna_promedio = suma_tna / len(creditos)

    print(f"Aumento acumulado de tu sueldo (12 meses): +{round(variacion, 1)}%")
    print(f"TNA promedio de tus creditos:               {round(tna_promedio, 1)}%")

    if tna_promedio > variacion:
        brecha = round(tna_promedio - variacion, 1)
        print(f"\n[!] Tus tasas superan tu aumento salarial en {brecha} puntos.")
        print("    Cada mes tus creditos te consumen una porcion MAYOR de tu sueldo real.")
    else:
        brecha = round(variacion - tna_promedio, 1)
        print(f"\n[ok] Tu sueldo crece mas que tus tasas (+{brecha} puntos a favor).")

    input("\n[Enter para volver al menu principal]")

def ver_resumen():
    print("\n==================================================")
    print(f"   RESUMEN DE TUS CREDITOS, {nombre.upper()}")
    print("==================================================")
    print(f"Gremio: {gremio_nom} (+{aumento}% mensual)")
    for c in creditos:
        linea = f"- {c['tipo']} en {c['banco']}"
        linea = linea + f" | TNA: {c['tna']}%"
        linea = linea + f" | Cuota: ${round(c['cuota'], 2)}"
        if c["en_mora"]:
            linea = linea + f"  [!] EN MORA - saldo vencido: ${round(c['saldo_vencido'], 2)} ({round(c['tna_banco'] / 365, 4)}%/dia)"
        print(linea)
    input("\n[Enter para volver al menu principal]")

def calcular_resultados_cashflow():
    # Recorre los 12 meses igual que ver_cashflow, pero sin imprimir.
    # Solo devuelve el disponible del mes 12 y los datos del resumen.
    sueldo_actual = sueldo
    disponible_mes12 = 0

    for mes in range(1, 13):
        if mes > 1:
            sueldo_actual = sueldo_actual * (1 + aumento / 100)
        total_cuotas = 0
        total_mora   = 0
        for c in creditos:
            cuotas_restantes = c["cuotas_totales"] - c["cuotas_pagas"] - (mes - 1)
            if cuotas_restantes > 0:
                total_cuotas = total_cuotas + c["cuota"]
            if c["en_mora"]:
                dias_atraso = mes * 30
                mora = calcular_mora_diaria(c["saldo_vencido"], c["tna_banco"], dias_atraso)
                total_mora = total_mora + mora
        total_cuotas = total_cuotas + total_mora
        disponible = sueldo_actual - total_cuotas
        if mes == 12:
            disponible_mes12 = disponible

    sueldo_final = sueldo
    for mes in range(12):
        sueldo_final = sueldo_final * (1 + aumento / 100)
    variacion = (sueldo_final / sueldo - 1) * 100

    suma_tna = 0
    for c in creditos:
        suma_tna = suma_tna + c["tna"]
    tna_promedio = suma_tna / len(creditos)

    if tna_promedio > variacion:
        brecha = round(tna_promedio - variacion, 1)
    else:
        brecha = round(variacion - tna_promedio, 1)

    return round(disponible_mes12, 2), round(variacion, 1), round(tna_promedio, 1), brecha

def guardar_csv():
    if sueldo == 0 or gremio_nom == "" or len(creditos) == 0:
        print("\n[!] Antes de guardar completa: sueldo, gremio y al menos un credito.")
        return

    disponible_mes12, variacion, tna_promedio, brecha = calcular_resultados_cashflow()

    # Si el archivo no existe todavia, escribo primero la linea de encabezado.
    existe = False
    try:
        with open("registros.csv", "r") as archi:
            if archi.read() != "":
                existe = True
    except:
        existe = False

    with open("registros.csv", "a") as archi:
        if existe == False:
            archi.write("nombre;sueldo_inicial;gremio;aumento_mensual;disponible_mes12;aumento_acum_12m;tna_promedio;brecha\n")
        linea = nombre + ";" + str(sueldo) + ";" + gremio_nom + ";" + str(aumento)
        linea = linea + ";" + str(disponible_mes12) + ";" + str(variacion)
        linea = linea + ";" + str(tna_promedio) + ";" + str(brecha)
        archi.write(linea + "\n")

    print("\n✔ Registro guardado en registros.csv")
    print(f"  {nombre} - disponible mes 12: ${disponible_mes12} - brecha: {brecha} puntos")
    input("\n[Enter para volver al menu principal]")

def menu_principal():
    while True:
        est_gremio  = "✔" if gremio_nom != "" else "✘"
        est_sueldo  = "✔" if sueldo > 0 else "✘"
        est_credito = f"✔ ({len(creditos)})" if len(creditos) > 0 else "✘"

        print("\n==================================================")
        print(f"   MENU PRINCIPAL  -  Hola, {nombre}!")
        print("==================================================")
        print(f"[{est_gremio}] 1) Seleccionar gremio / convenio")
        print(f"[{est_sueldo}] 2) Cargar sueldo neto")
        print(f"[{est_credito}] 3) Administrar creditos")
        print("      4) Ver Cash Flow (12 meses)")
        print("      5) Ver resumen de creditos")
        print("      6) Guardar registro en CSV")
        print("      0) Salir")
        print("--------------------------------------------------")

        opc = input("Elegi una opcion: ")
        while opc.isdigit() == False or int(opc) < 0 or int(opc) > 6:
            print("Opcion no valida !!")
            opc = input("Elegi una opcion: ")
        opc = int(opc)

        if opc == 1:
            elegir_gremio()
        elif opc == 2:
            cargar_sueldo()
        elif opc == 3:
            menu_creditos()
        elif opc == 4:
            ver_cashflow()
        elif opc == 5:
            ver_resumen()
        elif opc == 6:
            guardar_csv()
        else:
            print(f"\nHasta luego, {nombre}!")
            break

pantalla_inicio()
menu_principal()
