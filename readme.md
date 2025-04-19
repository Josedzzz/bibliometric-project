## Proyecto final de análisis de algoritmos

El objetivo central de este proyecto:

1. Obtener metadatos (en formato RIS) de publicaciones sobre "computational thinking" desde plataformas académicas.
2. Proecesos esos datos obtenidos para cumplir los requerimientos específicos (unificación, estadísticas, análisis de texto).

## Apuntes y pasos que voy a seguir

Esto es un intento de centrar un poquito el corto desarrollo del proyecto, sin llegar a la granularidad del desarrollo de software realmente.

1. Extracción de metadatos
- Las fuentes que se usaron: ScienceDirect, IEEE Xplore y ACM Digital Library.
- Por ahora, se descargaron los archivos RIS manualmente, pero, eventualmente se hará un scrapper para obtener todos los archivos de las 3 fuentes que se usaron. Si no le ingresó una cantidad de datos decente, ¿Cómo puedo comprobar que quedó el proyecto bien? Aunque, que estoy sea en Python me preocupa un poco sobre su eficiencia.
- También se puede hacer que la búsqueda no quede limitada a "computational thinking".
 
2. Unificación y limpieza (Requerimiento 1)
- Hay que unificar los archivos RIS de las distintas plataformas en uno solo, aunque queda la duda de cómo comprobar que dos artículos son iguales, claramente hay valores estáticos como el DOI o ISBN, pero, ¿Qué pasa si no están estos valores? ¿El formato RIS o cualquier formato me garantiza igualdad de metadatos del artículo independiente de dónde se encuentre alojado? ¿Qué criterio de comparación toma en cuenta todos los casos extremos? 
- Mientras se unifica, también hay que tener en cuenta los artículos que se repiten, ya que, se necesita guardar estos en otro archivo.
- Básicamente, de este requerimiento sale dos archivos: unificado.ris y duplicado_eliminado.ris.

3. Generación de estadísticas (Requerimiento 2)
- Luego, con la ayuda del requerimiento 1, hay que generar estadísticas como:
    - Autores más frecuentes
    - Años de publicación por tipo (artículo, conferencia, etcétera)
    - Publishers más comunes (?)
Se puede hacer fácil con las librerías de Python la verdad.


