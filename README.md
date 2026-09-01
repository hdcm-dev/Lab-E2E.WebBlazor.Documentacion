# Lab-E2E.WebBlazor.Documentacion

Documentación del laboratorio [Lab-E2E.WebBlazor](../Lab-E2E.WebBlazor): una aplicación .NET Blazor
con render *interactive server* usada para practicar pruebas de extremo a extremo con Playwright y su
integración en la cadena de desarrollo con GitHub Actions.

## ia-db

Base de conocimiento indexada, pensada para que un agente de IA responda sobre los laboratorios sin
recorrerlos enteros. Cada workspace tiene su `README.md` como punto de entrada único, y desde ahí una
tabla de navegación indica qué índice cargar.

| Workspace | Indexa | Punto de entrada |
| --- | --- | --- |
| [ia-db/Root/](ia-db/Root/) | [Lab-E2E.WebBlazor](../Lab-E2E.WebBlazor) — la aplicación, sus pruebas y su pipeline | [ia-db/Root/README.md](ia-db/Root/README.md) |
| [ia-db/Base/](ia-db/Base/) | [Lab-E2E.WebBlazor.Base](../Lab-E2E.WebBlazor.Base) — el andamiaje mínimo previo, en construcción | [ia-db/Base/README.md](ia-db/Base/README.md) |

## Guías

Las guías de estudio viven en el propio laboratorio, junto al código que citan:

| Documento | Para quién | Qué deja |
| --- | --- | --- |
| [Beginner-Guide.md](../Lab-E2E.WebBlazor/Guides/E2E-Guide/Beginner-Guide.md) | Quien nunca escribió una prueba E2E | Anatomía del proyecto E2E en .NET, criterios sobre qué testear, cómo se escribe y estabiliza un caso, y cómo se atan las pruebas al merge de un pull request con GitHub Actions |
| [Quick-Guide-ABM.md](../Lab-E2E.WebBlazor/Guides/E2E-Guide/Quick-Guide-ABM.md) | Quien ya escribió pruebas E2E y necesita el camino corto | Los siete pasos para montar las pruebas de un ABM, las trampas propias de Blazor *interactive server* y una lista de verificación |

## PROMPTs

Los archivos de [PROMPTs/](PROMPTs/) registran las instrucciones con las que se generaron el
laboratorio y esta documentación, ordenadas por tipo de encargo: `Solicitudes/`, `Analisis/`,
`Features/` e `Indexado/`. Los que producen artefactos los dejan en su propia carpeta `OUTPUTs/`.
