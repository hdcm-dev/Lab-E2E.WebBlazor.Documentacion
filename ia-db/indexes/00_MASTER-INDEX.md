# 00 — Índice maestro

> **Propósito**: visión general del laboratorio Lab-E2E.WebBlazor —qué es, sus cinco aplicaciones y doce proyectos, el stack con versiones, los puertos, el devcontainer de Android, las decisiones que lo definen y los desfasajes documentales conocidos—, con el mapa hacia los índices que desarrollan cada tema.
>
> **Fuente primaria**: `README.md` (§Estructura, §La API, §La aplicación Android, §Diseño, §Cómo se corren, §Evidencia), `CHANGELOG.md`, `Lab-E2E.WebBlazor.sln`, `Lab-E2E.WebBlazor.SinMaui.slnf`, `src/*/*.csproj`, `tests/*/*.csproj`, `src/*/Properties/launchSettings.json`, `pruebas.runsettings`, `scripts/*.sh`, `.devcontainer/{Dockerfile,devcontainer.json,dev.sh}`, `.github/workflows/*.yml`, `.gitignore`, `evidencia/`; historia: `git log` de `7679135` a `8fb4c3a`.
>
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18).
>
> **Vecinos**: capas y composición en [01](01_Arquitectura.md) · dominio en [02](02_Dominio-Y-Reglas.md) · sesión y base en [03](03_Sesiones-Y-Persistencia.md) · pantallas web en [04](04_Interfaz-Y-Pantallas.md) · suites en [05](05_Pruebas.md) · workflows en [06](06_CI-Y-Workflows.md) · guías en [07](07_Guias.md) · porqué y trampas en [08](08_Decisiones-Y-Trampas.md) · términos en [09](09_Glosario.md) · Hola Mundo y Login en [10](10_Hola-Mundo-Y-Login.md) · template en [11](11_Template-Y-Superficies.md) · API en [12](12_Api-REST.md) · Android en [13](13_App-Android.md).

---

## 1. Qué es

Laboratorio para practicar **pruebas de extremo a extremo con Playwright** sobre una aplicación **.NET Blazor con render interactive server**, e integrarlas en la cadena de desarrollo con **GitHub Actions** (`README.md` líneas 1-5). Es el ejemplo de *movilidad urbana* de `Lab-E2E.StaticHtml` replanteado sobre una aplicación real: el estado vive en el servidor, en **SQLite**, y cada interacción viaja por el circuito de Blazor (`README.md` líneas 7-9). Con el tiempo sumó una API REST y una app Android de la misma temática, y dos webs más simples (Hola Mundo y Login) como escalones previos.

| Dato | Valor | Fuente |
| --- | --- | --- |
| Repositorio | `https://github.com/hdcm-dev/Lab-E2E.WebBlazor`, rama `main` (única rama remota) | `git remote -v`; [06](06_CI-Y-Workflows.md) §7 |
| Commit indexado | `8fb4c3a` (2026-09-18), árbol limpio | `git log -1`, `git status` |
| Historia | 45 commits, de `7679135` «Initial commit» (2026-08-23) a `8fb4c3a` | `git log` |
| Versión del producto | **No declarada**: sin `<Version>` en los `.csproj`, sin etiquetas git; el `CHANGELOG.md` agrupa por fecha bajo «[Sin publicar]» («un laboratorio que se lee y se corre entero, no un artefacto que alguien instala en una versión determinada», líneas 6-8). La app Android declara `ApplicationDisplayVersion 1.0` / `ApplicationVersion 1` | `CHANGELOG.md`; `git tag` vacío; `src/MovilidadUrbana.MAUI/MovilidadUrbana.MAUI.csproj` líneas 19-20 |
| Visibilidad | Público | API `/repos` ([06](06_CI-Y-Workflows.md) §5) |
| Documentación de estudio | Fuera del repo: `/LAB/Lab-Documentos/Lab-Documentos/Guides/Testing/Lab-E2E.WebBlazor-Guides/` (repo `hdcm-dev/Lab-Documentos`). Esta ia-db vive en `/LAB/Lab-E2E.WebBlazor/Lab-E2E.WebBlazor.Documentacion/` | [07](07_Guias.md) §1 |

