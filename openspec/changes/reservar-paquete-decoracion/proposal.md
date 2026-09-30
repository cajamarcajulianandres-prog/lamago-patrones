# Propuesta: Reserva de paquetes de decoración Lamago

## 1. Problema
Lamago alquila decoración para quinceañeras. Cada cliente pide algo distinto: un tema
(rosa y dorado, azul y plata, vintage), un número de invitados, un presupuesto y extras
(iluminación LED, montaje, transporte). Hoy el paquete se arma a mano y cada cotización
mezcla varias tareas: escoger artículos, calcular mesas y sillas según invitados, revisar
inventario y sumar el costo.

Problemas concretos al crear los objetos directamente:
1. Un paquete tiene muchas partes opcionales; un constructor con 10 parámetros es ilegible y propenso a errores.
2. Un paquete contiene artículos y también sub-paquetes (ej. "Mesas y sillas"); el código se llena de `if` para distinguirlos.
3. Los extras se combinan libremente (LED + montaje, solo transporte…); crear una clase por combinación es inviable.
4. Consultar el inventario es lento (hoja de cálculo / base de datos) y se repite para los mismos artículos.
5. El cliente solo quiere "reservar", pero internamente hay que coordinar armado, inventario, extras, pago y logística.

## 2. Patrón creacional seleccionado: Builder
`PaqueteBuilder` construye el paquete paso a paso (`con_tema`, `agregar_articulo`, `agregar_subpaquete`,
`con_presupuesto`) y valida en `construir()`. `DirectorPaquetes` guarda recetas (básico, premium).
**Ventaja frente a `new` directo:** evita constructores enormes, permite paquetes válidos por
pasos, centraliza validaciones (paquete vacío, presupuesto excedido) y reutiliza recetas.

## 3. Patrones estructurales seleccionados
| Patrón | Dónde | Qué problema resuelve |
|---|---|---|
| Composite | `Articulo`, `Paquete` | Tratar igual un artículo y un paquete con sub-paquetes (precio y artículos recursivos). |
| Decorator | `IluminacionLED`, `MontajeProfesional`, `TransporteExpress` | Agregar extras combinables sin modificar el paquete ni crear una clase por combinación. |
| Cache Proxy | `InventarioProxy` | Evitar consultas repetidas al inventario lento, con expiración (TTL). |
| Facade (apoyo) | `ReservaFacade` | Una sola operación `reservar()` que oculta la coordinación del subsistema. |

## Alcance
Incluye: armado, cotización, verificación de stock, extras y reserva simulada (pago y logística simulados).
Excluye: interfaz gráfica, base de datos real, pasarela de pagos real.
