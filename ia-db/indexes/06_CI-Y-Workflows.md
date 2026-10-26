# 06 — CI y workflows

> **Propósito**: qué hace cada uno de los seis workflows de GitHub Actions del laboratorio, qué los dispara, en qué runner corre cada job, cómo se encadenan, y qué corridas se observaron realmente en la API pública de GitHub Actions.
> **Fuente primaria**: `.github/workflows/ci.yml`, `.github/workflows/e2e.yml`, `.github/workflows/e2e-holamundo.yml`, `.github/workflows/e2e-login.yml`, `.github/workflows/android.yml`, `.github/workflows/verificacion-entorno.yml`, `pruebas.runsettings`, `scripts/publicar.sh`, `Lab-E2E.WebBlazor.SinMaui.slnf`, `README.md` (§«Los workflows», §«Runner»), `CHANGELOG.md`, `git log -- .github/workflows`; y la API pública `https://api.github.com/repos/hdcm-dev/Lab-E2E.WebBlazor/actions/…` (runs, jobs, annotations, artifacts, branches), consultada el 2026-10-25.
> **Vigencia**: versión 3.1, generada el 2026-10-25 sobre el commit `8fb4c3a` (2026-09-18). Las corridas están fechadas al 2026-10-25.
> **Vecinos**: qué prueba cada suite que estos workflows corren → [05](05_Pruebas.md); la compilación Android fuera de CI (devcontainer) → [13](13_App-Android.md); las pruebas sin fixture de Hola Mundo y Login → [10](10_Hola-Mundo-Y-Login.md); por qué se decidió así y qué no revertir → [08](08_Decisiones-Y-Trampas.md); dónde está la guía de GitHub Actions y sus desfasajes → [07](07_Guias.md); puertos y stack → [00](00_MASTER-INDEX.md).

---

## 1. Mapa de los seis workflows

| Archivo | `name:` (en Actions) | ID de workflow | Proyecto | Rol |
| --- | --- | --- | --- | --- |
| `ci.yml` | `CI` | 340678050 | Solución sin MAUI | Puerta de integración: compilación + unitarias + API + ViewModels, después E2E |
| `e2e.yml` | `E2E` | 340684644 | `MovilidadUrbana.Web` | Definición **reutilizable** de las E2E de Movilidad Urbana (+ cron nocturno) |
| `e2e-holamundo.yml` | `E2E — Hola Mundo` | 356677889 | `WebBlazor.HolaMundo` | Escalón 1: un job, un navegador |
| `e2e-login.yml` | `E2E — Login` | 356677890 | `WebBlazor.Login` | Escalón 2: publica una vez, matriz de navegadores |
| `android.yml` | `Android — MAUI` | 356840216 | `MovilidadUrbana.MAUI` | Pruebas de ViewModels + APK Release como artefacto |
| `verificacion-entorno.yml` | `Verificación de entorno` | 340684647 | `MovilidadUrbana.Web` desplegada | Prueba de humo contra una URL ya desplegada, reusando `e2e.yml` |

Los seis están `active` en la API (`/actions/workflows`, 2026-10-25). Los seis figuran en la carpeta de solución `github-workflow` de `Lab-E2E.WebBlazor.sln` (líneas 16–25).

```
ci.yml ──(needs: compilacion)──► uses: ./.github/workflows/e2e.yml  ◄── uses ── verificacion-entorno.yml
   │                                    ▲ workflow_call                          (workflow_dispatch, url-base)
   ├─ comentario-en-pr (needs: e2e)     │ también: workflow_dispatch + schedule '15 3 * * *'
   └─ ci-ok (needs: compilacion, e2e)

e2e-holamundo.yml   e2e-login.yml   android.yml      ← independientes, con filtro de rutas, no reutilizables
```

La escalera es deliberada (README §«Los workflows»; cabeceras de `e2e-holamundo.yml` líneas 1–8 y `e2e-login.yml` líneas 1–11):

| Escalón | Workflow | Qué suma respecto del anterior |
| --- | --- | --- |
| 1 | `e2e-holamundo.yml` | Compila, levanta la app con `dotnet run`, prueba con chromium |
| 2 | `e2e-login.yml` | Publica autocontenida **una vez** y reparte el artefacto a una matriz elegible a mano |
| 3 | `e2e.yml` | Reutilizable (`workflow_call`) con inputs/outputs, cron, caché de navegadores, URL desplegada, reporte unificado |

