"""PATRÓN DECORATOR: extras que se 'envuelven' sobre un paquete sin modificarlo."""
from .componentes import Articulo, ComponenteDecoracion


class ExtraDecorator(ComponenteDecoracion):
    etiqueta = "Extra"
    costo = 0

    def __init__(self, envuelto: ComponenteDecoracion):
        self._envuelto = envuelto

    def nombre(self) -> str:
        return f"{self._envuelto.nombre()} + {self.etiqueta}"

    def precio(self) -> int:
        return self._envuelto.precio() + self.costo

    def articulos(self) -> list[Articulo]:
        return self._envuelto.articulos()

    def descripcion(self, nivel: int = 0) -> list[str]:
        return self._envuelto.descripcion(nivel) + [
            f"{'  ' * nivel}* Extra {self.etiqueta}: ${self.costo:,}"
        ]


class IluminacionLED(ExtraDecorator):
    etiqueta = "Iluminación LED"
    costo = 150_000


class MontajeProfesional(ExtraDecorator):
    etiqueta = "Montaje profesional"
    costo = 200_000


class TransporteExpress(ExtraDecorator):
    etiqueta = "Transporte express"
    costo = 80_000


EXTRAS = {
    "led": IluminacionLED,
    "montaje": MontajeProfesional,
    "transporte": TransporteExpress,
}
