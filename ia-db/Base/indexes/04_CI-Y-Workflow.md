# 04 — CI y workflow

> **Propósito**: describir el único workflow del repositorio y señalar qué partes están adaptadas y
> cuáles siguen siendo del laboratorio grande.
> **Fuente primaria**: `.github/workflows/e2e.yml` (261 líneas) y `Guides/Notas.GitHub.md`.
> **Vigencia**: 2026-09-02, commit `6af2049`. Ninguna corrida se observó desde esta máquina.

Hay **un solo** workflow: `e2e.yml`, copiado de
[`Lab-E2E.WebBlazor`](../../Root/indexes/06_CI-Y-Workflows.md). Dos de las tres divergencias
bloqueantes que registraba el indexado inicial se corrigieron el 2026-09-01/02; queda una. El detalle
está en [05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md); acá se describe qué hace.

## Disparadores

| Disparador | Estado |
| --- | --- |
| `pull_request` | **Agregado** el 2026-09-01 (`65435e5`), sobre `branches: [main]` |
| `workflow_dispatch` | Declarado, con entradas `navegadores` (choice) y `url-base` (string) |
| `workflow_call` | **No declarado** (sí lo está en el original) |
| `schedule` | **No declarado** en el YAML, aunque el bloque `env` y la guía lo mencionan |

Tampoco hay bloques `concurrency` ni `permissions`, que el original sí declara: sin `permissions`
explícitos rige el valor por defecto del repositorio o de la organización.

Con `pull_request` no hay `inputs`, así que las cuatro expresiones `inputs.*` caen en su valor por
defecto y los `if: inputs.url-base == ''` se cumplen: la corrida publica la aplicación y prueba
contra ella. **No verificado por ejecución.**

## Variables del bloque env

| Variable | Valor |
| --- | --- |
| `CI` | `'true'` |
| `NAVEGADORES` | `inputs.navegadores` o las cuatro configuraciones |
| `URL_BASE` | `inputs.url-base` o vacío |
| `RETENCION_DIAS` | `inputs.retencion-dias` o 7 |
| `ARTEFACTO_APLICACION` | `aplicacion-publicada` |
| `PROYECTO_PRUEBAS` | `tests/WebBlazor.E2E.Base.HolaMundo.E2ETests` |
| `PATH_PROJECT_FILE` | `src/WebBlazor.E2E.Base.HolaMundo/WebBlazor.E2E.Base.HolaMundo.csproj` |

`PROYECTO_PRUEBAS` y `PATH_PROJECT_FILE` están adaptados a este repositorio: solo se prueba
`HolaMundo`, nunca `Login` —lo cual, dado que el proyecto de pruebas del login no compila, es lo
único que puede correr—.

Desde `ca68245` las dos variables además **se usan** donde antes había rutas literales de
`MovilidadUrbana`:

| Paso | Antes | Ahora |
| --- | --- | --- |
| Caché del navegador | `hashFiles('tests/MovilidadUrbana.E2ETests/…csproj')` | `hashFiles(format('{0}/*.csproj', env.PROYECTO_PRUEBAS))` |
| Permiso de ejecución | `chmod +x publicacion/MovilidadUrbana.Web` | `chmod +x "publicacion/$(basename "${PATH_PROJECT_FILE%.csproj}")"` |

## Los cuatro jobs

Todos con `runs-on: [self-hosted, i7infra-dev]` **activo** y `ubuntu-latest` comentado —al revés que
en el laboratorio grande, donde el runner alojado por GitHub es el que está activo—.

| Job | Qué hace |
| --- | --- |
| `publicar` | Checkout, `setup-dotnet` 10.0.x, comprueba que el `<TargetFramework>` coincida con el SDK del runner, `dotnet publish` autocontenido para `linux-x64` y sube el artefacto `aplicacion-publicada`. Se saltea con `if: inputs.url-base == ''` |
| `preparar` | Convierte `chromium,firefox,…` en el JSON de la matriz y lo deja en el resumen |
| `pruebas` | Un job por configuración: traduce `mobile-chrome` a chromium + `EMULAR_MOVIL`, compila las pruebas, cachea e instala el navegador con el CLI del paquete, baja el artefacto, `chmod +x`, corre `dotnet test` y sube el TRX y las trazas |
| `reporte` | Junta los TRX en una tabla del `$GITHUB_STEP_SUMMARY` con un script de Node y falla si `needs.pruebas.result != 'success'` |

`fail-fast: false` en la matriz y `timeout-minutes` en todos los jobs (20 / 5 / 30 / 15).

## Ideas que el workflow ilustra

Aunque no esté terminado, el archivo sirve como material de estudio de varias prácticas —las mismas
del laboratorio grande, donde están explicadas en detalle:

- **Compilar una vez, probar muchas**: la aplicación se publica en un job y toda la matriz la
  reutiliza como artefacto.
- `mobile-chrome` **no es un navegador**: es chromium con el descriptor de un Pixel 7, traducido en
  un paso `case` que exporta a `$GITHUB_ENV`.
- Los artefactos de Actions **pierden el bit de ejecución** al empaquetarse en zip: de ahí el
  `chmod +x`.
- El navegador lo instala el CLI que viene **dentro del paquete** `Microsoft.Playwright`, así la
  biblioteca y el navegador no se pueden desincronizar.
- El binding de .NET no tiene `merge-reports`: el reporte de cada configuración es un TRX y hay que
  juntar los contadores a mano.
- El SDK se pide explícitamente con `actions/setup-dotnet` porque la imagen del runner no garantiza
  la versión que necesita el proyecto.
- **Derivar del entorno en lugar de repetir la ruta**: `hashFiles(format(...))` y el `basename` del
  `PATH_PROJECT_FILE` son la corrección de `ca68245`, y valen como ejemplo de por qué el nombre del
  proyecto no se escribe dos veces.

## El runner propio y los forks

`Guides/Notas.GitHub.md` (sin versionar, 14 líneas) registra el riesgo que abre el disparador nuevo:
el repositorio es **público** y los jobs corren en `i7infra-dev`, así que un pull request desde un
fork ejecutaría código sin revisar en la máquina propia. La nota apunta a la configuración de la
organización —*Settings → Actions → General → Fork pull request workflows*— con «Require approval for
all outside collaborators» y, para repositorios privados o internos, el detalle de qué tildar. Es una
nota de configuración, no un cambio en el repositorio: **no hay nada en el YAML que lo implemente**.

## Lo que no hay

No existen `ci.yml` ni `verificacion-entorno.yml`: no hay verificación de compilación y pruebas
unitarias, ni un check resumen para la protección de rama, ni comentario automático en los pull
requests. Todo eso vive únicamente en `Lab-E2E.WebBlazor`.

`Guides/E2E-Guides.md` transcribe este workflow en su sección «workflow de GitHub Actions», con un
bloque `schedule` que el YAML del repositorio no tiene, y sin el `pull_request` que sí tiene.
`Guides/GitHub-Action.md`, que sería el lugar natural para explicarlo, sigue vacío.