---

## 2. Disparadores, concurrencia y permisos

| Workflow | `push` | `pull_request` | Otros | `concurrency.group` | Cancela en curso |
| --- | --- | --- | --- | --- | --- |
| `ci.yml` | `main`, `paths-ignore: **/*.md, docs/**, .gitignore` | a `main` o `develop`; `types: opened, synchronize, reopened, ready_for_review` | `merge_group` | `ci-${{ github.ref }}` | solo si `pull_request` |
| `e2e.yml` | — | — | `workflow_call`, `workflow_dispatch`, `schedule: '15 3 * * *'` | `e2e-${{ github.workflow }}-${{ github.ref }}` | solo si `pull_request` |
| `e2e-holamundo.yml` | `main`, `paths: src/WebBlazor.HolaMundo/**, tests/WebBlazor.HolaMundo.E2ETests/**, el propio yml` | a `main`, mismas rutas | `workflow_dispatch` | *(no declara)* | — |
| `e2e-login.yml` | `main`, `paths: src/WebBlazor.Login/**, tests/WebBlazor.Login.E2ETests/**, el propio yml` | a `main`, mismas rutas | `workflow_dispatch` con input `navegadores` | `e2e-login-${{ github.ref }}` | solo si `pull_request` |
| `android.yml` | `main`, `paths: src/MovilidadUrbana.MAUI/**, tests/MovilidadUrbana.MAUI.Tests/**, el propio yml` | a `main`, mismas rutas | `workflow_dispatch` | `android-${{ github.ref }}` | solo si `pull_request` |
| `verificacion-entorno.yml` | — | — | `workflow_dispatch` (inputs `entorno` tipo `environment`, `url-base`, ambos requeridos); `workflow_run` solo como comentario (línea 19–20) | *(no declara)* | — |

- **Permisos**: todos declaran `permissions: contents: read`; solo el job `comentario-en-pr` de `ci.yml` suma `pull-requests: write` (`ci.yml` líneas 121–123).
- **`paths-ignore` de `ci.yml`** incluye `docs/**`, carpeta que no existe en el repo (verificado con `ls` sobre `8fb4c3a`). Efecto observado: el commit `8fb4c3a` (solo `README.md` y `CHANGELOG.md`) **no disparó CI**; la última corrida de CI es la de `e9dea2a`.
- **`e2e.yml` cron**: `15 3 * * *` (comentario: «03:15 UTC ≈ 00:15 en Argentina», línea 61). Ver §6.3 sobre el atraso real.

---

## 3. Jobs, por workflow

### 3.1 `ci.yml`

| Job (id → nombre visible) | `needs` | Runner activo | Timeout | Qué hace |
| --- | --- | --- | --- | --- |
| `compilacion` → «Compilación y unitarias» | — | `ubuntu-latest` (propio comentado) | 15 | `if: draft != true`; `setup-dotnet 10.0.x`; `dotnet restore/build Lab-E2E.WebBlazor.SinMaui.slnf -c Release -warnaserror`; `dotnet test` de `MovilidadUrbana.UnitTests` (`unitarias.trx`), `MovilidadUrbana.ApiWeb.Tests` (`api.trx`), `MovilidadUrbana.MAUI.Tests` (`maui-viewmodels.trx`); sube `resultados-unitarias` (7 días); `dotnet test tests/MovilidadUrbana.E2ETests --list-tests` |
| `e2e` → «E2E» | `compilacion` | (los de `e2e.yml`) | — | `uses: ./.github/workflows/e2e.yml`; `navegadores`: `chromium` en PR, `chromium,firefox,webkit,mobile-chrome` en el resto; `referencia`: `pull_request.head.sha \|\| github.sha` |
| `comentario-en-pr` → «Comentar en el PR» | `e2e` | `ubuntu-latest` | — | Solo en PR desde el mismo repo (no forks); `actions/github-script@v9` crea o **actualiza** un comentario marcado `<!-- e2e-playwright -->` con resultado, commit y enlace a la corrida |
| `ci-ok` → «CI aprobada» | `compilacion`, `e2e` | `ubuntu-latest` | — | `if: always()`; falla si algún resultado no es `success` ni `skipped`. Comentario: «Único job que las reglas de protección de rama necesitan exigir» |

