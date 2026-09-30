"""PATRÓN (CACHE) PROXY: el proxy guarda en caché las consultas de disponibilidad."""
from abc import ABC, abstractmethod
import time


class Inventario(ABC):
    @abstractmethod
    def disponible(self, codigo: str) -> int: ...


class InventarioReal(Inventario):
    """Simula una consulta lenta (base de datos / hoja de cálculo del negocio)."""

    def __init__(self, stock: dict[str, int], latencia: float = 0.0):
        self._stock = dict(stock)
        self._latencia = latencia
        self.consultas = 0  # cuántas veces se fue realmente al "origen"

    def disponible(self, codigo: str) -> int:
        self.consultas += 1
        time.sleep(self._latencia)
        return self._stock.get(codigo, 0)


class InventarioProxy(Inventario):
    def __init__(self, real: Inventario, ttl: float = 60.0, reloj=time.monotonic):
        self._real = real
        self._ttl = ttl
        self._reloj = reloj
        self._cache: dict[str, tuple[int, float]] = {}
        self.aciertos = 0
        self.fallos = 0

    def disponible(self, codigo: str) -> int:
        ahora = self._reloj()
        if codigo in self._cache:
            valor, guardado = self._cache[codigo]
            if ahora - guardado < self._ttl:
                self.aciertos += 1
                return valor
        self.fallos += 1
        valor = self._real.disponible(codigo)
        self._cache[codigo] = (valor, ahora)
        return valor

    def invalidar(self) -> None:
        self._cache.clear()