---

## 2. Cinco aplicaciones

| Aplicación | Proyecto | Tipo | Capas | Persistencia | Sesión de datos | Índice |
| --- | --- | --- | --- | --- | --- | --- |
| Movilidad Urbana web | `src/MovilidadUrbana.Web` | Blazor Web App, Interactive Server (render mode en la raíz) | `Domain/`, `Application/`, `Infrastructure/` propias | SQLite `datos/movilidad.db` | cookie `sesion-movilidad` | [04](04_Interfaz-Y-Pantallas.md), [11](11_Template-Y-Superficies.md) |
| Movilidad Urbana API | `src/MovilidadUrbana.ApiWeb` | ASP.NET Core con controllers, OpenAPI + Scalar | ídem, copia propia | SQLite `datos/movilidad-api.db` | encabezado `X-Sesion-Id` | [12](12_Api-REST.md) |
| Movilidad Urbana Android | `src/MovilidadUrbana.MAUI` | .NET MAUI, XAML nativo + MVVM, solo `net10.0-android` | ídem + `Presentation/` | SQLite en `FileSystem.AppDataDirectory` | el dispositivo (`Preferences` `sesion-dispositivo`) | [13](13_App-Android.md) |
| Hola Mundo | `src/WebBlazor.HolaMundo` | Blazor, render por página | sin capas | ninguna | — | [10](10_Hola-Mundo-Y-Login.md) |
| Login | `src/WebBlazor.Login` | Blazor + autenticación por cookie (`auth_token`), login en SSR estático | sin capas | ninguna (identidad fija `admin`/`admin`) | — | [10](10_Hola-Mundo-Y-Login.md) |

- Las tres de Movilidad Urbana son **independientes**: ningún `.csproj` de `src/` tiene `ProjectReference` (en `tests/` solo `UnitTests` → Web y `ApiWeb.Tests` → ApiWeb, [01](01_Arquitectura.md) §7); el código de capas se repite a propósito («cada proyecto tiene que poder estudiarse, compilarse y llevarse por separado», `README.md` §Estructura). `Domain/` y `Application/` son idénticos salvo el namespace en las tres copias ([01](01_Arquitectura.md) §2.1, [02](02_Dominio-Y-Reglas.md) §1).
- Las tres webs forman una **escalera** de complejidad: Hola Mundo → Login → Movilidad Urbana, «para que la temática se pueda estudiar de a un escalón» (`README.md` líneas 80-84). Hola Mundo y Login llegaron byte a byte desde `Lab-E2E.WebBlazor.Base`, retirado (`11620e9`).
- Dominio común: un **ABM de localidades** y una **encuesta de transporte** en tres pasos ([02](02_Dominio-Y-Reglas.md)).

---

## 3. Doce proyectos

`Lab-E2E.WebBlazor.sln` tiene 17 entradas `Project(...)`: 12 `.csproj` y 5 carpetas de solución; `Lab-E2E.WebBlazor.SinMaui.slnf` lista 11, todos menos `src/MovilidadUrbana.MAUI`, y es lo que compila CI (sin workload de MAUI). Casos contados con `git grep '\[Test\]'` / `'\[TestCase'` sobre `tests/`.

