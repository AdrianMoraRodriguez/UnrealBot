import pysmile_license
import pysmile

net = pysmile.Network()
net.read_file("data/red_bayesiana.xdsl")
nodos = {
  "St": "Estado en tiempo t (Atacar, Recoger_Arma, Recoger_Energia, Explorar, Huir, Detectar_peligro)",
  "H": "Nivel de salud (Alto o Bajo)",
  "W": "Armas del bot (Armado o Desarmado)",
  "OW": "Armas de los oponentes (Armado o Desarmado)",
  "HN": "Sonido detectado (SeOye o NoSeOye)",
  "NE": "Enemigos cercanos (Si o No)",
  "PW": "Arma cercana (Si o No)",
  "PH": "Paquete de salud cercano (Si o No)",
}
mode_of_use = input("¿Desea ingresar los valores de los nodos (0), el modo de tender al infinito? (1) o el modo aprendizaje? (3): ")
if (mode_of_use == "0"): 
  valores_usuario = {}
  for nodo in nodos:
    valores_usuario[nodo] = input(f"Ingrese el valor para {nodos[nodo]}: ")
  for nodo, valor in valores_usuario.items():
    net.set_evidence(nodo, valor)
  net.update_beliefs()
  distribucion_St1_dado_St = net.get_node_value("St_1")
  for i in range(len(distribucion_St1_dado_St)):
    print(f"P(St+1={net.get_outcome_id('St_1', i)} | St, H, W, OW, HN, NE, PW, PH) = {distribucion_St1_dado_St[i]}")
elif (mode_of_use == "1"):
  net.clear_all_evidence()
  net.update_beliefs()
  net.set_evidence("H", "Alto")
  net.set_evidence("W", "Armado")
  net.set_evidence("OW", "Armado")
  net.set_evidence("HN", "SeOye")
  net.set_evidence("NE", "Si")
  net.set_evidence("PW", "Si")
  net.set_evidence("PH", "Si")
  net.update_beliefs()
  for _ in range(1000):
    net.update_beliefs()  
  distribucion_St_1_despues_iteraciones = net.get_node_value("St_1")
  outcomes = [net.get_outcome_id("St_1", i) for i in range(len(distribucion_St_1_despues_iteraciones))]
  print("Estado del bot después de 1000 iteraciones:")
  for outcome, probability in zip(outcomes, distribucion_St_1_despues_iteraciones):
    print(f"P(St_1={outcome}) = {probability}")
else:
  datos = open("data/datos_aprendizaje.txt", "r")
  nombres_tablas = datos.readline().split(",")
  # Eliminar el salto de línea
  nombres_tablas[-1] = nombres_tablas[-1][:-1]
  tablas = {}
  for nombre_tabla in nombres_tablas:
    tablas[nombre_tabla] = {}
  for linea in datos:
    valores = linea.split(",")
    for i in range(len(valores)):
      tablas[nombres_tablas[i]][valores[i]] = tablas[nombres_tablas[i]].get(valores[i], 0) + 1
  for tabla in tablas:
    total = sum(tablas[tabla].values())
    for valor in tablas[tabla]:
      tablas[tabla][valor] /= total
  tablas_condicionadas = {}
  for nombre_tabla in nombres_tablas:
    tablas_condicionadas[nombre_tabla] = {}
  for nombre_tabla in nombres_tablas:
    if (nombre_tabla == "St"):
      tablas_condicionadas[nombre_tabla] = tablas[nombre_tabla]
      continue
    if (nombre_tabla == "st_1"):
      for valor in tablas["St"]:
        tablas_condicionadas[nombre_tabla][valor] = {}
        for valor2 in tablas[nombre_tabla]:
          tablas_condicionadas[nombre_tabla][valor][valor2] = 0
    for valor in tablas["st_1"]:
      tablas_condicionadas[nombre_tabla][valor] = {}
      for valor2 in tablas[nombre_tabla]:
        tablas_condicionadas[nombre_tabla][valor][valor2] = 0
  datos.seek(0)
  datos.readline()
  for linea in datos:
    valores = linea.split(",")
    for i in range(len(valores)):
      if (i == 6):
        continue
      elif (i == 7):
        tablas_condicionadas[nombres_tablas[i]][valores[6]][valores[i]] += 1
      else:
        tablas_condicionadas[nombres_tablas[i]][valores[7]][valores[i]] += 1
  for nombre_tabla in nombres_tablas:
    if (nombre_tabla == "St"):
      continue
    if (nombre_tabla == "st_1"):
      for valor in tablas_condicionadas[nombre_tabla]:
        total = sum(tablas_condicionadas[nombre_tabla][valor].values())
        for valor2 in tablas_condicionadas[nombre_tabla][valor]:
          if (tablas_condicionadas[nombre_tabla][valor][valor2] == 0):
            continue
          tablas_condicionadas[nombre_tabla][valor][valor2] /= total
      continue
    for valor in tablas_condicionadas[nombre_tabla]:
      total = sum(tablas_condicionadas[nombre_tabla][valor].values())
      for valor2 in tablas_condicionadas[nombre_tabla][valor]:
        if (tablas_condicionadas[nombre_tabla][valor][valor2] == 0):
          continue
        tablas_condicionadas[nombre_tabla][valor][valor2] /= total
  for nombre_tabla in nombres_tablas:
    if (nombre_tabla == "St"):
      print(f"Tabla de {nombre_tabla}:")
      for valor in tablas[nombre_tabla]:
        print(f"P({nombre_tabla}={valor}) = {tablas[nombre_tabla][valor]}")
      continue
    elif (nombre_tabla == "st_1"):
      print(f"Tabla condicionada de {nombre_tabla} dado St:")
      for valor in tablas_condicionadas[nombre_tabla]:
        print(f"P({nombre_tabla}={valor} | St) = {tablas_condicionadas[nombre_tabla][valor]}")
      continue
    print(f"Tabla condicionada de {nombre_tabla} dado St + 1:")
    for valor in tablas_condicionadas[nombre_tabla]:
      print(f"P({nombre_tabla}={valor} | St) = {tablas_condicionadas[nombre_tabla][valor]}")