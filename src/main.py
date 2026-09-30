"""Demo: python src/main.py"""
from lamago.fachada import ReservaFacade, SinDisponibilidad
from lamago.inventario import InventarioProxy, InventarioReal

STOCK = {"ARCO_GLOBOS": 2, "BACKDROP_15": 1, "MESA_REDONDA": 20, "MANTEL": 20,
         "SILLA_TIFFANY": 150, "CENTRO_MESA": 20, "CAMINO_FLORAL": 1, "TRONO_QUINCE": 1}

real = InventarioReal(STOCK, latencia=0.05)
proxy = InventarioProxy(real, ttl=60)
fachada = ReservaFacade(proxy)

print("=== Reserva 1: Paquete Premium con extras ===")
r1 = fachada.reservar("Familia Gómez", "2026-11-14", "rosa_dorado", 80,
                      nivel="premium", extras=["led", "montaje"])
print(*r1.paquete.descripcion(), sep="\n")
print(*r1.bitacora, sep="\n")
print(f"[{r1.codigo}] Total: ${r1.total:,} | Anticipo: ${r1.anticipo:,}\n")

print("=== Reserva 2: Paquete Básico (usa la caché) ===")
r2 = fachada.reservar("Familia Rojas", "2026-12-05", "azul_plata", 50)
print(f"[{r2.codigo}] Total: ${r2.total:,}\n")

print("=== Caché Proxy ===")
print(f"Consultas al inventario real: {real.consultas}")
print(f"Aciertos de caché: {proxy.aciertos} | Fallos: {proxy.fallos}\n")

print("=== Reserva 3: sin disponibilidad ===")
try:
    fachada.reservar("Familia Díaz", "2026-11-14", "vintage", 400)
except SinDisponibilidad as e:
    print("Error controlado:", e)
