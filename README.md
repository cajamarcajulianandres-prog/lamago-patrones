# Lamago – Builder + Composite + Decorator + Cache Proxy (+ Facade)

Actividad de Patrones de Diseño de Software – UNINPAHU.

## Problema
Lamago es un negocio familiar de alquiler de decoración para quinceañeras en Bogotá. Cada cliente
pide tema, número de invitados, presupuesto y extras distintos. El sistema debe armar el paquete,
revisar inventario (consulta lenta), aplicar extras y registrar la reserva sin que el cliente vea esa complejidad.

## Patrones usados
| Tipo | Patrón | Clase(s) | Para qué |
|---|---|---|---|
| Creacional | **Builder** | `PaqueteBuilder`, `DirectorPaquetes` | Armar paquetes paso a paso y validarlos |
| Estructural | **Composite** | `Articulo`, `Paquete` | Paquetes con artículos y sub-paquetes |
| Estructural | **Decorator** | `IluminacionLED`, `MontajeProfesional`, `TransporteExpress` | Extras combinables |
| Estructural | **Cache Proxy** | `InventarioProxy` | Cachear disponibilidad con TTL |
| Estructural (apoyo) | **Facade** | `ReservaFacade` | `reservar()` como única entrada |

## Estructura
```
openspec/   Especificación SDD (problema, requisitos, patrones, diseño, criterios de aceptación)
src/        Código (paquete lamago/ y main.py)
tests/      Pruebas unitarias
```
La especificación está en `openspec/changes/reservar-paquete-decoracion/`.

## Cómo ejecutar
Requiere Python 3.10 o superior (sin dependencias externas).
```bash
python src/main.py                               # demo
python -m unittest discover -s tests -t .        # pruebas
```

## Qué demuestra la salida
- Una reserva premium con sub-paquete y extras (Builder + Composite + Decorator).
- Una segunda reserva que reutiliza la caché (Proxy): el contador muestra aciertos vs. consultas reales.
- Un error controlado por falta de stock (Facade).