| # | Proyecto | Rol | Casos | ¿En CI? | Índice |
| ---: | --- | --- | ---: | --- | --- |
| 1 | `src/MovilidadUrbana.Web` | App web | — | compila | [04](04_Interfaz-Y-Pantallas.md) |
| 2 | `src/MovilidadUrbana.ApiWeb` | App API | — | compila | [12](12_Api-REST.md) |
| 3 | `src/MovilidadUrbana.MAUI` | App Android | — | solo `android.yml` | [13](13_App-Android.md) |
| 4 | `src/WebBlazor.HolaMundo` | App web | — | compila | [10](10_Hola-Mundo-Y-Login.md) |
| 5 | `src/WebBlazor.Login` | App web | — | compila | [10](10_Hola-Mundo-Y-Login.md) |
| 6 | `tests/MovilidadUrbana.E2ETests` | Playwright sobre la web publicada (fixture propio) | 22 | `e2e.yml` | [05](05_Pruebas.md) §2 |
| 7 | `tests/MovilidadUrbana.UnitTests` | Reglas de dominio de la web | 49 (3 `[Test]` + 46 `[TestCase]`) | `ci.yml` | [05](05_Pruebas.md) §3 |
| 8 | `tests/MovilidadUrbana.ApiWeb.Tests` | API en proceso (`WebApplicationFactory`) | 13 | `ci.yml` | [12](12_Api-REST.md) §8 |
| 9 | `tests/MovilidadUrbana.MAUI.Tests` | ViewModels con capas enlazadas | 18 | `ci.yml`, `android.yml` | [13](13_App-Android.md) §8 |
| 10 | `tests/MovilidadUrbana.MAUI.UITests` | Appium sobre la app instalada | 5 | **no** (necesita teléfono) | [13](13_App-Android.md) §9 |
| 11 | `tests/WebBlazor.HolaMundo.E2ETests` | Playwright, sin fixture, URL fija `:5027` | 1 | `e2e-holamundo.yml` | [10](10_Hola-Mundo-Y-Login.md) §5 |
| 12 | `tests/WebBlazor.Login.E2ETests` | Playwright, sin fixture, URL fija `:5181` | 10 | `e2e-login.yml` | [10](10_Hola-Mundo-Y-Login.md) §5 |
| | **Total de casos** | | **118** | | |

Las cinco carpetas de solución son `src` y `tests` (los proyectos) y `github-workflow`, `scripts` y `Solution Items` (archivos sueltos) (`Lab-E2E.WebBlazor.sln`; `README.md` §La aplicación Android, último párrafo).

---

## 4. Stack con versiones

