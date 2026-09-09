# Notas de configuración del repositorio en GitHub

> **De qué va** — Cómo se configura el repositorio para que un pull request desde un fork no ejecute código sin revisar en el runner propio.
> **Para quién** — Quien administra el repositorio.
> **Qué deja** — La opción exacta de *Settings* y las casillas que corresponden.

## La opción que hay que tocar

> Para que usuarios que hagan fork no corran el runner

Desde la configuración de la organización

El repo es público y los jobs corren en i7infra-dev. Este push activa el disparador, y a partir de ahí un PR desde un fork ejecuta código sin revisar en tu máquina. La opción más rápida sin cambiar nada más es ***Settings → Actions → General → Fork pull request workflows from outside collaborators*** → Require approval for all outside collaborator o poner el repo en privado

Fork pull request workflows in private and internal repositories
[ x ]  Run workflows from fork pull requests
  [   ]  Send write tokens to workflows from fork pull requests.
  [   ]  Send secrets and variables to workflows from fork pull requests.
  [ x ]  Require approval for fork pull request workflows.
