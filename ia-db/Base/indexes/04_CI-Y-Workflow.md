# 04 — CI y workflow

> **Propósito**: describir el único workflow del repositorio y señalar qué partes están adaptadas y
> cuáles siguen siendo del laboratorio grande.
> **Fuente primaria**: `.github/workflows/e2e.yml`.

Hay **un solo** workflow: `e2e.yml`, de 258 líneas, copiado de
[`Lab-E2E.WebBlazor`](../../Root/indexes/06_CI-Y-Workflows.md) y adaptado a medias. Las divergencias
concretas están en [05_Estado-Y-Divergencias.md](05_Estado-Y-Divergencias.md); acá se describe qué
hace.

## Disparadores

| Disparador | Estado |
| --- | --- |
| `workflow_dispatch` | Declarado, con entradas `navegadores` (choice) y `url-base` (string) |
| `workflow_call` | **No declarado** (sí lo está en el original) |
| `schedule` | **No declarado** en el YAML, aunque el bloque `env` y la guía lo mencionan |

Tampoco hay bloques `concurrency` ni `permissions`, que el original sí declara: sin
`permissions` explícitos rige el valor por defecto del repositorio o de la organización.

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

`PROYECTO_PRUEBAS` y `PATH_PROJECT_FILE` **sí** están adaptados a este repositorio: solo se prueba
`HolaMundo`, nunca `Login`.

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

## Lo que no hay

No existen `ci.yml` ni `verificacion-entorno.yml`: no hay verificación atada a `pull_request` ni a
`push`, ni un check resumen para la protección de rama, ni comentario automático en los pull
requests. Todo eso vive únicamente en `Lab-E2E.WebBlazor`.

`Guides/E2E-Guides.md` transcribe este workflow en su sección «workflow de GitHub Actions», con un
bloque `schedule` que el YAML del repositorio no tiene.
