
# 🐳 Office Access – Sistema de Registro de Visitantes

Aplicación completa (Frontend + Backend + Base de Datos) para registrar visitantes empresariales y personales.  
Desarrollada con **Flask + MySQL + Nginx**, y automatizada mediante **Docker Compose** y pipelines locales con **Jenkins**.

---

## 🗂️ Arquitectura del Proyecto

- **Frontend (Nginx + HTML/CSS/JS)**: formulario responsive que envía registros vía `fetch` a la API.
- **Backend (Flask + SQLAlchemy)**: expone `/api/visitantes`, valida campos críticos y persiste el modelo `Visitante` (@backend/models.py).
- **Base de datos (MySQL 8)**: almacén relacional con inicialización automática; usa credenciales provistas en `.env` o `docker-compose`.
- **Pipelines locales (Jenkins + ngrok)**: orquestan builds/tests y exponen webhooks vía túneles seguros.

---

## 📦 Estructura del Repositorio

```
office-access-backend/
├── backend/
│   ├── app.py               # Aplicación Flask principal
│   ├── db.py                # Configuración de conexión a MySQL
│   ├── models.py            # Modelos SQLAlchemy
│   ├── routes/
│   │   └── visitantes.py    # Rutas del API REST
├───├── tests/
│   ├── conftest.py          # Fixtures para pruebas
│   │   └── unit/routes/...  # Pruebas unitarias
│   ├── pytest.ini           # Configuración de Pytest
│   ├── requirements.txt     # Dependencias Python
│   ├── Dockerfile           # Imagen Docker del backend
│   ├── coverage.xml         # Reporte de coverage de pruebas
│   ├── .coveragerc          # Configuración de coverage de pruebas
│   └── .env.example         # Variables de entorno de ejemplo
│
├── frontend/
│   ├── index.html           # Formulario de registro
│   ├── app.js               # Lógica de envío y validación
│   ├── style.css            # Estilos visuales
│   
├── jenkins/
│   └── docker-compose.jenkins.yml # Orquestador de pipelines locales
│   └── Dockerfile           # Imagen Docker del Jenkins
├
└── docker-compose.yml       # Orquestador de servicios
└── Jenkinsfile              # Pipeline de Jenkins
```

---

## 🧰 Tecnologías Utilizadas

| Componente | Tecnología |
|-------------|-------------|
| Lenguaje | Python 3.10 |
| Framework | Flask 2.3.0 |
| ORM | Flask-SQLAlchemy 3.0.5 |
| Base de datos | MySQL 8.0 |
| Frontend | HTML, CSS, JS, Nginx |
| Containerización | Docker + Docker Compose |
| Testing | Pytest |
| CI/CD local | Jenkins + ngrok |

---

## ⚙️ Requisitos Previos

- **Docker** 20.10+ y **Docker Compose** 2.0+
- **Python 3.10** si vas a ejecutar el backend sin contenedores
- Al menos **2GB RAM** y **5GB** libres

---

## 🚀 Puesta en Marcha Rápida

1. **Clonar repositorio**
```bash
git clone <repository-url>
cd office-access-backend
```
2. **Configurar variables (solo entorno local)**
```bash
cp backend/.env.example backend/.env
# Ajusta credenciales según tu entorno
```
3. **(Opcional) Dar permisos al socket Docker**
```bash
sudo chmod 666 /var/run/docker.sock
```
4. **Construir e iniciar el stack completo**
```bash
docker compose up -d --build
```
5. **Verificar contenedores**
```bash
docker ps
```
Deberías ver `visitante-frontend`, `office-access-backend` y `office-access-mysql` activos.

---

## 🌐 Accesos Rápidos

