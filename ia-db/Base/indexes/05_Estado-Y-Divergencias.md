# 05 — Estado y divergencias verificadas

> **Propósito**: dejar registrado, con su evidencia, qué está incompleto o inconsistente en el
> repositorio, para que ningún agente lo dé por terminado ni «arregle» algo sin ver el conjunto.
> **Fuente primaria**: inspección directa de los archivos citados, 2026-09-01.
>
> Este índice separa **hechos** —lo que dicen los archivos— de **interpretaciones** —lo que de ahí
> se deduce—. Nada de lo que sigue se verificó ejecutando el código: **las pruebas no se corrieron
> durante el indexado.**

## Resumen

| # | Hecho verificado | Archivo |
| --- | --- | --- |
| 1 | La prueba navega a `https://localhost:7071`, puerto que no figura en ningún `launchSettings.json` | `HolaMundoE2ETests.cs:11` |
| 2 | `LoginE2ETests.TestLogin` tiene el cuerpo vacío | `LoginE2ETests.cs` |
| 3 | `LoginE2ETests` es `internal` | `LoginE2ETests.cs` |
| 4 | El workflow referencia rutas de `MovilidadUrbana`, que no existen acá | `e2e.yml:149`, `e2e.yml:171` |
| 5 | El workflow pasa `--settings pruebas.runsettings`, archivo que no existe en el repositorio | `e2e.yml:183` |
| 6 | El bloque `env` usa `inputs.retencion-dias`, entrada no declarada | `e2e.yml:29` |
| 7 | Dos jobs usan `inputs.referencia`, entrada no declarada | `e2e.yml:49`, `e2e.yml:119` |
| 8 | El workflow no declara `workflow_call`, `schedule`, `concurrency` ni `permissions` | `e2e.yml` |
| 9 | `Guides/GitHub-Action.md` está vacío (0 líneas) y sin embargo figura en la solución | `Guides/GitHub-Action.md`, `.slnx` |
| 10 | `README.md` contiene solo el título del repositorio | `README.md` |
| 11 | No hay proyecto de pruebas E2E para `Login` con contenido, ni ninguna prueba del login | `tests/` |

## Detalle

### 1. La URL de la prueba no coincide con ningún perfil de arranque

**Hecho.** `HolaMundoE2ETests.Setup` navega a `https://localhost:7071/HolaMundo`. Los perfiles
`https` de `launchSettings.json` son `7230` para `HolaMundo` y `7212` para `Login`; los `http`, 5027
y 5181.

**Interpretación.** Con la aplicación levantada por cualquiera de sus perfiles, la prueba no llegaría
al servidor. El puerto parece heredado de otra corrida o de otro proyecto.

### 2 y 3. La prueba del login no prueba nada

**Hecho.** `TestLogin` contiene dos comentarios en inglés («Implement your login test logic here…»)
y ninguna instrucción. El `[SetUp]` agrega una cookie llamada `MiCookie`, que no corresponde a
ninguna cookie del servidor —la de autenticación se llama `auth_token`—. La clase está declarada
`internal`.

**Interpretación.** Es un esqueleto reservado. Todo el flujo descrito en
[02_Autenticacion.md](02_Autenticacion.md) —el login SSR estático, `DestinoSeguro()`, `[Authorize]`,
`<NotAuthorized>`— está **sin cobertura automatizada**. La visibilidad `internal` no impide que
NUnit descubra el caso, pero es una inconsistencia con la otra clase de prueba, que es `public`.

### 4 a 8. El workflow está copiado del laboratorio grande sin adaptar del todo

**Hecho.** Además de lo ya adaptado (`PROYECTO_PRUEBAS` y `PATH_PROJECT_FILE`, que sí apuntan a
`HolaMundo`), quedaron sin cambiar:

| Línea | Contenido | Problema |
| --- | --- | --- |
| 149 | `hashFiles('tests/MovilidadUrbana.E2ETests/MovilidadUrbana.E2ETests.csproj')` | Ruta inexistente: `hashFiles` sobre nada devuelve siempre la misma clave, así que la caché no se invalidaría al cambiar la versión de Playwright |
| 171 | `chmod +x publicacion/MovilidadUrbana.Web` | El binario publicado se llama `WebBlazor.E2E.Base.HolaMundo` |
| 183 | `--settings pruebas.runsettings` | El archivo no existe en este repositorio |
| 29 | `${{ inputs.retencion-dias \|\| 7 }}` | La entrada no está declarada; el `||` la resuelve en 7 |
| 49, 119 | `${{ inputs.referencia \|\| github.ref }}` | Ídem; cae en `github.ref` |
| 24 | Comentario «`inputs` está vacío en `schedule`» | No hay bloque `schedule` |

**Interpretación.** Los tres primeros harían fallar la corrida o la volverían inútil; los tres
últimos son inocuos gracias al operador `||`, pero delatan el origen del archivo. `Guides/E2E-Guides.md`
transcribe una versión del workflow **con** `schedule` y `concurrency`, así que la guía y el YAML
tampoco coinciden entre sí.

### 9 y 10. Documentación incompleta

**Hecho.** `Guides/GitHub-Action.md` tiene 0 líneas y está declarado en `Ejemplos.WebBlazor.E2E.Base.slnx`.
`README.md` contiene una única línea: `# Lab-E2E.WebBlazor.Base`.

**Interpretación.** La guía de GitHub Actions está reservada pero no escrita. Un agente que llegue
al repositorio por su `README.md` no encuentra ninguna orientación: la puerta de entrada real es
`Guides/E2E-Guides.md`.

### 11. Cobertura

**Hecho.** El repositorio declara 2 casos de prueba; solo 1 tiene cuerpo.

## Lo que sí está completo y funciona como ejemplo

Para no dejar una impresión sesgada:

- La página `HolaMundo.razor` y su prueba son un ejemplo **cerrado y coherente**: los tres
  `data-testid`, los tres llamados de Playwright y la distinción entre `ToHaveValueAsync` y
  `ToHaveTextAsync`.
- El login por cookies está **bien resuelto y bien comentado**: el porqué del SSR estático, el
  `??=` para evitar `BL0008`, el `HttpContext` por cascada y `DestinoSeguro()` contra el *open
  redirect*.
- `Guides/E2E-Guides.md` cubre la creación del proyecto, el ejemplo completo y el anexo sobre la
  instalación de navegadores.

## Cómo verificar todo esto

| Afirmación | Comprobación |
| --- | --- |
| Puertos | `grep applicationUrl src/*/Properties/launchSettings.json` frente a la URL de `HolaMundoE2ETests.cs` |
| Rutas del workflow | `grep -n MovilidadUrbana .github/workflows/e2e.yml` |
| `pruebas.runsettings` | `ls pruebas.runsettings` |
| Entradas no declaradas | `grep -n 'inputs\.' .github/workflows/e2e.yml` frente al bloque `workflow_dispatch` |
| Guía vacía | `wc -l Guides/GitHub-Action.md` |