| Capa | Pieza | Versión | Fuente |
| --- | --- | --- | --- |
| Plataforma | .NET / `TargetFramework` | `net10.0` (todos) · `net10.0-android` (MAUI) | `*.csproj` |
| | SDK en CI | `actions/setup-dotnet@v6`, `dotnet-version: 10.0.x` (sin `global.json`) | `.github/workflows/*.yml` |
| | SDK en contenedor | `mcr.microsoft.com/dotnet/sdk:10.0` | `scripts/dotnet.sh` línea 9; `.devcontainer/Dockerfile` línea 9 |
| Web | Blazor Web App, Interactive Server; sin librería de componentes ni framework CSS (template del Framework SDD, `Tokens.css` + `Componentes.css`) | — | `README.md` líneas 15-24; [11](11_Template-Y-Superficies.md) |
| Datos | `Microsoft.EntityFrameworkCore.Sqlite` (Web, ApiWeb, MAUI, MAUI.Tests) | 10.0.11 | `*.csproj` |
| API | `Microsoft.AspNetCore.OpenApi` · `Scalar.AspNetCore` | 10.0.11 · 2.17.3 | `MovilidadUrbana.ApiWeb.csproj` |
| Android | `Microsoft.Maui.Controls` | `$(MauiVersion)` (la fija el workload: el repo no tiene `Directory.Build.props` ni `global.json`; **no verificado** qué versión resuelve) | `MovilidadUrbana.MAUI.csproj` línea 34 |
| | `CommunityToolkit.Mvvm` · `Microsoft.Extensions.Logging.Debug` | 8.4.2 · 10.0.11 | ídem |
| | Android SDK en la imagen | `platforms;android-36` y `android-35`, `build-tools` 36.0.0 y 35.0.0, cmdline-tools `13114758`, JDK 17; API mínima 23 | `.devcontainer/Dockerfile`; [13](13_App-Android.md) §7 |
| Pruebas | NUnit · NUnit3TestAdapter · NUnit.Analyzers · Microsoft.NET.Test.Sdk | 4.3.2 · 5.0.0 · 4.7.0 · 17.14.0 | `tests/*/*.csproj` |
| | `Microsoft.Playwright.NUnit` (las tres E2E) | 1.62.0 | ídem |
| | Imagen de `scripts/pruebas.sh` | `mcr.microsoft.com/playwright:v1.62.1-noble` (`VERSION_PLAYWRIGHT`) | `scripts/pruebas.sh` líneas 30-31 |
| | `Microsoft.AspNetCore.Mvc.Testing` | 10.0.11 | `MovilidadUrbana.ApiWeb.Tests.csproj` |
| | `Appium.WebDriver` · servidor Appium · driver | 8.0.0 · 3.7.0 · `uiautomator2@8.6.4` (las dos últimas sin versión fija en la imagen: son las del 2026-09-13) | `MovilidadUrbana.MAUI.UITests.csproj`; `evidencia/2026-09-13-uitests/README.md` |
| | `coverlet.collector` (tres E2E) | 6.0.4, sin uso observado | [05](05_Pruebas.md) §1 |
| CI | GitHub Actions: 6 workflows; `checkout@v7`, `upload-artifact@v7`, `download-artifact@v8`, `cache@v6`, `github-script@v9`, `setup-java@v6` | — | [06](06_CI-Y-Workflows.md) §10 |

---

## 5. Puertos y direcciones

| Qué | Dirección | Fuente |
| --- | --- | --- |
| Web Movilidad Urbana (`dotnet run`, perfil `http`) | `http://localhost:5232` | `src/MovilidadUrbana.Web/Properties/launchSettings.json` |
| Web bajo prueba E2E (fixture) | `http://127.0.0.1:<PUERTO>`, por defecto `4173`; o `URL_BASE` | `tests/MovilidadUrbana.E2ETests/Infrastructure/TestAppServer.cs`; [05](05_Pruebas.md) §8 |
| API (perfil `http`) | `http://localhost:5250`; OpenAPI `/openapi/v1.json` y Scalar `/scalar/v1` solo en Development | `src/MovilidadUrbana.ApiWeb/Properties/launchSettings.json`; [12](12_Api-REST.md) §7 |
| Hola Mundo | `http://localhost:5027` (perfil `https`: `https://localhost:7230;http://localhost:5027`) | `src/WebBlazor.HolaMundo/Properties/launchSettings.json` |
| Login | `http://localhost:5181` (perfil `https`: `https://localhost:7212;http://localhost:5181`) | `src/WebBlazor.Login/Properties/launchSettings.json` |
| Servidor Appium | `http://127.0.0.1:4723` (`APPIUM_URL`) | `tests/MovilidadUrbana.MAUI.UITests/Infrastructure/AppiumSession.cs` |
| Hosts de la evidencia del template | `http://app-holamundo:8080`, `http://app-login:8080` (cómo se levantaron no está versionado) | `evidencia/2026-09-01-aplicacion-template/verificar.mjs`; [10](10_Hola-Mundo-Y-Login.md) §5.5 |

Las URL de Hola Mundo y Login están escritas en la prueba y repetidas en `scripts/pruebas.sh` y en el `env` de sus workflows: tienen que coincidir ([10](10_Hola-Mundo-Y-Login.md) §5.1).

---

## 6. Devcontainer (solo para Android)

`.devcontainer/` existe para compilar, instalar y probar la app MAUI en un teléfono por USB sin SDK en el host. La web, la API y las pruebas web no lo usan: se corren con SDK local o con `scripts/dotnet.sh` / `scripts/pruebas.sh` (Docker).

