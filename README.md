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

**Cada documento abre con un abstract** —*de qué va, para quién, qué deja*— y con su índice, así que
la tabla de abajo alcanza para elegir cuál abrir.

### [Guides/E2E-Guide/](Guides/E2E-Guide/) — pruebas de extremo a extremo

Se leen en este orden si es la primera vez; si no, por la columna del medio.

| Documento | Para quién | De qué va |
| --- | --- | --- |
| [Mapa-Del-Conjunto.md](Guides/E2E-Guide/Mapa-Del-Conjunto.md) | Quien llega y no sabe por dónde entrar | Qué documento responde a qué pregunta, cómo se cruzan los dos vocabularios y quién es dueño de cada tema |
| [Del-Requerimiento-Al-Caso.md](Guides/E2E-Guide/Del-Requerimiento-Al-Caso.md) | Quien recibe un pedido y no tiene nada escrito | Cómo se llega de un problema contado en desorden hasta superficies, promesas y estados, antes de que exista una pantalla. **Método propuesto**: su §10 declara qué tiene respaldo y qué no |
| [Quick-Guide-Primer-Proyecto.md](Guides/E2E-Guide/Quick-Guide-Primer-Proyecto.md) | Quien nunca creó un proyecto de pruebas | Cómo se crea el proyecto NUnit con Playwright y se escribe la primera prueba |
| [Beginner-Guide.md](Guides/E2E-Guide/Beginner-Guide.md) | Quien nunca escribió una prueba E2E | Qué es una E2E, cómo se arma el proyecto en .NET, cómo se escribe y se estabiliza un caso, y cómo se ata al merge |
| [Quick-Guide-ABM.md](Guides/E2E-Guide/Quick-Guide-ABM.md) | Quien ya escribió pruebas E2E | La receta corta para montar las de un ABM, con las trampas de Blazor *interactive server* |
| [Caso-HolaMundo-Page.md](Guides/E2E-Guide/Caso-HolaMundo-Page.md) | Quien tiene que decidir **qué** probar | El caso mínimo: superficie, estados y el testigo de hidratación |
| [Caso-Login-Page.md](Guides/E2E-Guide/Caso-Login-Page.md) | Ídem, con postura de seguridad | La promesa negativa, que se verifica comparando dos observaciones |
| [Caso-Encuesta-Page.md](Guides/E2E-Guide/Caso-Encuesta-Page.md) | Ídem, con un acto divisible | Por qué tres pasos de un asistente son **una** superficie y no tres |
| [Marco-La-Superficie-Verificable.md](Guides/E2E-Guide/Marco-La-Superficie-Verificable.md) | Quien quiere ir más lejos | De qué tradición viene cada concepto, con bibliografía y con lo que se reinventó sin saberlo |
| [Template-SDD-Aplicado.md](Guides/E2E-Guide/Template-SDD-Aplicado.md) | Quien construye la superficie | Qué se aplicó del template SDD, qué se decidió al aplicarlo y cómo se verificó |
| [Notas.GitHub.md](Guides/E2E-Guide/Notas.GitHub.md) | Quien administra el repositorio | Cómo se evita que un pull request desde un fork corra en el runner propio |

### [Guides/](Guides/) — ramas, integración y releases

| Documento | Para quién | De qué va |
| --- | --- | --- |
| [Estandares-Modelo-Ramas.md](Guides/Estandares-Modelo-Ramas.md) | El equipo entero | Qué modelos de ramas hay, cómo se elige uno y cómo se opera el ciclo de vida de las versiones |
| [Guia-Practica-GitFlow.md](Guides/Guia-Practica-GitFlow.md) | Un equipo de tres que rota roles | Los ocho escenarios ejecutables del modelo adoptado |
| [Guia-Practica-GitHubFlow.md](Guides/Guia-Practica-GitHubFlow.md) | Ídem | Los mismos ocho sobre el modelo que **no** se adoptó, como línea de base |
| [GitHub-Action-Guide.md](Guides/GitHub-Action-Guide.md) | Quien nunca escribió un workflow | Vocabulario, sintaxis y escenarios completos, con ejemplos que corren en este workspace |
| [Anexos/workflows/](Guides/Anexos/workflows/README.md) | Quien monta la CI | Los tres workflows listos para copiar |

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
