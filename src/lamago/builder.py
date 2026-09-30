"""PATRÓN BUILDER: arma un Paquete paso a paso, validando al final."""
from .catalogo import CATALOGO, TEMAS
from .componentes import Articulo, ComponenteDecoracion, Paquete


class PresupuestoExcedido(Exception):
    pass


class PaqueteBuilder:
    def __init__(self):
        self._nombre = "Paquete personalizado"
        self._tema = None
        self._presupuesto = None
        self._hijos: list[ComponenteDecoracion] = []

    def con_nombre(self, nombre: str) -> "PaqueteBuilder":
        self._nombre = nombre
        return self

    def con_tema(self, tema: str) -> "PaqueteBuilder":
        if tema not in TEMAS:
            raise ValueError(f"Tema desconocido: {tema}")
        self._tema = tema
        return self

    def con_presupuesto(self, maximo: int) -> "PaqueteBuilder":
        self._presupuesto = maximo
        return self

    def agregar_articulo(self, codigo: str, cantidad: int = 1) -> "PaqueteBuilder":
        if codigo not in CATALOGO:
            raise ValueError(f"Artículo desconocido: {codigo}")
        nombre, precio = CATALOGO[codigo]
        self._hijos.append(Articulo(codigo, nombre, precio, cantidad))
        return self

    def agregar_subpaquete(self, sub: Paquete) -> "PaqueteBuilder":
        self._hijos.append(sub)
        return self

    def construir(self) -> Paquete:
        if not self._hijos:
            raise ValueError("El paquete debe tener al menos un componente")
        etiqueta = f" ({TEMAS[self._tema]})" if self._tema else ""
        paquete = Paquete(self._nombre + etiqueta)
        for h in self._hijos:
            paquete.agregar(h)
        if self._presupuesto is not None and paquete.precio() > self._presupuesto:
            raise PresupuestoExcedido(
                f"Precio ${paquete.precio():,} supera el presupuesto ${self._presupuesto:,}"
            )
        return paquete


class DirectorPaquetes:
    """Recetas predefinidas que reutilizan el builder."""

    @staticmethod
    def mesas_y_sillas(invitados: int) -> Paquete:
        mesas = max(1, -(-invitados // 8))  # 8 personas por mesa, redondeo hacia arriba
        return (PaqueteBuilder().con_nombre("Mesas y sillas")
                .agregar_articulo("MESA_REDONDA", mesas)
                .agregar_articulo("MANTEL", mesas)
                .agregar_articulo("SILLA_TIFFANY", invitados)
                .agregar_articulo("CENTRO_MESA", mesas)
                .construir())

    @classmethod
    def basico(cls, tema: str, invitados: int) -> PaqueteBuilder:
        return (PaqueteBuilder().con_nombre("Paquete Básico").con_tema(tema)
                .agregar_subpaquete(cls.mesas_y_sillas(invitados))
                .agregar_articulo("ARCO_GLOBOS"))

    @classmethod
    def premium(cls, tema: str, invitados: int) -> PaqueteBuilder:
        return (cls.basico(tema, invitados).con_nombre("Paquete Premium")
                .agregar_articulo("BACKDROP_15")
                .agregar_articulo("TRONO_QUINCE")
                .agregar_articulo("CAMINO_FLORAL"))
