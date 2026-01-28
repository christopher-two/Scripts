import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

# --- CONFIGURACIÓN ---
# Lista de URLs que deseas capturar
URLS = [
    "https://www.override.com.mx/",
    "https://logistics.override.com.mx/",
    "https://lerna.override.com.mx/",
    "https://mindstack.override.com.mx/",
    "https://dependency.christopher.com.mx/",
    "https://shop.override.com.mx/",
    "https://wasm.christopher.com.mx/cotizador/yazbek/",
    "https://eikocolors.atomo.click/",
    "https://charmstar.atomo.click/"
]

# Carpeta de destino y dimensiones de pantalla
OUTPUT_DIR = Path("/home/christopher/Imágenes/proyectos/webs")
VIEWPORT = {"width": 1920, "height": 1080}


async def capturar_sitio(browser, url):
    """Procesa la navegación y captura de una URL específica."""
    # Crear un contexto nuevo (como una pestaña aislada)
    context = await browser.new_context(viewport=VIEWPORT)
    page = await context.new_page()

    # Generar nombre de archivo limpio basado en la URL
    nombre_limpio = url.split("//")[-1].replace("/", "_").replace(".", "_")
    ruta_archivo = OUTPUT_DIR / f"{nombre_limpio}.png"

    try:
        print(f"Iniciando captura de: {url}...")

        # wait_until="networkidle" espera a que no haya tráfico de red por 500ms
        await page.goto(url, wait_until="networkidle", timeout=60000)

        # Tomar captura de pantalla completa (full_page=True)
        await page.screenshot(path=str(ruta_archivo), full_page=True)
        print(f"✓ Éxito: {url} -> {ruta_archivo}")

    except Exception as e:
        print(f"✗ Error al capturar {url}: {e}")
    finally:
        await context.close()


async def main():
    # Asegurar que la carpeta de salida exista
    OUTPUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        # Lanzar el navegador (Chromium es el más compatible)
        # headless=True significa que no se abrirá una ventana visible
        browser = await p.chromium.launch(headless=True)

        # Ejecutar todas las capturas simultáneamente
        tareas = [capturar_sitio(browser, url) for url in URLS]
        await asyncio.gather(*tareas)

        await browser.close()
        print("\nProceso finalizado. Revisa la carpeta 'capturas'.")


if __name__ == "__main__":
    asyncio.run(main())