| Pieza | Qué | Fuente |
| --- | --- | --- |
| Imagen | `mcr.microsoft.com/dotnet/sdk:10.0` + JDK 17 + Android SDK + workload `maui-android` + Node 22 + Appium (`uiautomator2`); usuario `dev` (UID 1000); `LANG=es_AR.UTF-8` | `.devcontainer/Dockerfile` |
| Contenedor | `lab-e2e-maui-dev` (imagen `lab-e2e-maui-dev:net10` con `dev.sh`), `--privileged`, `/dev/bus/usb`, repo en `/work` | `devcontainer.json`, `dev.sh` |
| Volúmenes | `lab-maui-nuget`, `gda-app-adbkeys` (clave adb compartida con GDA.Core.APP), `lab-maui-keystore` (keystore Debug persistente) | `devcontainer.json` |
| Dos caminos | VS Code *Reopen in Container* o `dev.sh up/devices/build/install/run/logs/uitests/down/devolver`; mismo nombre de contenedor, no conviven | [13](13_App-Android.md) §7 |
| Teléfono de la evidencia | Motorola moto e6 play, Android 9, armeabi-v7a (`ABI=android-arm` por defecto) | `evidencia/2026-09-12-maui/dispositivo.txt` |

Rastro: el encabezado del `Dockerfile` (línea 2) lo presenta como entorno de **GDA.Core.APP**, de donde se copió la receta (`devcontainer.json` líneas 2-3).

---

## 7. Árbol de primer nivel (versionado)

```
Lab-E2E.WebBlazor/
├── src/                     5 aplicaciones (§2)
├── tests/                   7 proyectos de prueba (§3)
├── scripts/                 dotnet.sh (SDK en contenedor) · publicar.sh (autocontenido linux-x64) · pruebas.sh (E2E en contenedor Playwright)
├── .github/workflows/       ci · e2e · e2e-holamundo · e2e-login · android · verificacion-entorno
├── .devcontainer/           Dockerfile · devcontainer.json · dev.sh (Android)
├── evidencia/               7 carpetas fechadas (2026-09-01 a 2026-09-13), 75 archivos versionados, 52 PNG
├── Lab-E2E.WebBlazor.sln    12 proyectos
├── Lab-E2E.WebBlazor.SinMaui.slnf   11 proyectos (lo que compila CI)
├── pruebas.runsettings      chromium · ExpectTimeout 5000 · Headless · 4 workers · resultados/
├── README.md · CHANGELOG.md · .gitignore
└── (ignorados, generados al correr) datos/, datos-e2e/, publicacion/, resultados/, .dotnet/, .navegadores/, .nuget/
```

Fuente: `ls`, `git ls-files`, `.gitignore`. No hay carpeta `docs/` (aunque `ci.yml` la ignora en `paths-ignore`, [06](06_CI-Y-Workflows.md) §2).

---

## 8. Historia en ocho hitos

| Fecha | Commit | Hito |
| --- | --- | --- |
| 2026-08-23 | `0516139` | Nace la web de Movilidad Urbana con capas como carpetas en español y E2E en JavaScript |
| 2026-08-23 | `90ad8fe` | Las E2E pasan a proyecto C# de la solución (`Microsoft.Playwright.NUnit`) |
| 2026-08-24 | `db775c5` | Jobs a `ubuntu-latest`; desde `4815823` (2026-09-03) `publicar` de `e2e.yml` vuelve al runner propio `i7infra-dev` |
| 2026-09-04 | `b0c828e` / `7a9edaa` | Template SDD en la interfaz web (reemplaza Bootstrap), PR #11 |
| 2026-09-12 | `11620e9`, `f9f3ca2`, `e0f3e9d` | Llegan Hola Mundo y Login; un workflow por web; https→http; se quita el prefijo `E2E.Base` |
| 2026-09-12 | `88e5caa` → `3b53d14` → `10ce735` | Nace la API (capas como proyectos), Scalar, y vuelta a apps independientes; nace la app MAUI y el devcontainer |
| 2026-09-13 | `3e119b8` | UITests con Appium: la solución llega a 12 proyectos (el `CHANGELOG.md` lo asienta dentro del bloque del 2026-09-12, línea 55) |
| 2026-09-18 | `946d023`, `e9dea2a`, `8fb4c3a` | Convención «arquitectura en inglés, dominio en español»; `cref` corregidos; README/CHANGELOG enlazan la guía de nomenclatura |

