# 05 — Estado y divergencias verificadas

> **Propósito**: dejar registrado, con su evidencia, qué está incompleto o inconsistente en el
> repositorio, para que ningún agente lo dé por terminado ni «arregle» algo sin ver el conjunto.
> **Fuente primaria**: inspección directa de los archivos citados, 2026-09-02, commit `6af2049`.
>
> Este índice separa **hechos** —lo que dicen los archivos— de **interpretaciones** —lo que de ahí se
> deduce—. Nada de lo que sigue se verificó ejecutando el código: **ni las pruebas ni el workflow se
> corrieron durante el indexado** (esta máquina no tiene SDK de .NET instalado). Lo único que sí se
> ejecutó alguna vez es el guion de `evidencia/`, y su log es del 2026-09-01.

## Resumen

| # | Hecho verificado | Archivo | Estado |
| --- | --- | --- | --- |
| 1 | Las pruebas navegan a `https://localhost:7071`, puerto que no figura en ningún `launchSettings.json` | `HolaMundoE2ETests.cs:10`, `HolaMundoE2ETest.cs:34` | **Abierto** |
| 2 | El archivo de pruebas del login declara **dos métodos `Setup`** en la misma clase | `HolaMundoE2ETest.cs` | **Abierto — nuevo** |
| 3 | Ese mismo archivo espera un testigo `estado-app` que no existe en el marcado | `HolaMundoE2ETest.cs` | **Abierto — nuevo** |
| 4 | Y navega a `/HolaMundo` relativo sin `BaseURL` configurada | `HolaMundoE2ETest.cs` | **Abierto — nuevo** |
| 5 | La clase de pruebas del login es `internal` | `HolaMundoE2ETest.cs` | Abierto |
| 6 | El workflow pasa `--settings pruebas.runsettings`, archivo que no existe | `e2e.yml:186` | **Abierto** |
| 7 | El bloque `env` usa `inputs.retencion-dias`, entrada no declarada | `e2e.yml:32` | Abierto, inocuo |
| 8 | Dos jobs usan `inputs.referencia`, entrada no declarada | `e2e.yml:52`, `e2e.yml:122` | Abierto, inocuo |
| 9 | El workflow no declara `workflow_call`, `schedule`, `concurrency` ni `permissions` | `e2e.yml` | Abierto |
| 10 | El repositorio es público, corre en un runner propio y nada en el YAML restringe los forks | `e2e.yml:45`, `Guides/Notas.GitHub.md` | **Abierto — nuevo** |
| 11 | `Guides/GitHub-Action.md` está vacío (0 líneas), figura en la solución y el `README.md` lo enlaza | `Guides/GitHub-Action.md` | Abierto |
| 12 | `Guides/E2E-Guides.md` transcribe la superficie y el workflow anteriores al 2026-09-01 | `Guides/E2E-Guides.md:90,101,176-199` | **Abierto — nuevo** |
| 13 | `Guides/Notas.GitHub.md` está sin versionar | `git status` | Abierto, menor |
| 14 | El workflow referenciaba rutas de `MovilidadUrbana` | `e2e.yml:149,171` | **Resuelto** en `ca68245` |
| 15 | `README.md` contenía solo el título del repositorio | `README.md` | **Resuelto** en `0b5c4c7` |
| 16 | El caso del login tenía el cuerpo vacío | `LoginE2ETests.cs` | **Resuelto de forma parcial**: hoy tiene cuerpo, pero el archivo no compila (ver 2) |

## Detalle

### 1. La URL de las pruebas no coincide con ningún perfil de arranque

**Hecho.** `HolaMundoE2ETests.Setup` navega a `https://localhost:7071/HolaMundo`, y el segundo
`Setup` del proyecto del login empieza por la misma URL. Los perfiles `https` de
`launchSettings.json` son `7230` para `HolaMundo` y `7212` para `Login`; los `http`, 5027 y 5181. El
tercer puerto que aparece en el repositorio es el `8080` de los contenedores de `evidencia/`.