`MovilidadUrbana.MAUI` queda fuera porque compilarla pide el workload (comentario líneas 54–55); de eso se ocupa `android.yml`. `MovilidadUrbana.MAUI.UITests` **no corre en CI**: ningún `dotnet test` de `ci.yml` lo invoca (casos «con Appium sobre la app instalada en el teléfono», README línea 64), aunque sí se compila, porque figura en `Lab-E2E.WebBlazor.SinMaui.slnf`. Ningún job corre las E2E de Hola Mundo ni de Login: tienen sus propios workflows.

### 3.2 `e2e.yml` (reutilizable)

Entradas `workflow_call`: `navegadores` (default `chromium`), `url-base` (vacío = publicar y levantar local), `referencia`, `retencion-dias` (default 7). Salida: `resultado` ← `jobs.reporte.outputs.resultado`. En `workflow_dispatch` `navegadores` es un `choice` de 4 combinaciones. Variables globales: `CI=true`, `NAVEGADORES` (default `chromium,firefox,webkit,mobile-chrome`, que es lo que corre el cron), `ARTEFACTO_APLICACION=aplicacion-publicada`, `PROYECTO_PRUEBAS=tests/MovilidadUrbana.E2ETests`.

| Job | `needs` | Runner activo | Timeout | Pasos clave |
| --- | --- | --- | --- | --- |
| `publicar` | — | **`[self-hosted, i7infra-dev]`** (línea 89; `ubuntu-latest` comentado) | 20 | `if: inputs.url-base == ''`; checkout de `referencia`; `setup-dotnet`; **verifica que el SDK (`net$(dotnet --version major).0`) coincida con el `<TargetFramework>` de `MovilidadUrbana.Web.csproj`**; `dotnet publish` autocontenido `linux-x64` → `publicacion/`; sube `aplicacion-publicada` |
| `preparar` → «Preparar matriz» | — | `ubuntu-latest` | 5 | Convierte la lista separada por comas en JSON para la matriz; la escribe en el resumen |
| `pruebas` → «Pruebas (<configuración>)» | `publicar`, `preparar` | `ubuntu-latest` | 30 | `fail-fast: false`; `mobile-chrome` ⇒ `NAVEGADOR=chromium` + `EMULAR_MOVIL=true`; compila las pruebas; `actions/cache@v6` sobre `~/.cache/ms-playwright` con clave `playwright-<os>-<navegador>-<hash del csproj de E2E>`; instala el navegador con el CLI embebido (`bin/Release/net10.0/.playwright/…/cli.js install --with-deps`); baja el artefacto y hace `chmod +x publicacion/MovilidadUrbana.Web` (el zip pierde el bit); `dotnet test --settings pruebas.runsettings -- Playwright.BrowserName=$NAVEGADOR` con `PUBLICAR_ANTES_DE_PROBAR=false`; sube `resultados-<configuración>` (TRX + `trazas/*.zip`) |
| `reporte` → «Reporte unificado» | `preparar`, `pruebas` | `ubuntu-latest` | 15 | Junta `resultados-*`, lee los `<Counters>` de cada TRX con `node -e` y arma una tabla Total/Pasaron/Fallaron en `$GITHUB_STEP_SUMMARY`; `exit 1` si `pruebas` no fue `success` |

- El `if` de `pruebas` (`!cancelled() && preparar == success && publicar != failure`) es lo que permite que `publicar` se saltee contra una URL desplegada sin arrastrar a la matriz (comentario línea 155).
- Nada corre en un contenedor de job (`container:`): el runner propio es él mismo un contenedor sin socket de Docker (cabecera, líneas 15–17). Origen: ver §5.

### 3.3 `e2e-holamundo.yml`

Un job, «Pruebas (chromium)», `ubuntu-latest`, 20 min: `dotnet build` de app y pruebas → instala chromium con el CLI embebido → `dotnet run --no-build --no-launch-profile` con `ASPNETCORE_URLS=http://localhost:5027`, `ASPNETCORE_ENVIRONMENT=Development`, en segundo plano, sondeando `/` hasta 60 s → `dotnet test --settings pruebas.runsettings` (`holamundo.trx`). Sube `resultados-holamundo` + `aplicacion.log` **solo si falla**. La URL está duplicada a propósito con la prueba (cabecera del yml, líneas 7–8): `http://localhost:5027` también figura en `tests/WebBlazor.HolaMundo.E2ETests/HolaMundoE2ETests.cs:12`.

