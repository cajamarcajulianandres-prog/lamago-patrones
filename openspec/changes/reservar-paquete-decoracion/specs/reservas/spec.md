# Especificación: reservas

## ADDED Requirements

### Requirement: Construcción de paquetes con Builder
El sistema SHALL construir paquetes de decoración paso a paso mediante `PaqueteBuilder`.

#### Scenario: Paquete válido
- **WHEN** se agrega el artículo `ARCO_GLOBOS` y se llama `construir()`
- **THEN** se obtiene un paquete cuyo precio es 280.000

#### Scenario: Paquete vacío
- **WHEN** se llama `construir()` sin componentes
- **THEN** el sistema lanza `ValueError`

#### Scenario: Presupuesto excedido
- **WHEN** el precio supera el presupuesto indicado con `con_presupuesto`
- **THEN** el sistema lanza `PresupuestoExcedido`

### Requirement: Paquetes jerárquicos con Composite
El sistema SHALL calcular precio y lista de artículos de un paquete que contiene artículos y sub-paquetes, de forma recursiva.

#### Scenario: Precio recursivo
- **WHEN** un paquete contiene un sub-paquete (2 x 100) y un artículo (1 x 50)
- **THEN** su precio es 250 y contiene 2 artículos

### Requirement: Extras con Decorator
El sistema SHALL permitir agregar extras (LED 150.000, montaje 200.000, transporte 80.000) sobre un paquete sin modificar el paquete original.

#### Scenario: Extras combinados
- **WHEN** se decoran un paquete con LED y montaje
- **THEN** el precio es el del paquete + 350.000 y el paquete original conserva su precio

### Requirement: Caché de disponibilidad con Proxy
El sistema SHALL reutilizar una consulta de disponibilidad durante el TTL configurado.

#### Scenario: Acierto de caché
- **WHEN** se consulta dos veces el mismo artículo dentro del TTL
- **THEN** el inventario real se consulta una sola vez (1 acierto, 1 fallo)

#### Scenario: Expiración
- **WHEN** pasa más tiempo que el TTL entre dos consultas
- **THEN** el inventario real se consulta de nuevo

### Requirement: Reserva con Facade
El sistema SHALL ofrecer una operación `reservar()` que arme el paquete, verifique stock, aplique extras y registre un anticipo del 50 %.

#### Scenario: Reserva exitosa
- **WHEN** hay stock suficiente
- **THEN** se devuelve una reserva con código `LMG-####`, total y anticipo igual a la mitad del total

#### Scenario: Sin disponibilidad
- **WHEN** algún artículo no tiene stock suficiente
- **THEN** el sistema lanza `SinDisponibilidad` indicando los códigos faltantes

## Criterios de aceptación
1. Las 9 pruebas de `tests/test_patrones.py` pasan (`python -m unittest discover -s tests -t .`).
2. `python src/main.py` muestra: reserva premium con extras, reserva básica que aprovecha la caché, contadores del proxy y un error controlado por falta de stock.
3. Cada patrón está implementado en su propio módulo y puede identificarse por su docstring.
4. Ninguna clase cliente crea paquetes con `Paquete(...)` directamente: lo hace siempre el Builder.
