# Diseño

## Clases principales
```mermaid
classDiagram
    class ComponenteDecoracion { <<abstract>> +nombre() +precio() +articulos() +descripcion() }
    class Articulo
    class Paquete { +agregar(c) }
    class ExtraDecorator { -envuelto }
    class IluminacionLED
    class MontajeProfesional
    class TransporteExpress
    class PaqueteBuilder { +con_tema() +agregar_articulo() +agregar_subpaquete() +construir() }
    class DirectorPaquetes { +basico() +premium() }
    class Inventario { <<abstract>> +disponible(codigo) }
    class InventarioReal
    class InventarioProxy { -cache, ttl }
    class ReservaFacade { +reservar() }

    ComponenteDecoracion <|-- Articulo
    ComponenteDecoracion <|-- Paquete
    ComponenteDecoracion <|-- ExtraDecorator
    ExtraDecorator <|-- IluminacionLED
    ExtraDecorator <|-- MontajeProfesional
    ExtraDecorator <|-- TransporteExpress
    Paquete o-- ComponenteDecoracion
    ExtraDecorator o-- ComponenteDecoracion
    Inventario <|-- InventarioReal
    Inventario <|-- InventarioProxy
    InventarioProxy o-- InventarioReal
    DirectorPaquetes ..> PaqueteBuilder
    PaqueteBuilder ..> Paquete
    ReservaFacade ..> DirectorPaquetes
    ReservaFacade ..> Inventario
    ReservaFacade ..> ExtraDecorator
```

## Flujo de `ReservaFacade.reservar()`
1. **Builder/Director** arma el paquete (**Composite**: mesas y sillas es un sub-paquete).
2. Por cada artículo del paquete se consulta el **Proxy**; si hay faltantes → `SinDisponibilidad`.
3. Se envuelven los extras con **Decorator**.
4. Se calcula total, anticipo (50 %) y se registra la bitácora.

## Decisiones
- Decorator y Composite comparten la interfaz `ComponenteDecoracion`, por eso un paquete decorado sigue siendo un componente válido.
- El proxy recibe el reloj por parámetro para poder probar la expiración sin esperas.
- Regla de mesas: 8 invitados por mesa, redondeando hacia arriba.
