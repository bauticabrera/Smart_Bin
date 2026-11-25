
#include <Servo.h>

// Sensor 1: Basura (Interior)
const int TRIG_LLENADO = 4;
const int ECHO_LLENADO = 5;

// Sensor 2: Persona (Frente)
const int TRIG_PRESENCIA = 2;
const int ECHO_PRESENCIA = 3;

// Servo Motor (Tapa)
const int PIN_SERVO = 9;

// LED RGB (Pines PWM)
const int PIN_RED   = 6;
const int PIN_GREEN = 10;
const int PIN_BLUE  = 11;

int distanciaDeteccion = 15;
int limiteLlenadoPct = 80;
int alturaTotalTacho = 38;

Servo servoTapa;
bool tapaAbierta = false;

// Control del tiempo de apertura
unsigned long tiempoApertura = 0;
const unsigned long tiempoEspera = 5000;

// Control de envío a Python
unsigned long ultimoEnvio = 0;
const long intervaloEnvio = 1000;


// Función para medir distancia
long medirDistancia(int pinTrig, int pinEcho) {
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);

  long duracion = pulseIn(pinEcho, HIGH, 30000);

  if (duracion == 0) return 999;

  return duracion * 0.034 / 2;
}


// Control del LED RGB
void fijarColorRGB(int r, int g, int b) {
  analogWrite(PIN_RED, r);
  analogWrite(PIN_GREEN, g);
  analogWrite(PIN_BLUE, b);
}


// Abrir tapa
void abrirTapa() {
  servoTapa.write(0);
  tapaAbierta = true;
  tiempoApertura = millis();
}


// Cerrar tapa
void cerrarTapa() {
  servoTapa.write(80);
  tapaAbierta = false;
}


void setup() {
  Serial.begin(9600);

  pinMode(TRIG_LLENADO, OUTPUT);
  pinMode(ECHO_LLENADO, INPUT);

  pinMode(TRIG_PRESENCIA, OUTPUT);
  pinMode(ECHO_PRESENCIA, INPUT);

  pinMode(PIN_RED, OUTPUT);
  pinMode(PIN_GREEN, OUTPUT);
  pinMode(PIN_BLUE, OUTPUT);

  servoTapa.attach(PIN_SERVO);

  cerrarTapa();
}


void loop() {

  // A. LEER COMANDOS DESDE PYTHON
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "ABRIR") {
      abrirTapa();
    }
    else if (comando == "CERRAR") {
      cerrarTapa();
    }
    else if (comando.startsWith("SET:")) {

      String datos = comando.substring(4);
      int comaPos = datos.indexOf(',');

      if (comaPos != -1) {
        distanciaDeteccion = datos.substring(0, comaPos).toInt();
        limiteLlenadoPct = datos.substring(comaPos + 1).toInt();
      }
    }
  }


  // B. AUTODETECCIÓN DE PRESENCIA
  long distPresencia = medirDistancia(
    TRIG_PRESENCIA,
    ECHO_PRESENCIA
  );

  // Si detecta una persona
  if (distPresencia > 0 &&
      distPresencia <= distanciaDeteccion) {

    // Abrir si está cerrada
    if (!tapaAbierta) {
      abrirTapa();
    }

    // Reiniciar los 5 segundos cada vez que detecta
    tiempoApertura = millis();
  }

  // Cerrar si pasaron 5 segundos sin detectar a nadie
  if (tapaAbierta &&
      millis() - tiempoApertura >= tiempoEspera) {

    cerrarTapa();
  }


  // C. CÁLCULO DE NIVEL Y ENVÍO A PYTHON
  if (millis() - ultimoEnvio >= intervaloEnvio) {

    ultimoEnvio = millis();

    // Medir nivel de basura
    long distLlenado = medirDistancia(
      TRIG_LLENADO,
      ECHO_LLENADO
    );

    // Calcular porcentaje de llenado
    int porcentaje = map(
      distLlenado,
      alturaTotalTacho,
      5,
      0,
      100
    );

    porcentaje = constrain(porcentaje, 0, 100);

    // Determinar estado y color
    String estado = "";
    String colorNombre = "";

    if (porcentaje >= limiteLlenadoPct) {

      estado = "Nivel lleno";
      colorNombre = "red";

      fijarColorRGB(255, 0, 0);
    }
    else if (porcentaje >= 30) {

      estado = "Nivel medio";
      colorNombre = "yellow";

      fijarColorRGB(255, 200, 0);
    }
    else {

      estado = "Nivel bajo";
      colorNombre = "green";

      fijarColorRGB(0, 255, 0);
    }

    // Enviar datos a Python
    Serial.print(porcentaje);
    Serial.print(",");
    Serial.print(estado);
    Serial.print(",");
    Serial.println(colorNombre);
  }
}
