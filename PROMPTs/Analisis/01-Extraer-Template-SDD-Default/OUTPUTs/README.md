# OUTPUTs — Extracción del template SDD por defecto

**Fecha:** 2026-09-01
**Producido por:** ejecución de `../Extraer-Template-SDD-Default.md`

---

## 1. Qué hay acá

Dos documentos de conocimiento escritos contra el contrato de
`IA.SDD/SDD/Devs/Rules/Rules-Base-Conocimiento.md` 2.2, más las filas de índice que les corresponden y
el registro de la mesa que los produjo.

| Archivo | Alias | Qué es |
| --- | --- | --- |
| `Knowledge-Template-HTML-SDD-Default.md` | `Template-HTML-SDD-Default` | Forma constructiva de una maqueta HTML/CSS/JS del framework, con los cuatro tipos de diálogo |
| `Knowledge-Template-Blazor-Interactive-Server-SDD-Default.md` | `Template-Blazor-Interactive-Server-SDD-Default` | El delta para realizar ese template en Blazor Interactive Server sin librería de componentes |
| `Index-Knowledge-Filas.md` | — | Las dos filas listas para pegar en el índice de la base del fork |
| `Registro-De-Mesa.md` | — | Convocatoria, hallazgos, veredictos, deuda declarada y escaladas |

**No se tocó el Framework SDD.** Estos archivos viven acá a propósito: el cliente que use el framework
los suma en su fork, junto con las dos filas de `Index-Knowledge-Filas.md`.

## 2. Cómo se incorporan a un fork

1. Copiar los dos `Knowledge-*.md` a `Conocimiento/` del fork.
2. Pegar las dos filas de `Index-Knowledge-Filas.md` en la §3 del `Index-Knowledge.md` de esa base.
3. Correr la verificación de ofuscación del fork si es público, y la lista de comprobación de
   `Rules-Base-Conocimiento.md` §6.1.
4. Registrar el alta como intervención sobre el framework: entrada en el `CHANGELOG.md`, copia del
   conjunto superado a `_legacy/` y, si alcanza a varios archivos, nota de coherencia.
5. Desde el intake de un producto, citar el alias que corresponda.

## 3. Advertencia sobre el techo de tamaño

Los dos documentos son de naturaleza `propio` y superan las 600 líneas de
`Rules-Base-Conocimiento.md` §6.2. Los dos se acogen a la excepción de §4.3 y §6.2 —el §5 de esqueletos
no se puede partir sin volverlo inútil— y lo declaran en su §0. Es una excepción legítima del contrato,
pero es la primera comprobación que va a fallar si alguien corre la lista de §6.1 sin leer el §0.
