---
doc_id: GF-AX-WF
doc_type: anexo
title: Anexo — workflows del procedimiento
status: vigente
origin: agente
confidence: media
owner: Lab-GitFlow
last_review: 2026-08-23
audience: [devops, desarrollo]
traces: [GF-08, GF-09-00]
---

# Anexo — workflows

Los tres archivos de esta carpeta completan el pipeline para operar el modelo de tronco con ramas de
release. Se copian a `.github/workflows/` del repositorio de práctica en el
[escenario 00](../../Guia-Practica-GitFlow.md#2-escenario-00--preparación).

| Archivo | Disparadores | Qué hace |
|---|---|---|
| [`ci.yml`](ci.yml) | `pull_request` y `push` a `main` y `release/**`, `merge_group` | Verificación rápida, regresión E2E y check resumen para la protección de rama |
| [`release.yml`](release.yml) | `push` de un tag `v*` | Verifica la referencia etiquetada, construye el artefacto **una vez** y publica la versión |
| [`auditoria-convergencia.yml`](auditoria-convergencia.yml) | diario, `push` a `release/**`, y a pedido | Detecta correcciones de release que nunca volvieron a `main` |

**`ci.yml` reemplaza** al que trae la aplicación sembrada. Aquel solo se dispara sobre `main`; este
protege además las ramas `release/**`, que es precisamente donde el equipo tenía el hueco.

## Lo que estos archivos dan por sentado

- Existe `.github/workflows/e2e.yml`, el workflow reutilizable que define **cómo** se corren las
  pruebas y que viene con la aplicación sembrada. Sus entradas de `workflow_call` son exactamente
  cuatro: `navegadores`, `url-base`, `referencia` y `retencion-dias`. **[F: GHA-1]** No declara
  reparto en shards, así que ningún llamador puede pasarle `cantidad-shards`: GitHub Actions
  rechaza la corrida como workflow inválido.
- El proyecto .NET está en `src/MovilidadUrbana.Web`, la solución en `Lab-E2E.WebBlazor.sln` y las
  pruebas de extremo a extremo en el proyecto **.NET** `tests/MovilidadUrbana.E2ETests`, que se
  ejecutan con `dotnet test` y `pruebas.runsettings`. No hay `package.json`, ni `e2e/`, ni
  `playwright.config.js`: el binding usado es el de .NET.
- Existe el runner autoalojado con las etiquetas `self-hosted` e `i7infra-dev`. Sobre un runner
  alojado de GitHub alcanza con cambiar el `runs-on:` por `ubuntu-latest`.
- El repositorio de práctica es **privado y sin colaboradores externos**, o bien tiene activada la
  aprobación manual de corridas provenientes de forks. Un runner autoalojado es una máquina
  persistente: en el evento `pull_request` se ejecuta el `ci.yml` *de la rama del pull request*,
  todavía sin revisar, con acceso al estado que dejaron las corridas anteriores y a la red interna.
  Si esa condición no se cumple, el pipeline es ejecución remota de código de terceros. **[C]**

Antes de copiar los archivos conviene comprobar el contrato contra el archivo real, no contra esta
descripción:

```bash
grep -n 'cantidad-shards' ../../../../Lab-E2E.WebBlazor/.github/workflows/e2e.yml   # no debe haber salida
sed -n '/workflow_call:/,/outputs:/p' ../../../../Lab-E2E.WebBlazor/.github/workflows/e2e.yml
```

## Decisiones que conviene entender antes de copiar

**Ejecución directa sobre el runner, sin `container:`.** El aislamiento en contenedor sería
preferible —**[F: PW-1]** Playwright publica su imagen precisamente para eso—, pero no es una opción
sobre el runner exigido por el contrato: `e2e.yml` documenta que `i7infra-dev` es él mismo un
contenedor, sin acceso al demonio de Docker, y que ya trae el SDK de .NET 10 sobre Ubuntu 24.04. Por
eso los tres workflows de esta carpeta corren directo sobre el runner, igual que `e2e.yml`, y los
navegadores los instala el CLI de Playwright que viene dentro del paquete de .NET. La contrapartida
es real y conviene tenerla anotada: la reproducibilidad depende del estado del runner. **[C]**

**Un solo check obligatorio.** La protección de rama exige `CI aprobada` y nada más. Listar cada job
obliga a editar la configuración del repositorio cada vez que cambia la matriz, y es la razón por la
que las reglas de protección terminan desactualizadas.

**Permisos mínimos.** `contents: read` salvo en `release.yml`, que necesita `contents: write` para
publicar la versión.

**La auditoría compara por contenido.** `git cherry` es la herramienta correcta porque el SHA cambia
siempre al hacer cherry-pick. Requiere `fetch-depth: 0`: con un clon superficial no hay historia que
comparar.

## Estado de verificación

**Parcialmente verificado.** Los tres archivos parsean como YAML. La lógica de
`auditoria-convergencia.yml` —la más frágil de las tres, porque es un script de shell con tuberías
bajo `set -euo pipefail`— se ejecutó fuera de GitHub Actions, sobre un repositorio de prueba armado
al efecto con una rama de release que tenía dos correcciones sin retorno a `main`, una de ellas con
el encabezado `Convergencia:` en su mensaje. **[E: corrida local del 2026-08-23]** El resultado fue
el declarado: la marcada con `Convergencia:` se excluyó, la otra se reportó como `::error::`, el
contador del resumen dio `1` y el job terminó en `exit 1`. El camino en verde —una rama de release
sin divergencias— dio contador `0` y salida `0`.

`ci.yml` **sí corrió en GitHub Actions**, sobre el runner `i7infra-dev` y con la aplicación sembrada
en `Lab-GitFlow`. **[E: corrida del 2026-08-25]** Terminó en verde y encadenó lo que declara: la
verificación rápida, la publicación de la aplicación, la matriz de pruebas con sus cuatro
configuraciones de navegador, el reporte unificado y el job resumen `CI aprobada`. El disparador fue
un `push` a `main`, y la matriz salió completa —los cuatro navegadores—, que es lo que el
procedimiento reserva para lo ya integrado.

Con eso quedan verificados también dos supuestos que hasta ahora se afirmaban leyendo los archivos:
que los jobs arrancan sin `container:` sobre ese runner, y que el contrato con el workflow
reutilizable `e2e.yml` de la aplicación es el correcto.

Lo que sigue **sin verificar** son los otros dos, y por un motivo simple: sus disparadores no se
dieron todavía. `release.yml` se activa con un tag `v*`, que produce el
[escenario 03](../../Guia-Practica-GitFlow.md#5-escenario-03--corte-de-release-e-03-y-e-04), y
`auditoria-convergencia.yml` con un `push` a `release/**` o por horario, que llega con el mismo
escenario. Su lógica de shell sí está comprobada, pero fuera de Actions.
