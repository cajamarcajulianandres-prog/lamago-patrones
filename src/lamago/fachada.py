"""PATRÓN FACADE: una sola llamada coordina paquete, inventario, extras, pago y logística."""
from dataclasses import dataclass, field
from itertools import count

from .builder import DirectorPaquetes
from .componentes import ComponenteDecoracion
from .decoradores import EXTRAS
from .inventario import Inventario


class SinDisponibilidad(Exception):
    pass


@dataclass
class Reserva:
    codigo: str
    cliente: str
    fecha: str
    paquete: ComponenteDecoracion
    total: int
    anticipo: int
    bitacora: list[str] = field(default_factory=list)


class ReservaFacade:
    _consecutivo = count(1)

    def __init__(self, inventario: Inventario):
        self._inventario = inventario

    def reservar(self, cliente: str, fecha: str, tema: str, invitados: int,
                 nivel: str = "basico", extras: list[str] | None = None,
                 presupuesto: int | None = None) -> Reserva:
        bitacora = []
        # 1. Builder + Composite
        builder = getattr(DirectorPaquetes, nivel)(tema, invitados)
        if presupuesto is not None:
            builder.con_presupuesto(presupuesto)
        paquete: ComponenteDecoracion = builder.construir()
        bitacora.append(f"Paquete armado: {paquete.nombre()}")

        # 2. Disponibilidad (a través del Proxy)
        faltantes = [a.codigo for a in paquete.articulos()
                     if self._inventario.disponible(a.codigo) < a.cantidad]
        if faltantes:
            raise SinDisponibilidad(f"Sin stock suficiente de: {', '.join(faltantes)}")
        bitacora.append("Disponibilidad confirmada")

        # 3. Decorator
        for clave in extras or []:
            paquete = EXTRAS[clave](paquete)
            bitacora.append(f"Extra agregado: {clave}")

        # 4. Pago y logística (simulados)
        total = paquete.precio()
        anticipo = total // 2
        bitacora.append(f"Anticipo del 50% registrado: ${anticipo:,}")
        bitacora.append(f"Entrega y montaje programados para {fecha}")

        return Reserva(f"LMG-{next(self._consecutivo):04d}", cliente, fecha,
                       paquete, total, anticipo, bitacora)
