# Tool-Prompt — Extracción de comportamientos. 

> **Invocación**: Leer y ejecutar `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Analisis/01-Extraer-Template-SDD-Default/Extraer-Template-SDD-Default.md`
>
> **Overview**:  Extracción de comportamientos del template de SDD Default

---

## Contexto

  Leer `/IA/SDD/IA.SDD/README.md` trata sobre un `Framework SDD` 

  Leer `/IA/SDD/IA.SDD/Conocimiento/README.md`, trata sobre la `estructura de como se guarda en la base de conocimientos desacoplada` conocimientos sobre procedimientos y forma de hacer las cosas que pueden estar al alcance de los requerimientos que se requiera por parte del desarrollo del diseño por especificación.

  La maqueta:  `/PROG2/Geometria/Lab-Geometria/SDD/Maquetas/GeometriaFactory-Web` es `Maqueta generada por el Framework SDD`.

---

## Objetivos

  Extraer Base de conocimientos nuevo

---

## Solicitudes

  Teniendo en cuenta que quiero generés dos documentos como dicta: `estructura de como se guarda en la base de conocimientos desacoplada`, con la base de conocimiento que el `Framework SDD` a capturado como comportamiento de sus subagentes especializados en UX y UI dados en el contexto, extrayendo como se estructura y resuelven la codificación, UX y UI bajo la tecnología que se esta usando:

  1. Generar un documento con el conocimiento estructurado de como se haría un template con diferentes tipos de abms, puede ser un abm clásico, un asistentes de varios niveles , como ejemplo podes tomar 3 o 4 niveles, uso de ventanas modales. El objetivo debe estar pensado para que un agente IA pueda construir una maqueta html/css tal como si los agentes IA siguiesen esas reglas estrictamente o bien como si las personas que codearon la `Maqueta generada por el Framework SDD`. Catalogalo a este como: `Template-HTML-SDD-Default`. Revisa esta `Maqueta generada por el Framework SDD` para contrastar tu fuente de conocimiento lograda.

  2. Heredando el documento anterior: `Template-HTML-SDD-Default`, genera otro documento con el conocimiento estructurado de como se haría un template con diferentes tipos de abms, pero ahora en .NET Blazor interactive server, con excepción de las páginas para que el usuario se loguee, se pueden evaluar como ejemplos un abm clásico, un asistentes de varios niveles , como ejemplo podes tomar 3 o 4 niveles, uso de ventanas modales. La página de logueo se le aplica el mismo template html que el resto, pero esta no puede ser interactive server porque tiene que generar las cookies. En este Conocimiento vas a tener que reeplantearlo sin el uso de la librería MudBlazor, es decir Blazor interactive server puro. El objetivo debe estar pensado para que un agente IA pueda codear un proyecto de igual como dictan las reglas del Framework `Framework SDD `. Catalogalo a este como: `Template-Blazor-Interactive-Server-SDD-Default`

  Intenta extraer y catalogar y estructurar lo mejor que puedas los tipos de dialogos normados por el `Framework SDD` (abms, asistentes, menus, pantallas modales, presentación de datos), en cuanto al estilo de experiencia de usuario e intefaces de usuarios. No dudes en incluir ejemplos y lo necesarios para que los agentes IA interprenten adecuadamente lo logrado y lo que se quiere lograr.

  Estos dos documentos, no quiero que queden en bajo incorporados directamente el repositorio del `Framework SDD`, así que dejalos en `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Analisis/01-Extraer-Template-SDD-Default/OUTPUTs` así luego, el cliente que use `Framework SDD` los suma el en su fork de este framework.
  
  Te aconsejos que te bases en `/IA/PROMPTs/IA.Prompts/Base/Mesa-Evaluadora.md` para organizar una mesa evaluadora, y planificadora para relevar caracteristicas, clasificarlas, estructurarlas y clasificarlas adecuadamente y transcribirlas. Incopora los especialista necesarios, dales toda la autoridad para tomar decisiones necesarias para cumplir con los objetivos y/o necesidades demandadas.

---

## Reglas

  - No inventar información. 
  - Toda afirmación debe estar respaldada por evidencia verificable.
  - No modificar el `Framework SDD`