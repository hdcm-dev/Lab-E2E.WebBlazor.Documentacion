# 09 — Glosario

> **Propósito**: fijar el vocabulario del laboratorio, incluidos los términos propios del binding de
> .NET de Playwright que no coinciden con los del runner de JavaScript.
> **Fuente primaria**: código y `README.md` del repositorio.
> **Vigencia**: 2026-09-12, commit `10ce735`.

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
| **Testigo de interactividad (o de hidratación)** | El elemento con `data-testid="estado-app"` y `data-interactivo`, que pasa a `true` cuando el circuito quedó conectado. En Movilidad Urbana es un `div hidden` del layout; en Hola Mundo y Login, un `span` de la superficie |
| **Estado de superficie** | Uno de los desenlaces excluyentes de una pantalla, del vocabulario `EstadoDeSuperficie` del template: `Vacio`, `Cargando`, `ConDatos`, `ErrorDeEntrada`… Ver [11](11_Template-Y-Superficies.md) |
| **Superficie** | Una pantalla que promete algo verificable. Tres pasos de un asistente son **una** superficie si ningún paso promete nada por sí solo (`Caso-Encuesta-Page.md`) |
| **Guard** | Lo que decide si alguien pasa a una superficie protegida. Solo existe en Login — ver [10](10_Hola-Mundo-Y-Login.md) |
| **Sesión** | El espacio de datos de un visitante: la cookie `sesion-movilidad` en la web, el encabezado `X-Sesion-Id` en la API, el dispositivo entero en Android. Cada prueba estrena la suya |
| **Aplicación independiente** | Cada una de las tres de Movilidad Urbana —web, API, Android—, que lleva sus propias copias de `Dominio/`, `Aplicacion/` e `Infraestructura/` y no referencia a otro proyecto. No hay proyecto compartido, a propósito |
| **Cabeza** | Término usado en el `CHANGELOG.md` del 2026-09-12 para la web y la API como presentaciones sobre las mismas capas; desde `10ce735` cada «cabeza» es una aplicación independiente |
| **Sesión del dispositivo** | En Android, el identificador único generado la primera vez y guardado en `Preferences` (`sesion-dispositivo`); el único ámbito de DI de la app lo lleva puesto |
| **ViewModel** | En la app Android, la clase de `Presentacion/` que expone estado y comandos a una página XAML (CommunityToolkit.Mvvm). Se prueba sin teléfono con dobles de `INavegador` e `IAvisos` |
| **Archivos enlazados** | `<Compile Include="..\..\src\…" LinkBase="…">`: la forma en que `MovilidadUrbana.MAUI.Tests` compila las capas de la app sin referenciar el proyecto `net10.0-android` |
| **Workload** | El paquete `maui-android` del SDK de .NET que hace compilable `net10.0-android`. Solo lo tienen el devcontainer y `android.yml`; el runner de `ci.yml` no |
| **Filtro de solución (`.slnf`)** | `Lab-E2E.WebBlazor.SinMaui.slnf`: la solución sin la app Android, para compilar donde no está el workload |
| **ABI** | Arquitectura del APK: `android-arm` (armeabi-v7a, la del teléfono de prueba) por defecto en `dev.sh`; `ABI=android-arm64` para 64 bits |
| **Devcontainer** | `.devcontainer/`: imagen `lab-e2e-maui-dev:net10` con SDK 10, JDK 17, Android SDK y el workload; `dev.sh` la maneja desde el host y toma el `adb` del teléfono USB |
| **Siembra** | El juego inicial de localidades —Corrientes y Resistencia— que recibe cada sesión la primera vez |
| **Apphost** | El ejecutable nativo que produce `dotnet publish`: `MovilidadUrbana.Web.exe` en Windows, sin extensión en Linux y macOS |
| **Publicación autocontenida** | La que incluye el runtime de .NET; es la que usa CI, para no depender del runtime del ejecutor |
| **TRX** | El formato de reporte de resultados de `dotnet test`. Reemplaza al reporte HTML de `@playwright/test` |
| **Traza** | El `.zip` de Playwright con DOM paso a paso, red y consola. Se conserva solo en los casos fallidos, en `resultados/trazas/` |
| **`data-testid`** | El atributo con el que las pruebas ubican los elementos. Nunca se localiza por clase CSS ni por texto de estilo |
| **Puerta** | En el pipeline, la verificación que bloquea un merge. Acá la puerta es el check `ci-ok` |
| **Workflow reutilizable** | Uno invocable con `uses:` desde otro workflow (`workflow_call`). Acá es `e2e.yml` |
| **Runner autoalojado** | El runner propio del laboratorio, etiquetado `i7infra-dev`. Activo solo en el job `publicar` de `e2e.yml`; en los demás jobs queda comentado |
| **Falsificación** | Correr una prueba en condiciones en que **debe** fallar —sin la aplicación levantada— para demostrar que no pasa en vacío. Registros `*-falsificacion-*.log` en `evidencia/` |
| **Modelo adoptado** | Tronco con ramas de release, documentado en §6 de `Guides/Estandares-Modelo-Ramas.md`, en `Lab-E2E.WebBlazor.Documentacion`. **No** es GitFlow |
