"""PATRÓN COMPOSITE: un artículo suelto y un paquete se tratan igual."""
from __future__ import annotations
from abc import ABC, abstractmethod


class ComponenteDecoracion(ABC):
    @abstractmethod
    def nombre(self) -> str: ...

    @abstractmethod
    def precio(self) -> int: ...

    @abstractmethod
    def articulos(self) -> list["Articulo"]:
        """Todos los artículos (hojas) contenidos, para revisar inventario."""

    @abstractmethod
    def descripcion(self, nivel: int = 0) -> list[str]: ...


class Articulo(ComponenteDecoracion):
    """Hoja del Composite."""

    def __init__(self, codigo: str, nombre: str, precio_unitario: int, cantidad: int = 1):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        self.codigo = codigo
        self._nombre = nombre
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad

    def nombre(self) -> str:
        return self._nombre

    def precio(self) -> int:
        return self.precio_unitario * self.cantidad

    def articulos(self) -> list["Articulo"]:
        return [self]

    def descripcion(self, nivel: int = 0) -> list[str]:
        return [f"{'  ' * nivel}- {self.cantidad} x {self._nombre}: ${self.precio():,}"]


class Paquete(ComponenteDecoracion):
    """Nodo compuesto: puede contener artículos u otros paquetes."""

    def __init__(self, nombre: str):
        self._nombre = nombre
        self._hijos: list[ComponenteDecoracion] = []

    def agregar(self, componente: ComponenteDecoracion) -> None:
        self._hijos.append(componente)

    def hijos(self) -> list[ComponenteDecoracion]:
        return list(self._hijos)

    def nombre(self) -> str:
        return self._nombre

    def precio(self) -> int:
        return sum(h.precio() for h in self._hijos)

    def articulos(self) -> list[Articulo]:
        return [a for h in self._hijos for a in h.articulos()]

    def descripcion(self, nivel: int = 0) -> list[str]:
        lineas = [f"{'  ' * nivel}+ {self._nombre}: ${self.precio():,}"]
        for h in self._hijos:
            lineas += h.descripcion(nivel + 1)
        return lineas