| Servicio | URL | Descripción |
|-----------|-----|-------------|
| **Frontend** | [http://localhost:8080](http://localhost:8080) | Formulario web para registrar visitantes |
| **Backend API** | [http://localhost:5000/api/visitantes](http://localhost:5000/api/visitantes) | Endpoint REST documentado en `routes/visitantes.py` |
| **MySQL** | `localhost:3307` | Base de datos (`pythonUser` / `python1234`) |
| **Jenkins (local)** | [http://localhost:8081](http://localhost:8081) | Panel de pipelines locales |

---

## 🧩 Servicios orquestados (`docker-compose.yml`)

### 🐍 Backend (Flask)
- Imagen base `python:3.10-slim` + `backend/Dockerfile`.
- Variables inyectadas: `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `PORT`.
- Inicializa la base al levantar la app (ver `create_app` en @backend/app.py).

### 🐬 MySQL 8.0
- Expone `3307:3306` para evitar conflictos locales.
- Volumen `mysql_data` para persistencia.
- Healthcheck que asegura disponibilidad antes de levantar Flask.

### 🖥️ Frontend (Nginx)
- Imagen `nginx:alpine` sirviendo `frontend/` en modo read-only.
- Consume la API `http://backend:5000/api/visitantes` mediante configuración del JS.

---

## 🧠 Variables de Entorno

### Desarrollo local (`backend/.env`)
```env
DB_HOST=localhost
DB_USER=pythonUser
DB_PASSWORD=python1234
DB_NAME=VISIT_REGISTRY_DB
PORT=5000
```

### Contenedores (definidas en `docker-compose.yml`)
```yaml
MYSQL_ROOT_PASSWORD: rootpassword
MYSQL_DATABASE: VISIT_REGISTRY_DB
MYSQL_USER: pythonUser
MYSQL_PASSWORD: python1234
```

> Nota: Para Docker no es necesario crear `.env`, ya que Compose pasa las variables automáticamente.

---

## 📋 API Principal

### POST `/api/visitantes`
- Valida campos obligatorios (`numero_identificacion`, `tipo_identificacion`, `nombres`, `apellidos`, `tipo_visitante`).
- Verifica que `tipo_visitante` ∈ {`Empresarial`, `Personal`} y que `empresa_representa` exista cuando corresponde.
- Evita duplicados consultando por `numero_identificacion` (@backend/routes/visitantes.py#39-46).

#### Request de ejemplo
```json
{
  "numero_identificacion": "1234567890",
  "tipo_identificacion": "CC",
  "nombres": "Juan",
  "apellidos": "Pérez",
  "tipo_visitante": "Empresarial",
  "empresa_representa": "Tech Solutions S.A."
}
```

#### Respuestas
✅ `201 Created`
```json
{
  "message": "Visitante registrado exitosamente",
  "status": "success",
  "data": {
    "id_visitante": 1,
    "numero_identificacion": "1234567890",
    "tipo_visitante": "Empresarial",
    "fecha_registro": "2025-11-04T14:30:00"
  }
}
```

⚠️ `409 Conflict`
```json
{
  "error": "Ya existe un visitante registrado con el número de identificación 1234567890",
  "status": "error",
  "status_code": 409
}
```


## � Testing automatizado

- Las suites viven en `backend/tests/unit/routes/test_visitantes_routes.py` e incluyen casos de éxito, validaciones, duplicados y manejo de errores (IntegrityError + excepciones inesperadas).
- Ejecutá las pruebas dentro del contenedor backend o localmente:
```bash
cd backend
pytest --cov --cov-report term-missing
```

---

## 🧾 Comandos Útiles

| Acción | Comando |
|--------|---------|
| Iniciar stack | `docker compose up -d` |
| Detener stack | `docker compose down` |
| Reinicio total (eliminar datos) | `docker compose down -v` |
| Reconstruir sin caché | `docker compose build --no-cache && docker compose up -d` |
| Logs en vivo | `docker compose logs -f backend` (cambia `backend` por mysql/frontend) |


## 🤖 CI/CD local con Jenkins + ngrok

### � Levantar Jenkins en Docker
1. Ajustar permisos al socket (solo la primera vez o tras reinicio):
```bash
sudo chmod 666 /var/run/docker.sock
```
2. Ingresar al directorio de Jenkins y levantar el stack dedicado:
```bash
cd jenkins/
docker compose -f docker-compose.jenkins.yml up -d
```
3. Acceder al panel en [http://localhost:8081](http://localhost:8081) o a través del túnel descrito abajo.

### 🌍 Exponer Jenkins con ngrok
```bash
ngrok http 8081
```
Obtendrás una URL pública temporal para recibir webhooks de GitHub/GitLab o supervisar builds fuera de la red local.

### 🧹 Apagar Jenkins y limpiar contenedores auxiliares
```bash
docker compose -f docker-compose.jenkins.yml down
```
Si necesitas limpiar por completo los contenedores del stack principal:
```bash
docker stop visitante-frontend office-access-backend office-access-mysql
docker rm visitante-frontend office-access-backend office-access-mysql
```

---

## 🔍 Verificación manual

1. **Listar contenedores**
```bash
docker ps
```
2. **Ver logs del backend**
```bash
docker compose logs backend | grep "Base de datos inicializada"
```
3. **Probar la API**
```bash
curl -X POST http://localhost:5000/api/visitantes -H "Content-Type: application/json" -d '{
    "numero_identificacion": "1234567890",
    "tipo_identificacion": "CC",
    "nombres": "Test",
    "apellidos": "Docker",
    "tipo_visitante": "Personal"
  }'
```

---

## 🧼 Limpieza y Mantenimiento

- Eliminar contenedores, imágenes y volúmenes huérfanos:
```bash
docker system prune -a --volumes
```
- Backup de la base de datos:
```bash
docker exec office-access-mysql mysqldump -u pythonUser -ppython1234 VISIT_REGISTRY_DB > backup.sql
```
- Restaurar backup:
```bash
docker exec -i office-access-mysql mysql -u pythonUser -ppython1234 VISIT_REGISTRY_DB < backup.sql
```

---

## 🧠 Tips Pro

- Si MySQL tarda en levantar:
  ```bash
  docker compose logs -f office-access-mysql
  ```
- Para reflejar cambios solo en el backend:
  ```bash
  docker compose up -d --build backend
  ```
- Abrir una shell dentro del contenedor Flask:
  ```bash
  docker exec -it office-access-backend bash
  ```

---

**Stack:** Flask · MySQL · Docker · Nginx · Jenkins  
**Fecha:** 2025