### 3.4 `e2e-login.yml`

| Job | Runner | Timeout | Qué hace |
| --- | --- | --- | --- |
| `publicar` → «Publicar la aplicación» | `ubuntu-latest` | 15 | `dotnet publish` autocontenido `linux-x64`; sube `aplicacion-login` (7 días); arma la matriz desde `inputs.navegadores \|\| 'chromium'` |
| `pruebas` → «Pruebas (<navegador>)» | `ubuntu-latest` | 20 | `fail-fast: false`; compila pruebas, instala el navegador, baja el artefacto, `chmod +x`, arranca `./WebBlazor.Login` **desde su carpeta** con `ASPNETCORE_URLS=http://localhost:5181` (sondea `/login`), corre `dotnet test -- Playwright.BrowserName=<navegador>`; sube resultados + log solo si falla |

Sin reporte unificado ni `workflow_call` (cabecera, líneas 7–8). La URL se copia de `PruebaDeSuperficie.UrlBase` (línea 11) — ese nombre de clase en el comentario es anterior al renombre: ver §8.

### 3.5 `android.yml`

Un job, «Pruebas y APK», `ubuntu-latest`, 45 min: `setup-dotnet 10.0.x` → `dotnet test tests/MovilidadUrbana.MAUI.Tests -c Release` → `setup-java@v6` Temurin 17 → `dotnet workload install maui-android` → `dotnet build … -t:InstallAndroidDependencies -f net10.0-android -p:AndroidSdkDirectory=$ANDROID_HOME -p:AcceptAndroidSDKLicenses=True` → `dotnet publish -c Release -f net10.0-android -p:AndroidPackageFormat=apk -o apk` → sube `apk/*-Signed.apk` como `movilidad-urbana-apk` (14 días, `if-no-files-found: error`). Firmado con la clave de depuración del runner: sirve para un teléfono de prueba, no para una tienda (cabecera, líneas 5–6).

### 3.6 `verificacion-entorno.yml`

Un job `humo` → «Prueba de humo»: `uses: ./.github/workflows/e2e.yml` con `navegadores: chromium`, `url-base: ${{ inputs.url-base }}`, `retencion-dias: 30`. Con `url-base` cargada, `e2e.yml` no publica y prueba la URL. El input `entorno` (tipo `environment`) se declara pero **no se pasa** a `e2e.yml` (líneas 10–14 contra 26–32).

---

## 4. Artefactos

| Artefacto | Lo sube | Retención | Contenido |
| --- | --- | --- | --- |
| `resultados-unitarias` | `ci.yml` / `compilacion` | 7 | TRX de unitarias, API y ViewModels |
| `aplicacion-publicada` | `e2e.yml` / `publicar` | `retencion-dias` (7; 30 desde `verificacion-entorno`) | Publicación autocontenida de `MovilidadUrbana.Web` |
| `resultados-<configuración>` | `e2e.yml` / `pruebas` | ídem | TRX + `trazas/*.zip` de casos fallidos |
| `aplicacion-login` | `e2e-login.yml` / `publicar` | 7 | Publicación autocontenida de `WebBlazor.Login` |
| `resultados-login-<navegador>`, `resultados-holamundo` | escalones 1 y 2 | default de GitHub | Solo si falla: TRX + `aplicacion.log` |
| `movilidad-urbana-apk` | `android.yml` | 14 | APK Release firmado con clave de depuración |

Observado 2026-10-25 (`/actions/artifacts`): 35 artefactos listados, todos de `e2e.yml` y no vencidos — 7 por nombre: `aplicacion-publicada`, `resultados-chromium`, `resultados-firefox`, `resultados-webkit`, `resultados-mobile-chrome` (consistente con 7 cron diarios × retención 7). No queda ningún `movilidad-urbana-apk` (la última corrida de `android.yml` es del 2026-09-18; retención 14 días).

---

## 5. Runner: historia y estado al commit `8fb4c3a`