Detalle: [01](01_Arquitectura.md) §9, [06](06_CI-Y-Workflows.md) §5, [08](08_Decisiones-Y-Trampas.md).

---

## 9. Decisiones clave (el porqué completo en [08](08_Decisiones-Y-Trampas.md))

| # | Decisión | Por qué, en una línea | Desarrollo |
| ---: | --- | --- | --- |
| 1 | Tres apps de Movilidad Urbana independientes, código de capas repetido | Cada una se estudia, compila y lleva por separado; costo: una regla se cambia tres veces y nada compara las copias | [01](01_Arquitectura.md) §2.1 |
| 2 | Las E2E son proyecto C# de la solución, no specs de TypeScript | Descubrir y depurar desde el Explorador de pruebas de Visual Studio; se pierden `--shard` y el reporte HTML | [08](08_Decisiones-Y-Trampas.md) §1 |
| 3 | Se prueba el binario **publicado**, publicado e instalado el navegador desde el fixture | Probar lo que se despliega; con un target de MSBuild las pruebas morían en `OneTimeSetUp` | [05](05_Pruebas.md) §2.2 |
| 4 | Aislamiento por sesión sobre un solo servidor y un solo SQLite (cookie / `X-Sesion-Id` / dispositivo) | Pruebas en paralelo sin pisarse; no es seguridad | [03](03_Sesiones-Y-Persistencia.md) §1 |
| 5 | Render mode en la raíz de la web | La cookie solo se lee en `App.razor` y viaja como parámetro a `Routes` (puente al circuito) | [03](03_Sesiones-Y-Persistencia.md) §2 |
| 6 | Testigo de hidratación `estado-app[data-interactivo]` antes del primer click; `@bind:event="oninput"` | HTML prerenderizado que no responde; `FillAsync` dispara `input` | [08](08_Decisiones-Y-Trampas.md) §2 |
| 7 | `EnsureCreated` + WAL, sin migraciones | El binario arranca en cualquier máquina; un cambio de esquema obliga a borrar las bases | [03](03_Sesiones-Y-Persistencia.md) §9 |
| 8 | Template propio con tokens, sin Bootstrap; `<dialog>` nativo; resultados como banda | Una sola fuente de valor visual; la evidencia E2E no depende de temporizadores | [11](11_Template-Y-Superficies.md) |
| 9 | CI sobre `SinMaui.slnf`; jobs sin `container:`; solo `publicar` en el runner propio | El runner no tiene workload de MAUI ni socket de Docker | [06](06_CI-Y-Workflows.md) §5 |
| 10 | Hola Mundo y Login **sin fixture**, contra URL fija, en http | Escalón más simple; con https no corrían en CI sin certificado | [10](10_Hola-Mundo-Y-Login.md) §5 |
| 11 | Arquitectura en inglés, dominio en español; no se traducen texto visible, URL, contrato JSON, `data-testid`, `AutomationId` ni comentarios | Las pruebas y las guías citan esos literales | [01](01_Arquitectura.md) §8 |
| 12 | Las guías viven en otro repositorio | Una sola copia en vez de dos que divergen | [07](07_Guias.md) §1.1 |

---

## 10. Estado de verificación al 2026-10-25

