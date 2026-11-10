#include <WiFi.h>
#include <WebServer.h>
#include <time.h>

// CONFIGURACOES DO WIFI
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";

// CONFIGURACOES DO SENSOR HC-SR04
#define TRIG_PIN 5
#define ECHO_PIN 18

// CONFIGURACOES GERAIS
WebServer server(80);

float distanciaAtual = 0;
bool leituraValida = false;

unsigned long ultimaLeitura = 0;
const unsigned long INTERVALO_LEITURA = 2000;

// CONFIGURACAO DE DATA E HORA
const long GMT_OFFSET = -3 * 3600;
const int DAYLIGHT_OFFSET = 0;

void configurarHorario() {
  configTime(
    GMT_OFFSET,
    DAYLIGHT_OFFSET,
    "pool.ntp.org",
    "time.nist.gov"
  );
}

String pegarHorario() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo, 1000)) {
    return "indisponivel";
  }
  char horario[20];
  strftime(horario, sizeof(horario), "%H:%M:%S", &timeinfo);
  return String(horario);
}

String pegarData() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo, 1000)) {
    return "indisponivel";
  }
  char data[20];
  strftime(data, sizeof(data), "%Y-%m-%d", &timeinfo);
  return String(data);
}

// CONEXAO WIFI
void conectarWiFi() {
  Serial.println();
  Serial.println("Conectando ao Wi-Fi...");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("Wi-Fi conectado!");
  Serial.print("Endereco IP: ");
  Serial.println(WiFi.localIP());
}

// LEITURA DO SENSOR HC-SR04
float medirDistancia() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracao = pulseIn(ECHO_PIN, HIGH, 30000);

  if (duracao == 0) {
    return -1;
  }
  return duracao * 0.0343 / 2;
}

void atualizarLeitura() {
  float distancia = medirDistancia();
  if (distancia > 0) {
    distanciaAtual = distancia;
    leituraValida = true;
    Serial.print("Distancia: ");
    Serial.print(distanciaAtual);
    Serial.println(" cm");
  } else {
    leituraValida = false;
    Serial.println("Falha na leitura do sensor!");
  }
}

// GERACAO DO JSON
String gerarJsonStatus() {
  String json = "{";
  json += "\"distanciaCm\":" + String(distanciaAtual, 2) + ",";
  json += "\"data\":\"" + pegarData() + "\",";
  json += "\"horario\":\"" + pegarHorario() + "\",";
  json += "\"leituraValida\":";
  json += leituraValida ? "true" : "false";
  json += "}";
  return json;
}

// ROTAS DA API DO ESP32
void configurarRotas() {
  // GET /status
  // Retorna os dados atuais do sensor
  server.on("/status", HTTP_GET, []() {
    String json = gerarJsonStatus();
    server.send(200, "application/json", json);
    Serial.println("Requisicao GET /status recebida!");
  });

  // GET /
  // Informacoes basicas do servidor
  server.on("/", HTTP_GET, []() {
    server.send(
      200,
      "application/json",
      "{\"mensagem\":\"API IoT ESP32 ativa\"}"
    );
  });

  // Rota nao encontrada
  server.onNotFound([]() {
    server.send(
      404,
      "application/json",
      "{\"erro\":\"Rota nao encontrada\"}"
    );
  });
  server.begin();
  Serial.println("API IoT iniciada!");
}

// SETUP
void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);

  conectarWiFi();
  configurarHorario();
  configurarRotas();

  Serial.println("Sistema IoT iniciado!");
}

// LOOP PRINCIPAL
void loop() {
  server.handleClient();
  unsigned long agora = millis();
  if (agora - ultimaLeitura >= INTERVALO_LEITURA) {
    ultimaLeitura = agora;
    atualizarLeitura();
  }
}