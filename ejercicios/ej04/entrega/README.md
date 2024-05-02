## Enunciado Trabajo Práctico 4

Efectos distorsivos del canal y de otros bloques analógicos.


### Objetivo

Familiarizarse con las fuentes de distorsión de las señales transmitidas
y sus efectos.


### Descripción

Este ejercicio se realiza de manera interactiva durante la clase.

Se discuten los distintos tipos de efectos distorsivos que pueden afectar
a las señales y a los símbolos recibidos, y cómo éstos pueden ser observados
en las constelaciones.

Utilizamos un
[jamboard](https://jamboard.google.com/d/1LToahZ0TIewaAYAcWZ0Mm2Ba-7jCZsp1kE0DuLKNmiI/edit?usp=sharing)
para dejar plasmados los conceptos.


### Entrega

Se debe crear el archivo `README.md` incluyendo imágenes capturadas del jamboard:
- Se deben realizar capturas del jamboard.
- Se deben subir las imágenes al repositorio.
- Se deben incluir las imágenes en el archivo Markdown de la entrega.


---
---
---

## Respuestas

Algunas de las fuentes de distorsión de las señales transmitidas y sus efectos.

    - *Ruido*: En la constelación se genera una nube de puntos.
![Ruido](Jam01.png)

    - *Error de sincronismo de portadora*: Se genera una pequeña rotación (error de fase) en los puntos del diagrama de constelación o una rotación continua (error de frecuencia).
![Error de sincronismo de portadora](Jam02.png)

    - *Error de sincronismo de símbolo*: La amplitud varia y generalmente puede disminuir. Se genera interferencia inter-símbolo.
![Error de sincronismo de símbolo](Jam03.png)

    - *Interferencia inter-símbolo*: Un punto tiende hacialos otros puntos.
![Interferencia inter-símbolo](Jam04.png)

    - *Alinealidad*: Cuando el canal no es lineal se produce que los puntos pierden un poco de potencia.
![Alinealidad](Jam05.png)

    - *I-Q Impairment (amplitud)*: Cuando no estan perfectamente en amplitud se comprime en una de las direcciones.
![I-Q Impairment (amplitud)](Jam06.png)

    - *I-Q Impairment (fase)*: Se pierde la ortogonalidad cuando no se encuentran perfectamente en fase.
![I-Q Impairment (fase)](Jam07.png)