**Interpretación.** Con la aplicación levantada por cualquiera de sus perfiles, la prueba no llegaría
al servidor. El puerto parece heredado de otra corrida o de otro proyecto. Es la divergencia más
vieja del repositorio: sobrevivió a la aplicación del template.

### 2, 3, 4 y 5. El proyecto de pruebas del login no compila

**Hecho.** El commit `6af2049` («.») renombró `LoginE2ETests.cs` a `HolaMundoE2ETest.cs` y le puso
cuerpo. El archivo resultante declara, en la misma clase `internal HolaMundoE2ETest : PageTest`:

| Miembro | Cuerpo |
| --- | --- |
| `[SetUp] async public Task Setup()` | `Context.AddCookiesAsync` con la cookie `MiCookie` sobre `UrlBase = "https://localhost:7212"` |
| `[SetUp] public async Task Setup()` | `GotoAsync("https://localhost:7071/HolaMundo")`, después `GotoAsync("/HolaMundo")`, después `Expect(GetByTestId("estado-app")).ToHaveAttributeAsync("data-interactivo", "true")` |
| `[Test] MostrarMensaje` | Copia del caso del otro proyecto |

**Interpretación.** Dos miembros con el mismo nombre y la misma firma no compilan (CS0111): el
proyecto entero queda fuera de la corrida, y con él el `[Test]` que trae. Aunque se resolviera el
duplicado, quedan tres problemas en ese segundo `Setup`:

| Problema | Por qué importa |
| --- | --- |
| El segundo `GotoAsync("/HolaMundo")` es relativo | `PageTest` no tiene `BaseURL` configurada —no hay `.runsettings` ni `BrowserNewContextOptions` sobreescrito—, así que la URL relativa no resuelve |
| Espera `estado-app` con `data-interactivo="true"` | Ese testigo es de `Lab-E2E.WebBlazor`; **en este repositorio ningún `.razor` lo declara** (`grep -rn 'estado-app' src/` no devuelve nada). La espera nunca se cumpliría |
| La cookie `MiCookie` no corresponde a nada del servidor | La de autenticación se llama `auth_token`; y para el flujo real haría falta ingresar, no inyectar una cookie cualquiera |

**Consecuencia.** Todo el flujo de identidad descrito en [02_Autenticacion.md](02_Autenticacion.md)
sigue **sin cobertura en la batería**. La guía del template ya lo declara como pendiente. Lo cubre
solamente el guion de `evidencia/`, que no corre en CI.

La visibilidad `internal` no impide que NUnit descubra el caso, pero es una inconsistencia con la
otra clase de prueba, que es `public`.

### 6 a 9. Lo que queda del workflow copiado

**Hecho.** `ca68245` y `65435e5` corrigieron las dos rutas literales de `MovilidadUrbana` y sumaron
el disparador `pull_request`. Quedaron sin cambiar:

| Línea | Contenido | Problema |
| --- | --- | --- |
| 186 | `--settings pruebas.runsettings` | El archivo **no existe** en este repositorio: `dotnet test` falla al no encontrarlo |
| 32 | `${{ inputs.retencion-dias \|\| 7 }}` | La entrada no está declarada; el `\|\|` la resuelve en 7 |
| 52, 122 | `${{ inputs.referencia \|\| github.ref }}` | Ídem; cae en `github.ref` |
| 28 | Comentario «`inputs` está vacío en `schedule`» | No hay bloque `schedule` |
| — | Sin `workflow_call`, `concurrency` ni `permissions` | El original los declara |

**Interpretación.** El `--settings` es hoy la **única divergencia bloqueante** del workflow: con el
disparador `pull_request` recién agregado, cada PR hacia `main` la va a encontrar. Se arregla de dos
maneras —agregar el `pruebas.runsettings` o sacar el argumento—, y la primera además cerraría lo que
[03_Pruebas.md](03_Pruebas.md) marca como faltante (navegador, timeouts y, de paso, la `BaseURL` que
la divergencia 4 necesita).

### 10. Runner propio, repositorio público y forks

