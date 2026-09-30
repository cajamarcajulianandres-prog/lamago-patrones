import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lamago.builder import DirectorPaquetes, PaqueteBuilder, PresupuestoExcedido
from lamago.componentes import Articulo, Paquete
from lamago.decoradores import IluminacionLED, MontajeProfesional
from lamago.fachada import ReservaFacade, SinDisponibilidad
from lamago.inventario import InventarioProxy, InventarioReal

STOCK = {"ARCO_GLOBOS": 2, "MESA_REDONDA": 20, "MANTEL": 20, "SILLA_TIFFANY": 150,
         "CENTRO_MESA": 20, "BACKDROP_15": 1, "TRONO_QUINCE": 1, "CAMINO_FLORAL": 1}


class TestBuilder(unittest.TestCase):
    def test_construye_paso_a_paso(self):
        p = PaqueteBuilder().con_tema("vintage").agregar_articulo("ARCO_GLOBOS").construir()
        self.assertEqual(p.precio(), 280_000)

    def test_paquete_vacio_falla(self):
        with self.assertRaises(ValueError):
            PaqueteBuilder().construir()

    def test_presupuesto_excedido(self):
        with self.assertRaises(PresupuestoExcedido):
            PaqueteBuilder().con_presupuesto(1000).agregar_articulo("ARCO_GLOBOS").construir()


class TestComposite(unittest.TestCase):
    def test_precio_recursivo(self):
        sub = Paquete("sub"); sub.agregar(Articulo("A", "a", 100, 2))
        raiz = Paquete("raiz"); raiz.agregar(sub); raiz.agregar(Articulo("B", "b", 50))
        self.assertEqual(raiz.precio(), 250)
        self.assertEqual(len(raiz.articulos()), 2)


class TestDecorator(unittest.TestCase):
    def test_extras_suman_y_no_modifican_el_original(self):
        base = DirectorPaquetes.basico("rosa_dorado", 16).construir()
        antes = base.precio()
        decorado = MontajeProfesional(IluminacionLED(base))
        self.assertEqual(decorado.precio(), antes + 150_000 + 200_000)
        self.assertEqual(base.precio(), antes)


class TestCacheProxy(unittest.TestCase):
    def test_segunda_consulta_usa_cache(self):
        real = InventarioReal(STOCK)
        proxy = InventarioProxy(real, ttl=60)
        proxy.disponible("ARCO_GLOBOS"); proxy.disponible("ARCO_GLOBOS")
        self.assertEqual(real.consultas, 1)
        self.assertEqual((proxy.aciertos, proxy.fallos), (1, 1))

    def test_cache_expira(self):
        t = [0.0]
        real = InventarioReal(STOCK)
        proxy = InventarioProxy(real, ttl=10, reloj=lambda: t[0])
        proxy.disponible("ARCO_GLOBOS"); t[0] = 11
        proxy.disponible("ARCO_GLOBOS")
        self.assertEqual(real.consultas, 2)


class TestFacade(unittest.TestCase):
    def setUp(self):
        self.real = InventarioReal(STOCK)
        self.f = ReservaFacade(InventarioProxy(self.real))

    def test_reserva_completa(self):
        r = self.f.reservar("Ana", "2026-11-14", "rosa_dorado", 80,
                            nivel="premium", extras=["led"])
        self.assertEqual(r.anticipo, r.total // 2)
        self.assertTrue(r.codigo.startswith("LMG-"))

    def test_sin_disponibilidad(self):
        with self.assertRaises(SinDisponibilidad):
            self.f.reservar("Ana", "2026-11-14", "vintage", 400)


if __name__ == "__main__":
    unittest.main()
