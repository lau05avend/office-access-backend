
# 🐳 Office Access – Sistema de Registro de Visitantes

Aplicación completa (Frontend + Backend + Base de Datos) para registrar visitantes empresariales y personales.  
Desarrollada con **Flask + MySQL + Nginx**, totalmente containerizada con **Docker Compose**.

---

## 📦 Estructura del Proyecto

```
project/
├── backend/
│   ├── app.py               # Aplicación Flask principal
│   ├── db.py                # Configuración de conexión a MySQL
│   ├── models.py            # Modelos SQLAlchemy
│   ├── routes/
│   │   └── visitantes.py    # Rutas del API REST
│   ├── Dockerfile           # Imagen Docker del backend
│   ├── requirements.txt     # Dependencias Python
│   └── .env.example         # Variables de entorno de ejemplo
│
├── frontend/
│   ├── index.html           # Formulario de registro
│   ├── app.js               # Lógica de envío y validación
│   ├── style.css            # Estilos visuales
│
└── docker-compose.yml       # Orquestador de servicios
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
| CORS | flask-cors |
| Autenticación MySQL | cryptography |

---

## ⚙️ Requisitos Previos

- **Docker** 20.10+  
- **Docker Compose** 2.0+  
- Al menos **2GB RAM** y **5GB de espacio libre**

---

## 🚀 Despliegue Rápido

### 1️⃣ Clonar el repositorio

```bash
git clone <repository-url>
cd project
```

### 2️⃣ (Opcional) Dar permisos a Docker

```bash
sudo chmod 666 /var/run/docker.sock
```

### 3️⃣ Construir e iniciar todos los servicios

```bash
docker compose up -d --build
```

### 4️⃣ Verificar estado

```bash
docker ps
```

Debes ver algo como:

```
visitante-frontend     0.0.0.0:8080->80/tcp
office-access-backend  0.0.0.0:5000->5000/tcp
office-access-mysql    0.0.0.0:3307->3306/tcp
```

---

## 🌐 Acceso a la Aplicación

| Servicio | URL | Descripción |
|-----------|-----|-------------|
| **Frontend** | [http://localhost:8080](http://localhost:8080) | Formulario web para registrar visitantes |
| **Backend API** | [http://localhost:5000/api/visitantes](http://localhost:5000/api/visitantes) | Endpoint principal REST |
| **MySQL** | `localhost:3307` | Base de datos (usuario: `pythonUser`, pass: `python1234`) |

---

## 🧩 Servicios del `docker-compose.yml`

### 🐍 Backend (Flask)

- Imagen: `python:3.10-slim`
- Puerto: `5000`
- Variables:
  ```yaml
  DB_HOST: office-access-mysql
  DB_USER: pythonUser
  DB_PASSWORD: python1234
  DB_NAME: VISIT_REGISTRY_DB
  PORT: 5000
  ```
- Conectado a la red `office-network`
- Reinicio automático: `always`

---

### 🐬 MySQL

- Imagen: `mysql:8.0`
- Puerto externo: `3307`
- Base de datos inicial: `VISIT_REGISTRY_DB`
- Usuario: `pythonUser`
- Password: `python1234`
- Persistencia: volumen `mysql_data`
- Healthcheck: 10 intentos cada 20s

---

### 🖥️ Frontend (Nginx)

- Imagen: `nginx:alpine`
- Puerto: `8080`
- Monta el contenido de `frontend/` en `/usr/share/nginx/html`
- Accede al backend por `http://localhost:5000/api/visitantes`
- Reinicio automático: `unless-stopped`

---

## 🧠 Variables de Entorno

### `.env` (para desarrollo local)

```env
DB_HOST=localhost
DB_USER=pythonUser
DB_PASSWORD=python1234
DB_NAME=VISIT_REGISTRY_DB
PORT=5000
```

### `docker-compose.yml` (para Docker)

```yaml
MYSQL_ROOT_PASSWORD: rootpassword
MYSQL_DATABASE: VISIT_REGISTRY_DB
MYSQL_USER: pythonUser
MYSQL_PASSWORD: python1234
```

---

## 📋 Endpoints Principales

### POST `/api/visitantes`

#### Request Body

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

**✅ Éxito (201 Created)**
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

**⚠️ Error (409 Conflict)**
```json
{
  "error": "Ya existe un visitante registrado con el número de identificación 1234567890",
  "status": "error",
  "status_code": 409
}
```

---

## 🧾 Comandos Útiles

### 🔹 Iniciar Servicios
```bash
docker compose up -d
```

### 🔹 Detener Servicios
```bash
docker compose down
```

### 🔹 Detener + eliminar datos (reinicio total)
```bash
docker compose down -v
```

### 🔹 Reconstruir todo desde cero
```bash
docker compose build --no-cache
docker compose up -d
```

### 🔹 Ver logs
```bash
docker compose logs -f backend
docker compose logs -f mysql
docker compose logs -f frontend
```

---

## 🔍 Verificación y Testing

### 1️⃣ Revisar contenedores activos
```bash
docker ps
```

### 2️⃣ Revisar logs del backend
```bash
docker compose logs backend | grep "Base de datos inicializada"
```

### 3️⃣ Probar API con `curl`
```bash
curl -X POST http://localhost:5000/api/visitantes   -H "Content-Type: application/json"   -d '{
    "numero_identificacion": "1234567890",
    "tipo_identificacion": "CC",
    "nombres": "Test",
    "apellidos": "Docker",
    "tipo_visitante": "Personal"
  }'
```

---

## 🧼 Limpieza y Mantenimiento

### Eliminar contenedores, imágenes y volúmenes
```bash
docker system prune -a --volumes
```

### Backup de la base de datos
```bash
docker exec office-access-mysql mysqldump -u pythonUser -ppython1234 VISIT_REGISTRY_DB > backup.sql
```

### Restaurar backup
```bash
docker exec -i office-access-mysql mysql -u pythonUser -ppython1234 VISIT_REGISTRY_DB < backup.sql
```

---

## 🧠 Tips Pro

- Si MySQL tarda en iniciar, ejecutá:
  ```bash
  docker compose logs -f mysql
  ```
- Si cambia tu código backend, solo reconstruí:
  ```bash
  docker compose up -d --build backend
  ```
- Para entrar al contenedor Flask:
  ```bash
  docker exec -it office-access-backend bash
  ```

---

**Stack:** Flask · MySQL · Docker · Nginx  
**Fecha:** 2025
