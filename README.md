SMART BIN 
Integrantes: Cabrera Pozzobon, Prados y Moragues

El proyecto consiste en construir un basurero inteligente que abra su tapa automáticamente 
cuando detecte una persona y mida el nivel de basura acumulada. Su objetivo es facilitar el 
uso del basurero y avisar cuando esté cerca de llenarse.

El sistema utiliza un sensor ultrasónico para detectar cuando una persona se acerca y 
activa un servomotor que abre la tapa. Otro sensor mide el nivel de basura acumulada. 
Según ese nivel, un LED RGB cambia de color: verde cuando está vacío, amarillo cuando 
está a un nivel intermedio y rojo cuando está lleno. La computadora muestra la información 
y permite controlar el funcionamiento.

Arduino Mega 2560 
Sensores ultrasónicos 
Servomotor  
LED RGB 
Protoboard y cables 

Arduino → Python (datos que envía): 
● Distancia detectada por el sensor de proximidad. 
● Nivel de llenado del basurero en porcentaje. 
● Estado de la tapa (abierta o cerrada). 
● Estado del basurero (vacío, intermedio o lleno). 
Python → Arduino (órdenes que envía): 
● Modificar la distancia de detección de personas. 
● Modificar el porcentaje de llenado para activar la alerta. 
● Enviar órdenes para abrir o cerrar la tapa desde la computadora. 

1er paso: enchufar el arduino a la computadora
2do paso: subir el .ino
3er paso: ejecutar el .py

<img width="527" height="455" alt="image" src="https://github.com/user-attachments/assets/e82f0771-3168-4cbd-9671-c51c401089f5" />

no hubo cambios con respecto al antaproyecto
