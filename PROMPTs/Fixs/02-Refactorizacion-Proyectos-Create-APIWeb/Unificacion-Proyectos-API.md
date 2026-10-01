# Tool-Prompt —  Unificacion-Proyectos

> **Invocación**: Leer y ejecutar `/LAB/Lab-E2E.WebBlazor.Documentacion/PROMPTs/Fixs/02-Refactorizacion-Proyectos/Unificacion-Proyectos.md`
>
> **Overview**:  Unificacion-Proyectos

---

## Contexto

  Leer `/LAB/Lab-E2E.WebBlazor.Documentacion/ia-db/README.md`. 

  Recientemente se ha unificado dos repositorios quedando una solución de visualstudio con varios proyectos.

---

## Objetivos

  Refactorizar proyectos

---

## Solicitudes

  Renombrar los siguientes proyectos:
  - `WebBlazor.E2E.Base.HolaMundo` a `WebBlazor.HolaMundo` - consecuentemente tambien `WebBlazor.E2E.Base.HolaMundo.E2ETests` a `WebBlazor.HolaMundo.E2ETests`
  - `WebBlazor.E2E.Base.Login` a `WebBlazor.Login` - consecuentemente renombrar `WebBlazor.E2E.Base.Login.E2ETests` a `WebBlazor.Login.E2ETests`.

  En todos y cada uno de los proyectos mencionados ajustar los espacios de nombres y ajustar las referencias en el archivo de solución de visualstudio como en la documentación en la que hace referencia.

  Crear en base al proyecto `MovilidadUrbana.Web` una versión dada en un RestAPI Web Dot NET 10 con dos controllers uno para localidades y otro para la encuesta, el proyecto nuevo debería llamarse `/MovilidadUrbana.ApiWeb` . Respeta la arquitectura clean. sigue los estandares de la industria en .net. 

---

## Reglas

  - No inventar información. 
  - Toda afirmación debe estar respaldada por evidencia verificable.