| Afirmación | Respaldo | Estado |
| --- | --- | --- |
| 22 E2E web, 49 unitarias, 13 API, 18 ViewModels, 5 Appium, 1 + 10 Hola Mundo/Login | Conteo en `tests/` | Verificado (conteo) |
| Corridas en verde de E2E (22/22), API (13/13), Hola Mundo/Login, Appium (5/5) | Logs en `evidencia/` (todos del 2026-09-01 al 2026-09-13) | Verificado, **anterior** al renombre `946d023` |
| Verde completo tras el renombre | Solo el `CHANGELOG.md` 2026-09-18 | **No verificado** con log guardado |
| CI y regresión nocturna | 117 corridas observadas en la API pública de GitHub Actions; el cron sobre `main` (`8fb4c3a`) sigue en verde al 2026-10-25 | Observado ([06](06_CI-Y-Workflows.md) §6) |
| Ejecución desde Visual Studio | El README declara que no hay Windows ni VS en la máquina de evidencia | **No verificado** |
| Capturas de la web de Movilidad Urbana | No hay: las PNG son de Hola Mundo/Login (2026-09-01) y de Android | — ([04](04_Interfaz-Y-Pantallas.md) §9) |

---

## 11. Desfasajes documentales conocidos

Lo que la documentación del repo (o sus comentarios) afirma y el código o la evidencia contradicen. Cada fila remite al índice que tiene el detalle.

| # | Afirmación | Dónde | Lo verificado | Índice |
| ---: | --- | --- | --- | --- |
| 1 | Las guías viven en `Lab-E2E.WebBlazor.Documentacion/Guides/` | `README.md` líneas 103, 254-263; `CHANGELOG.md` líneas 9, 176 | Esos enlaces dan 404 desde `8f29d0e` (2026-10-01); las guías están en `hdcm-dev/Lab-Documentos`, `Guides/Testing/Lab-E2E.WebBlazor-Guides/` | [07](07_Guias.md) §4.1 |
| 2 | Enlaces relativos `../../IA/SDD/...` y `../Lab-E2E.StaticHtml` | `README.md` líneas 7, 17-19, 172-176 | No resuelven desde el clon; las bases existen en `/IA/SDD/IA.SDD/...`, `Lab-E2E.StaticHtml` no está en `/LAB` | [11](11_Template-Y-Superficies.md) §1, [08](08_Decisiones-Y-Trampas.md) §8 |
| 3 | «descubre las pruebas de los cinco proyectos» | `README.md` §Desde Visual Studio | Son siete proyectos de prueba; faltan MAUI.Tests (18) y UITests (5) | [05](05_Pruebas.md) §14 |
| 4 | «La solución queda en once proyectos» | `CHANGELOG.md` 2026-09-12 (línea 96) | Cierto en `10ce735`; con `3e119b8` son 12 | [01](01_Arquitectura.md) §10 |
| 5 | «la API 11/11» | `CHANGELOG.md` 2026-09-12 | `api-tests.log` muestra 13/13; la falsificación sí es sobre 11 | [05](05_Pruebas.md) §14 |
| 6 | El renombre no cambió el contrato JSON | `README.md` §Convención de nombres; `CHANGELOG.md` 2026-09-18; mensaje de `946d023` | `ValidacionDePasoDto.Errores` → `Errors`: el JSON pasa de `errores` a `errors` (deducido del código, sin corrida) | [12](12_Api-REST.md) §10 |
| 7 | El renombre no cambió el texto visible | `CHANGELOG.md` 2026-09-18 | «El **service** no respondió.» (`Localidades.razor` línea 29) y «El service no llegó a resolverlo» (`Error.razor` de Hola Mundo y Login) | [04](04_Interfaz-Y-Pantallas.md) §9, [10](10_Hola-Mundo-Y-Login.md) §7 |
| 8 | De los workflows «solo se validó la sintaxis YAML» | `README.md` §Evidencia (última línea) | 117 corridas reales observadas | [06](06_CI-Y-Workflows.md) §8 |
| 9 | Todos los jobs en `ubuntu-latest`, el propio comentado | cabecera de `e2e.yml` líneas 11-13 y 87-88 | `publicar` tiene activo `[self-hosted, i7infra-dev]` (línea 89) | [06](06_CI-Y-Workflows.md) §8 |
| 10 | `ci.yml` y `ci-ok` se atan a la protección de rama | `ci.yml` línea 1; guías | `main` tiene `protected: false` | [06](06_CI-Y-Workflows.md) §7 |
| 11 | El encabezado de sesión se declara en la documentación OpenAPI | `src/MovilidadUrbana.ApiWeb/Program.cs` líneas 35-37 | `AddOpenApi()` sin opciones ni transformadores; «OpenAPI 3.1» en README frente a `3.1.1` en la evidencia | [12](12_Api-REST.md) §7 |
| 12 | «Cada prueba deja los datos como los encontró» (UITests) | `README.md` §La aplicación Android | Vale para localidades; la encuesta registrada no se deshace | [13](13_App-Android.md) §12 |
| 13 | `corrida-b-5-de-5.trx` como evidencia | `evidencia/2026-09-13-uitests/README.md` | `*.trx` está en `.gitignore` (línea 67): no versionado | [05](05_Pruebas.md) §14 |
| 14 | Movilidad Urbana se levanta «en un puerto libre» | comentario de `scripts/pruebas.sh` líneas 18-19 | `TestAppServer` usa `PUERTO` o `4173` fijo | [05](05_Pruebas.md) §14 |
| 15 | Entorno «de GDA.Core.APP», `InvariantGlobalization=false`, condición a macOS | `.devcontainer/Dockerfile` líneas 2, 24, 56-57 | El `.csproj` de MAUI no tiene nada de eso | [13](13_App-Android.md) §12 |
| 16 | `Domain/Reglas`, `MovilidadUrbana.E2ETests.Infraestructura`, textos de enlace «Grilla», «Campo»… | `README.md` líneas 184-191, 224, 455 | Nombres previos al renombre `946d023` (rastros) | [01](01_Arquitectura.md) §8.3 |
| 17 | Guías con nombres viejos, «tres workflows», 50 enlaces al código rotos, `Testing/E2E-Guide/` copia previa al renombre | Lab-Documentos | Ver el relevamiento | [07](07_Guias.md) §3-§5 |

