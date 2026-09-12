# 09 — Glosario

> **Propósito**: fijar el vocabulario del laboratorio, incluidos los términos propios del binding de
> .NET de Playwright que no coinciden con los del runner de JavaScript.
> **Fuente primaria**: código y `README.md` del repositorio.
> **Vigencia**: 2026-09-12, commit `7262395`.

| Término | Qué significa acá |
| --- | --- |
| **E2E** | Prueba de extremo a extremo: ejercita la aplicación desde la interfaz, con navegador real y servidor levantado |
| **Configuración** | Una combinación de navegador y emulación: `chromium`, `firefox`, `webkit`, `mobile-chrome`. Es el equivalente de un *project* del `playwright.config.js` |
| **`mobile-chrome`** | No es un navegador: es chromium con el descriptor de dispositivo `Pixel 7` (`EMULAR_MOVIL=true`) |
| **Fixture** | En NUnit, la clase que agrupa casos. `[SetUpFixture]` es el que corre una vez por namespace: en Movilidad Urbana levanta y baja la aplicación. Hola Mundo y Login **no tienen**: la aplicación la levanta quien corre la prueba |
| **`ParallelScope.Fixtures`** | Las clases de prueba corren en paralelo entre sí; los casos de cada clase, en secuencia |
| **Worker** | Cada hilo de ejecución de NUnit. La cantidad vive en `NumberOfTestWorkers` del `.runsettings` |
| **Circuito** | La conexión WebSocket entre el navegador y el servidor en Blazor *interactive server*. Sin circuito la página se ve pero no responde |
| **Prerender** | El HTML que el servidor entrega antes de establecer el circuito |
| **Testigo de interactividad** | El elemento con `data-testid="estado-app"` y `data-interactivo`, que pasa a `true` cuando el circuito quedó conectado. En Movilidad Urbana es un `div` del layout; en Hola Mundo y Login, un `span` de la superficie |
| **Estado de superficie** | Uno de los desenlaces excluyentes de una pantalla, del vocabulario `EstadoDeSuperficie` del template: `Vacio`, `Cargando`, `ConDatos`, `ErrorDeEntrada`… Ver [11](11_Template-Y-Superficies.md) |
| **Guard** | Lo que decide si alguien pasa a una superficie protegida. Solo existe en Login — ver [10](10_Hola-Mundo-Y-Login.md) |
| **Sesión** | El espacio de datos de un visitante, identificado por la cookie `sesion-movilidad`. Cada prueba estrena la suya |
| **Siembra** | El juego inicial de localidades —Corrientes y Resistencia— que recibe cada sesión la primera vez |
| **Apphost** | El ejecutable nativo que produce `dotnet publish`: `MovilidadUrbana.Web.exe` en Windows, sin extensión en Linux y macOS |
| **Publicación autocontenida** | La que incluye el runtime de .NET; es la que usa CI, para no depender del runtime del ejecutor |
| **TRX** | El formato de reporte de resultados de `dotnet test`. Reemplaza al reporte HTML de `@playwright/test` |
| **Traza** | El `.zip` de Playwright con DOM paso a paso, red y consola. Se conserva solo en los casos fallidos, en `resultados/trazas/` |
| **`data-testid`** | El atributo con el que las pruebas ubican los elementos. Nunca se localiza por clase CSS ni por texto de estilo |
| **Puerta** | En el pipeline, la verificación que bloquea un merge. Acá la puerta es el check `ci-ok` |
| **Workflow reutilizable** | Uno invocable con `uses:` desde otro workflow (`workflow_call`). Acá es `e2e.yml` |
| **Runner autoalojado** | El runner propio del laboratorio, etiquetado `i7infra-dev`. Activo solo en el job `publicar` de `e2e.yml`; en los demás jobs queda comentado |
| **Modelo adoptado** | Tronco con ramas de release, documentado en el bloque «Modelo adoptado» de `Guides/Estandares-Modelo-Ramas.md`, en `Lab-E2E.WebBlazor.Documentacion`. **No** es GitFlow |
