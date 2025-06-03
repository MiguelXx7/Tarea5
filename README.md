# Tarea: Simulaciones Interactivas con Python, Docker y ROS

Esta tarea reúne tres ejercicios prácticos desarrollados en Python e integrados mediante contenedores Docker. Cada ejercicio representa un enfoque diferente para aplicar conceptos relacionados con control automático, desarrollo de videojuegos 2D y comunicación distribuida en robótica. El propósito es aplicar conocimientos de programación, simulación e integración de entornos de ejecución, de manera técnica y reproducible.

## Contenido

1. [Seguidor de línea con PID y Tkinter](#1-seguidor-de-l%C3%ADnea-con-pid-y-tkinter)
2. [Videojuego SpaceMax Defender en Pygame](#2-videojuego-spacemax-defender-en-pygame)
3. [Simulación básica ROS con talker-listener y turtlesim](#3-simulaci%C3%B3n-b%C3%A1sica-ros-con-talker-listener-y-turtlesim)
4. [Instrucciones generales de instalación](#4-instrucciones-generales-de-instalaci%C3%B3n)
5. [Créditos y licencia](#5-cr%C3%A9ditos-y-licencia)

---

## 1. Seguidor de línea con PID y Tkinter

### Descripción

Este ejercicio simula el comportamiento de un robot móvil que sigue una pista utilizando sensores virtuales y un controlador PID. La interfaz gráfica fue construida con `tkinter`, permitiendo visualizar el movimiento del carro, el rastro y la detección de la pista.

### Características técnicas

* Control PID con ajuste dinámico.
* Interfaz visual con sensores y ruedas.
* Detección de contacto entre sensores y pista.
* Dibujo del rastro generado por el vehículo.

### Archivo fuente

* `seguidor_linea_pid.py`

### Ejecución

```bash
python seguidor_linea_pid.py
```

---

## 2. Videojuego SpaceMax Defender en Pygame

### Descripción

Este ejercicio consiste en un videojuego estilo "Space Invaders" desarrollado con `pygame`. El jugador controla una nave que debe enfrentar oleadas de enemigos, usar un escudo defensivo, recolectar power-ups y enfrentar un jefe final.

### Características técnicas

* Sistema de niveles progresivos.
* Enemigos con patrones de movimiento y disparo.
* Activación y gestión de escudo temporal.
* Recolección de power-ups.
* Barra de vida del jefe y visualización de HUD.

### Archivos involucrados

* `spacemax_defender.py`: código principal.
* Carpeta `images/` con los sprites:

  * `Tung.png`
  * `BrrrPara-removebg-preview.png`
  * `Bombardilo.png`

### Ejecución

```bash
python spacemax_defender.py
```

> Asegúrate de tener la carpeta `images/` junto al script.

---

## 3. Simulación básica ROS con talker-listener y turtlesim

### Descripción

Este ejercicio muestra cómo se comunican los nodos en ROS mediante la arquitectura publisher-subscriber. Se ejecutan dentro de un contenedor Docker para garantizar el aislamiento del entorno y se incluye la visualización con `turtlesim`.

### Objetivos

* Comprobar la ejecución de nodos ROS.
* Validar la comunicación entre talker y listener.
* Controlar una tortuga desde teclado con `turtlesim`.

### Comandos por consola

**1. Acceso al contenedor:**

```bash
docker exec -it ros_noetic_exercise /bin/bash
source /opt/ros/noetic/setup.bash
```

**2. Ejecutar nodos:**

```bash
rosrun rospy_tutorials talker
rosrun rospy_tutorials listener
```

**3. Ejecutar turtlesim:**

```bash
rosrun turtlesim turtlesim_node
rosrun turtlesim turtle_teleop_key
```

### Resultado esperado

* `talker` publica en `/chatter`.
* `listener` recibe los mensajes.
* La tortuga responde a las teclas.

---

## 4. Instrucciones generales de instalación

### Requisitos

* Python 3.8 o superior
* Docker instalado y en ejecución
* ROS Noetic (en el contenedor Docker)
* Pygame: `pip install pygame`
* Tkinter: incluido por defecto en la mayoría de entornos Python

---

## 5. Créditos y licencia

Desarrollado como parte de una tarea académica de sexto semestre de Ingeniería en Telecomunicaciones. Este documento incluye instrucciones claras para la ejecución y validación de cada componente.

Licencia: **MIT License**. Uso permitido para fines educativos y académicos.
