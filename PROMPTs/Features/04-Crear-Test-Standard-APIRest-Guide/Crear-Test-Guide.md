# Tool-Prompt —  Crear test guides

> **Invocación**:
> - Leer y ejecutar `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Features/04-Crear-Test-Standard-APIRest-Guide/Crear-Test-Guide.md`
>
> Overview:  Crear test guides

---

## Contexto


  Leer `/LAB/Lab-E2E.WebBlazor.Documentacion/ia-db/README.md`, tengo una solución .net con varios proyectos ejemplos en los que se aplica pruebas E2E PlayWright. Ahora hay otro `MovilidadUrbana.ApiWeb` que es una aplicación restapi y se cuenta con `MovilidadUrbana.MAUI` que es una aplicación MAUI

  Leer `LAB/Lab-E2E.WebBlazor.Documentacion/Guides/E2E-Guide` son guías, apuntes y casos de estudio sobre pruebas end to end, E2E.

  Lo que se hace necesario es comprender la gama de pruebas automatizadas que se aplican en proyectos de esta naturaleza tanto web, como restapi. Ahora he abarcadolos test E2E con playwright el cual requiere acceso al DOM a traves de un navegador, pero hay otros que se basan en la posición de la pantalla por ejemplo casos en que quisiera aplicarlo a pruebas sobre aplicaciones móviles donde no hay acceso al DOM, y las unitest que son aplicables entidades de dominio, etc. Cada cual la industria los propone de acuerdo a su entorno,finalidad y objetivos que se persiguen. Tener en cuenta conceptos de arquitecturas de proyectos , como la clean, conceptos de objetos mock, pruebas sobre la capa de base de datos. 

---

## Objetivos

   Construir un documento guia que permita entrar en contexto que tipo de pruebas automatizadas hay, como se aplican , en que tipo de proyecto se aplican, situación, criterios de diseño, enmarcados en soluciones .NET que van desde maui hasta.  

---

## Solicitudes

  - Se requiere elaborar y editar un documento markdown que introduzca en el dominio de pruebas y pruebas de pruebas de productos/proyectos de software en diferentes ambitos y estrategias y/o arquitecturas. Luego se debería plantear otro documento markdown para lo que son los conceptos de pruebas unitarias en las diferentes arquitecturas, y otro documento markdown que introduzca sobre lo que son las pruebas sobre aplicaciones de escritorios/móviles (por posición en pantalla). Los documentos se deben dejar en `/LAB/Lab-E2E.WebBlazor.Documentacion/Guides/Test-Guide`. 

---

## Reglas
  - Los documentos markdown de documentación deben estar organizados en secciones jerárquicas con índices. Deben incluir definiciones, explicaciones, ejemplos claros y en cuando sea necesario gráficos mermaid. Deben ser autocontenidos, no delta. Debe tener ejemplos explicaciones, snipped de código representativos, preguntas guías con respuestas explicativas formadoras de criterios que permitan o sirvan al lector identificar en que caso se aplica que, y dar enfoque al diseño de pruebas.
  - No inventar información. 
  - Toda afirmación debe estar respaldada por evidencia verificable.

---

## Framework

## Profile

  Aplicar:
  - `/IA/IA.Prompts/PromptFramework/Profiles/Study-Guide-Documentation.md`
  