| Fecha | Commit | Cambio | Evidencia |
| --- | --- | --- | --- |
| 2026-08-23 | `0516139` | Todo en `[self-hosted, i7infra-dev]`, con jobs dentro de `container:` | CI run #1 (32654172882): jobs «Compilación» y «Verificación rápida» fallan en *Initialize containers*, runner `i7infra-runner-dev` |
| 2026-08-23 | `6cb167d` | «Correr los jobs sobre el runner en vez de dentro de contenedores» | CI run #2 en verde |
| 2026-08-23 | `90ad8fe` | La suite E2E de JavaScript pasa a proyecto C# | CI run #3 (23d0ef3) todavía muestra 16 jobs «Pruebas (<nav> · shard N)», 4×4, todos en el runner propio; después de este commit desaparecen los shards |
| 2026-08-24 | `db775c5` (PR #10) | Todos los jobs a `ubuntu-latest`, el propio queda comentado como ejemplo | CI run #21 (35841f3): los 9 jobs que corrieron, con runner «GitHub Actions …» y etiqueta `ubuntu-latest` (el décimo, «Comentar en el PR», `skipped`) |
| 2026-09-03 | `4815823` | **`publicar` de `e2e.yml` vuelve al runner propio** (línea 89 descomentada) | CI run #39 (e9dea2a, 2026-09-18) y E2E #66 (cron 2026-10-25): «Publicar la aplicación» en `i7infra-runner-dev`, el resto en `ubuntu-latest` |
| 2026-09-12 | `7262395` | Se corrige el README §«Runner» para declarar esa excepción | `CHANGELOG.md` 2026-09-12 «Corregido» |

Estado vigente: **solo `e2e.yml` / `publicar` usa el runner propio**; los otros 5 workflows y los demás jobs de `e2e.yml` corren en `ubuntu-latest`. Como `ci.yml` llama a `e2e.yml` sin `url-base`, toda corrida de CI que llega al job `e2e` pasa por `i7infra-dev`; `verificacion-entorno.yml` siempre carga `url-base` (input requerido), así que `publicar` se saltea y no lo usaría. El repo es público (API `/repos`, `visibility: public`); el guardarraíl contra forks es la aprobación de workflows de GitHub (`CHANGELOG.md` 2026-09-03; guía `Notas.GitHub.md`, ver [07](07_Guias.md)). Si esa opción está activada en Settings **no es verificable** sin credenciales.

---

## 6. Corridas observadas (API pública, al 2026-10-25)

Fuente: `GET /repos/hdcm-dev/Lab-E2E.WebBlazor/actions/runs?per_page=100` páginas 1–2 (`total_count` 117), más `/runs/{id}/jobs` y `/check-runs/{id}/annotations` para las corridas citadas. Todas las corridas: `run_attempt` 1, actor `fernandofilipuzzi-utn`, rama `main` salvo los PR.

### 6.1 Totales

| Workflow | Corridas | Evento → conclusión | Primera | Última |
| --- | ---: | --- | --- | --- |
| `E2E` | 66 | 63 `schedule` → success · 3 `workflow_dispatch` → success | 2026-08-24 04:02Z | 2026-10-25 08:20Z |
| `CI` | 39 | push: 24 success, 1 failure, 2 cancelled · pull_request: 11 success, 1 failure | 2026-08-23 17:14Z | 2026-09-18 12:27Z |
| `Android — MAUI` | 4 | 4 push → success | 2026-09-13 01:21Z | 2026-09-18 12:27Z |
| `E2E — Hola Mundo` | 4 | 4 push → success | 2026-09-12 18:27Z | 2026-09-18 12:27Z |
| `E2E — Login` | 4 | 4 push → success | 2026-09-12 18:27Z | 2026-09-18 12:27Z |
| `Verificación de entorno` | **0** | nunca se disparó | — | — |
| **Total** | **117** | 113 success · 2 failure · 2 cancelled | | |

Ninguna corrida de `workflow_dispatch` de Hola Mundo, Login ni Android: las cuatro de cada uno son `push`, sobre los commits `f9f3ca2`, `e0f3e9d`, `946d023`, `e9dea2a` (escalones) y `10ce735`, `3e119b8`, `946d023`, `e9dea2a` (Android). No hay `merge_group` observado. Las 12 corridas de `pull_request` son de 2026-08-23 a 2026-09-04 (la última, rama `feature/template-sdd-en-la-interfaz`, que entró como PR #11 en `7a9edaa`); desde entonces todo entra por `push` a `main`.

### 6.2 Las cuatro corridas que no fueron verdes

| Corrida | Fecha | Commit | Qué pasó | Evidencia |
| --- | --- | --- | --- | --- |
| CI #1 (pull_request) | 2026-08-23 | `0516139` | *Initialize containers* falla en el runner propio (sin socket de Docker) | jobs de 32654172882 |
| CI #17 (push) | 2026-08-24 | `825afdf` | `cancelled`, sin ningún job registrado (`total_count: 0`) | jobs de 32768434103 |
| CI #19 (push) | 2026-08-24 → 2026-08-25 | `5afcb36` | En el runner propio: firefox y mobile-chrome pasan; chromium y webkit quedan `cancelled` sin runner asignado, con `completed_at` exactamente 24 h después de `started_at`; reporte y `ci-ok` en `failure` | jobs de 32769264675. Interpretación (cola de 24 h de un runner autoalojado sin tomar el job): **no verificada** |
| CI #38 (push) | 2026-09-18 | `946d023` | «Compilar con los avisos tratados como error» falla: `CS1574` *XML comment has cref attribute … that could not be resolved* en `src/MovilidadUrbana.ApiWeb/Application/Result.cs:5`, `Localidades/LocalidadPolicy.cs:8`, `Encuestas/EncuestaPolicy.cs:7` (crefs `Errores`, `ReglasDeLocalidad`, `ReglasDeEncuesta`, nombres previos al renombre). Corregido en `e9dea2a` (CI #39 verde, 5 min después) | annotations del job; `CHANGELOG.md` 2026-09-18 |

### 6.3 Regresión nocturna (`schedule` de `e2e.yml`)

- 63 corridas, **una por día sin huecos** del 2026-08-24 al 2026-10-25, las 63 en verde, siempre sobre `main`. Desde el 2026-09-19 todas prueban `8fb4c3a`.
- **Atraso respecto del cron** (03:15 UTC): mínimo 42 min, mediana 317 min (~08:30 UTC), máximo 722 min (arranque 2026-08-28 15:17Z). Ninguna arrancó a la hora.
- Duración (`run_started_at` → `updated_at`): mínimo 1,95 min, mediana 2,6, máximo 14,3.
- Forma de la última (40176198598, 2026-10-25): 7 jobs — «Preparar matriz», «Publicar la aplicación» (`i7infra-runner-dev`), 4 × «Pruebas (…)» y «Reporte unificado» (`ubuntu-latest`).
- Los 3 `workflow_dispatch` de `E2E` son del 2026-08-24/25 (commits `390a77c`, `35841f3`).

### 6.4 Duraciones de las corridas verdes

| Workflow | Mediana | Rango |
| --- | --- | --- |
| `CI` | 4,6 min | 2,5 min – 1659,8 min (la #21, creada 2026-08-24 20:05Z, cuyos jobs recién arrancaron 2026-08-25 23:41Z, cuando terminó la #19; que esperó por el `concurrency` de `main`, que no cancela, es inferencia **no verificada**) |
| `Android — MAUI` | 3,1 min | 3,1 |
| `E2E — Hola Mundo` | 1,0 min | 0,9 – 1,0 |
| `E2E — Login` | 1,6 min | 1,6 |

### 6.5 Aviso pendiente de la imagen del runner

El check-run de CI #38 (2026-09-18) trae la anotación *notice*: «The ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026». Las corridas del cron posteriores al 2026-10-19 siguen en verde; **qué imagen usaron no se verificó** (los logs piden autenticación).

---

## 7. Protección de rama

`ci.yml` se presenta como «el workflow que se ata a las reglas de protección de rama» (línea 1) y `ci-ok` como el único check a exigir (línea 160). Observado (API `/branches`, 2026-10-25): **`main` tiene `protected: false`**, y `main` es la única rama remota (`git branch -a`: no existe `develop`, aunque `ci.yml` la acepta como destino de PR). El diseño está listo; la regla no está configurada.

---

## 8. Desfasajes y rastros en los workflows y su documentación

| Dónde | Dice | Lo verificado |
| --- | --- | --- |
| `e2e.yml` líneas 11–13 (cabecera) | Los jobs corren en `ubuntu-latest`, con el runner propio comentado | `publicar` tiene activo `[self-hosted, i7infra-dev]` (línea 89) |
| `e2e.yml` líneas 87–88 | «Se deja comentado como ejemplo» | Encima de la línea **descomentada**; el comentario quedó del estado de `db775c5` |
| `e2e.yml` línea 205 | «El runner conserva la caché entre corridas» | Contradice el comentario de líneas 193–196 (los de GitHub arrancan limpios); `pruebas` corre en `ubuntu-latest` |
| `e2e-login.yml` línea 11 | «`PruebaDeSuperficie.UrlBase`» | Rastro en prosa del renombre `946d023` (hoy `SurfaceTestBase.UrlBase`); inventario en [01](01_Arquitectura.md) §8.3 |
| `ci.yml` línea 1 y README §`ci.yml` | Se ata a la protección de rama | `main` sin protección (§7) |
| `ci.yml` `paths-ignore: docs/**` | — | No hay carpeta `docs/`; inocuo |
| `verificacion-entorno.yml` | Input `entorno` requerido | No se usa; 0 corridas |
| README §Evidencia (última línea) y `CHANGELOG.md` 2026-08-30 | «el comportamiento real de los workflows, del que solo se validó la sintaxis YAML» | 117 corridas reales observadas (§6); la afirmación es de antes y nadie la actualizó |
| `CHANGELOG.md` 2026-09-12 | Se retiró `e2e_2.yml` (workflow de Base, «0 corridas exitosas de 4») | Ese archivo nunca estuvo en la historia de este repo (`git log --all -- .github/workflows/e2e_2.yml` vacío) y la API no lista sus corridas: **no verificable desde acá** |
| `CHANGELOG.md` 2026-09-12 | `publicar` en el runner propio «acumula 23 corridas en verde» | No recontado a esa fecha; **no verificado** |

---

## 9. Cómo reproducir lo que corre CI, en local

| Lo de CI | Equivalente local | Fuente |
| --- | --- | --- |
| `dotnet build …SinMaui.slnf -warnaserror` | `scripts/dotnet.sh dotnet build Lab-E2E.WebBlazor.SinMaui.slnf --configuration Release -warnaserror` (agregar `--no-incremental`: el `CS1574` de `946d023` no apareció en un build incremental) | README §Evidencia 2026-09-12; `CHANGELOG.md` 2026-09-18 |
| `publicar` de `e2e.yml` | `scripts/publicar.sh` (mismo `dotnet publish` autocontenido `linux-x64` a `publicacion/`) | `scripts/publicar.sh` líneas 11–16 |
| `pruebas` (una configuración) | `scripts/pruebas.sh <navegador>`, `EMULAR_MOVIL=true scripts/pruebas.sh` | README §«Sin nada instalado» |
| `--list-tests` | `dotnet test tests/MovilidadUrbana.E2ETests --list-tests` | `ci.yml` líneas 93–98 |

Configuración común de las corridas: `pruebas.runsettings` — `BrowserName` chromium, `ExpectTimeout` 5000, `Headless` true, `NumberOfTestWorkers` 4, `ResultsDirectory` `resultados`. Detalle de suites y variables (`PUBLICAR_ANTES_DE_PROBAR`, `INSTALAR_NAVEGADORES`, `EMULAR_MOVIL`, `TRAZAR`, `URL_BASE`) → [05](05_Pruebas.md).

---

## 10. Versiones de acciones usadas

| Acción | Versión | Dónde |
| --- | --- | --- |
| `actions/checkout` | v7 | los cinco con pasos propios (`verificacion-entorno` solo llama a `e2e.yml`) |
| `actions/setup-dotnet` | v6 (`dotnet-version: 10.0.x`) | todos los que compilan |
| `actions/upload-artifact` | v7 | `ci`, `e2e`, `e2e-holamundo`, `e2e-login`, `android` |
| `actions/download-artifact` | v8 | `e2e`, `e2e-login` |
| `actions/cache` | v6 | `e2e` |
| `actions/github-script` | v9 | `ci` |
| `actions/setup-java` | v6 (Temurin 17) | `android` |
