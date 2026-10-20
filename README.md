\# El deterioro de tu sueldo



Programa de consola en Python que proyecta, a 12 meses, cuánto del sueldo

queda disponible después de pagar créditos, comparando el aumento salarial

por paritarias con las tasas de interés de los créditos.



Trabajo final de Informática — Delfina Magi.



\## Qué hace



\- Permite elegir el gremio y toma su aumento mensual desde `paritarias.txt`.

\- Carga el sueldo neto y uno o más créditos (banco, tipo, monto, cuotas, mora).

\- Muestra un cash flow mes a mes con alertas si el disponible cae bajo el 40%

&#x20; o si las cuotas superan el sueldo.

\- Compara el aumento salarial acumulado con la TNA promedio de los créditos.

\- Guarda un resumen de cada simulación en `registros.csv`.



\## Cómo ejecutarlo



Requiere Python 3. Desde la carpeta del proyecto:



&#x20;   python flujo\_de\_caja\_trabajo\_final.py



Los archivos `paritarias.txt` y `tasas\_bancos.txt` deben estar en la misma carpeta.



\## Archivos



| Archivo | Contenido |

|---|---|

| `flujo\_de\_caja\_trabajo\_final.py` | Programa principal |

| `paritarias.txt` | Aumento mensual aproximado por gremio (formato `nombre;porcentaje`) |

| `tasas\_bancos.txt` | TNA de préstamos personales por banco (formato `banco;tna`) |



\## Limitaciones



\- La cuota se calcula con interés simple sobre el capital, no con sistema francés.

\- La mora se calcula como TNA/365 por día sobre el saldo vencido, con meses de 30 días.

\- Los porcentajes de paritarias y las tasas son valores aproximados de 2026 cargados a mano.