Inventario completo de rastros de nombres viejos (comentarios, mensajes, scripts): [01](01_Arquitectura.md) §8.3; los de la vista, [11](11_Template-Y-Superficies.md) §10; los de las pruebas, [05](05_Pruebas.md) §13.

---

## 12. Huecos abiertos que conviene conocer

| Hueco | Índice |
| --- | --- |
| Ninguna E2E navega a `/encuesta/2` ni `/encuesta/3`; `boton-procesando` y el `catch` del registro no se ejercitan (declarado en `CHANGELOG.md` 2026-09-04) | [05](05_Pruebas.md) §11 |
| 21 de los 84 `data-testid` de la web no los usa ninguna prueba (filtro, indisponible, cancelar…) | [04](04_Interfaz-Y-Pantallas.md) §7 |
| Validación más laxa que la política mostrada: provincia y localidad fuera de catálogo, largo máximo no aplicado, medios desconocidos | [02](02_Dominio-Y-Reglas.md) §8 |
| Las reglas de ApiWeb y MAUI no tienen unitarias propias; nada compara las tres copias | [01](01_Arquitectura.md) §2.1 |
| En Login, `<NotAuthorized>` es camino muerto: actúa el middleware de cookies y `sesion-requerida` nunca se muestra | [10](10_Hola-Mundo-Y-Login.md) §4 |
| `verificacion-entorno.yml` nunca se disparó; su input `entorno` no se usa | [06](06_CI-Y-Workflows.md) §3.6 |
