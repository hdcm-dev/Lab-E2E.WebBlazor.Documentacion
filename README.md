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

Toda la documentación de los dos laboratorios vive acá, en [Guides/](Guides/). Antes estaba
repartida entre los dos repositorios de código, con el riesgo de que dos copias del mismo texto
divergieran en silencio.

### [Guides/E2E-Guide/](Guides/E2E-Guide/) — pruebas de extremo a extremo

| Documento | Para quién | Qué deja |
| --- | --- | --- |
| [E2E-Resumen.md](Guides/E2E-Guide/E2E-Resumen.md) | Quien llega por primera vez | Del requerimiento al caso: cómo se deducen superficies, promesas y estados antes de que exista una pantalla, más el mapa del resto de los documentos |
| [Quick-Guide-Primer-Proyecto.md](Guides/E2E-Guide/Quick-Guide-Primer-Proyecto.md) | Quien nunca creó un proyecto de pruebas | Cómo se crea el proyecto NUnit con Playwright y se escribe la primera prueba, con el Explorador de pruebas de Visual Studio |
| [Beginner-Guide.md](Guides/E2E-Guide/Beginner-Guide.md) | Quien nunca escribió una prueba E2E | Anatomía del proyecto E2E en .NET, criterios sobre qué testear, cómo se escribe y estabiliza un caso, y cómo se atan las pruebas al merge de un pull request con GitHub Actions |
| [Quick-Guide-ABM.md](Guides/E2E-Guide/Quick-Guide-ABM.md) | Quien ya escribió pruebas E2E y necesita el camino corto | Los siete pasos para montar las pruebas de un ABM, las trampas propias de Blazor *interactive server* y una lista de verificación |
| [Caso-HolaMundo-Page.md](Guides/E2E-Guide/Caso-HolaMundo-Page.md) | Quien tiene que decidir **qué** probar | El caso mínimo: una superficie interactiva, sus estados y el testigo de hidratación |
| [Caso-Login-Page.md](Guides/E2E-Guide/Caso-Login-Page.md) | Ídem, con postura de seguridad | Una superficie SSR detrás de un acceso, y la promesa negativa que se verifica comparando dos observaciones |
| [Caso-Encuesta-Page.md](Guides/E2E-Guide/Caso-Encuesta-Page.md) | Ídem, con un acto divisible | Por qué los tres pasos de un asistente son **una** superficie y no tres |
| [Marco-La-Superficie-Verificable.md](Guides/E2E-Guide/Marco-La-Superficie-Verificable.md) | Quien quiere ir más lejos | De qué tradición viene cada concepto, con bibliografía y con lo que se reinventó sin saberlo |
| [Template-SDD-Aplicado.md](Guides/E2E-Guide/Template-SDD-Aplicado.md) | Quien construye la superficie | La forma constructiva: tokens, componentes propios y estados declarados |

### [Guides/](Guides/) — ramas, integración y releases

| Documento | De qué trata |
| --- | --- |
| [Estandares-Modelo-Ramas.md](Guides/Estandares-Modelo-Ramas.md) | La elección entre modelos de ramas, el adoptado y sus guardarraíles |
| [Guia-Practica-GitFlow.md](Guides/Guia-Practica-GitFlow.md) | Ocho escenarios ejecutables sobre el modelo adoptado |
| [Guia-Practica-GitHubFlow.md](Guides/Guia-Practica-GitHubFlow.md) | El modelo que **no** se adoptó, como línea de base |
| [GitHub-Action-Guide.md](Guides/GitHub-Action-Guide.md) | La corrida en integración continua |

Los documentos de `E2E-Guide/` citan el código de los dos laboratorios por ruta relativa, así que
se leen mejor con los tres repositorios clonados como carpetas hermanas.

## PROMPTs

Los archivos de [PROMPTs/](PROMPTs/) registran las instrucciones con las que se generaron los
laboratorios y esta documentación, ordenadas por el workspace al que apuntan:

| Carpeta | Encarga sobre |
| --- | --- |
| [PROMPTs/Root/](PROMPTs/Root/) | [Lab-E2E.WebBlazor](../Lab-E2E.WebBlazor) — `Inicio/` la creación de la solución, `Features/` los cambios posteriores |
| [PROMPTs/Base/](PROMPTs/Base/) | [Lab-E2E.WebBlazor.Base](../Lab-E2E.WebBlazor.Base) — el andamiaje mínimo previo |
| [PROMPTs/Analisis/](PROMPTs/Analisis/) | Estudios que no modifican código, con su resultado en `OUTPUTs/` |
| [PROMPTs/Indexado/](PROMPTs/Indexado/) | La generación y el refresco de `ia-db/` |

Los que producen artefactos los dejan en su propia carpeta `OUTPUTs/`.