**Hecho.** Los cuatro jobs corren en `runs-on: [self-hosted, i7infra-dev]`, el disparador
`pull_request` está activo, y `Guides/Notas.GitHub.md` —sin versionar— dice que el repositorio es
público y describe qué tildar en la configuración de la organización para exigir aprobación a los
pull requests de colaboradores externos.

**Interpretación.** Sin esa configuración —que vive en GitHub y no en el repositorio, así que **desde
acá no se puede verificar**—, un PR desde un fork ejecutaría código sin revisar en la máquina propia.
Es la consecuencia directa de haber sumado `pull_request` sin cambiar el runner. Que la nota exista y
esté sin versionar sugiere que se detectó y todavía no se cerró.

### 11, 12 y 13. Documentación desalineada

**Hecho.** `Guides/GitHub-Action.md` tiene 0 líneas, está declarado en
`Ejemplos.WebBlazor.E2E.Base.slnx` y el `README.md` lo enlaza como «la corrida en CI».
`Guides/E2E-Guides.md` transcribe el `.razor` de `HolaMundo` con `class="form-control"` y `@onclick`
(líneas 90 y 101) y el workflow con `schedule` y `concurrency` y sin `pull_request` (líneas 176-199).
`Guides/Notas.GitHub.md` figura como `??` en `git status`.

**Interpretación.** La guía E2E enseña una versión anterior de la superficie; lo que sigue vigente de
ella son los tres `data-testid` y todo el material sobre Playwright, NUnit y la instalación de
navegadores, que no dependen de la maqueta. La guía de GitHub Actions sigue reservada y no escrita, y
ahora tiene más para contar que antes: el disparador nuevo y el riesgo del runner.

### 14 y 15. Lo que se resolvió desde el indexado anterior

**Hecho.** El `README.md` pasó de una línea a un documento con la tabla de los dos proyectos, la
mención del template y los enlaces a las tres guías y a la evidencia. Las dos rutas de
`MovilidadUrbana` del workflow se reemplazaron por expresiones derivadas de `PROYECTO_PRUEBAS` y
`PATH_PROJECT_FILE`.

## Lo que sí está completo y funciona como ejemplo

Para no dejar una impresión sesgada:

- La superficie `HolaMundo` y su prueba siguen siendo un ejemplo **cerrado y coherente**: los tres
  `data-testid` con sus tres llamados de Playwright comentados al lado, y la distinción entre
  `ToHaveValueAsync` y `ToHaveTextAsync`.
- El acceso está **bien resuelto y bien comentado**: la credencial se emite en endpoints POST fuera
  del circuito, el rechazo es indiferenciado, los textos salen de un catálogo, `DestinoSeguro()`
  ataja el *open redirect* y el guard existe en las tres capas.
- La aplicación del template está **documentada y verificada**: `Guides/Template-SDD-Aplicado.md`
  declara qué se aplicó, qué se decidió y cómo se comprobó, y la corrida quedó versionada con su log
  y sus doce capturas — ver [06_Template-Y-Superficies.md](06_Template-Y-Superficies.md).
- `Guides/E2E-Guides.md` sigue cubriendo la creación del proyecto, el ejemplo completo y el anexo
  sobre la instalación de navegadores.

## Cómo verificar todo esto

| Afirmación | Comprobación |
| --- | --- |
| Puertos | `grep applicationUrl src/*/Properties/launchSettings.json` frente a las URL de `tests/` |
| Dos `Setup` en la misma clase | `grep -n 'Task Setup' tests/WebBlazor.E2E.Base.Login.E2ETests/HolaMundoE2ETest.cs` |
| `estado-app` no existe | `grep -rn 'estado-app' src/` (sin resultados) |
| `pruebas.runsettings` | `ls pruebas.runsettings` |
| Entradas no declaradas | `grep -n 'inputs\.' .github/workflows/e2e.yml` frente al bloque `workflow_dispatch` |
| Runner y disparador | `grep -n 'runs-on\|pull_request' .github/workflows/e2e.yml` |
| Guía vacía | `wc -l Guides/GitHub-Action.md` |
| Archivos sin versionar | `git status --porcelain` |
