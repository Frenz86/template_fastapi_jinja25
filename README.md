# 🚀 FastAPI CRUD con Docker & Caddy

Un'applicazione CRUD completa costruita con FastAPI, PostgreSQL, Redis, pgAdmin e Caddy come reverse proxy, tutto orchestrato con Docker Compose.

## 📋 Caratteristiche

- ✅ **FastAPI** - Framework web moderno e veloce
- ✅ **Jinja2 Templates** - Frontend con template HTML dinamici
- ✅ **PostgreSQL** - Database relazionale robusto
- ✅ **Redis** - Cache in-memory per performance ottimali
- ✅ **pgAdmin** - Interfaccia web per gestione database
- ✅ **Caddy** - Reverse proxy con HTTPS automatico
- ✅ **Docker Compose** - Orchestrazione dei servizi
- ✅ **Bootstrap 5** - UI responsiva e moderna
- ✅ **SQLAlchemy** - ORM per Python
- ✅ **Pydantic** - Validazione dati

## 🏗️ Struttura del Progetto

```
fastapi-crud-project/
├── 📁 app/                     # Codice dell'applicazione
│   ├── main.py                 # Entry point FastAPI
│   ├── database.py             # Configurazione database
│   ├── models.py               # Modelli SQLAlchemy
│   ├── schemas.py              # Schemi Pydantic
│   └── crud.py                 # Operazioni CRUD
├── 📁 templates/               # Template Jinja2
│   ├── base.html               # Template base
│   ├── index.html              # Lista utenti
│   ├── create_user.html        # Creazione utente
│   └── edit_user.html          # Modifica utente
├── 📁 static/                  # File statici (CSS, JS, immagini)
├── 📄 docker-compose.yml       # Configurazione Docker Compose
├── 📄 Dockerfile               # Immagine Docker per FastAPI
├── 📄 Caddyfile                # Configurazione Caddy
├── 📄 requirements.txt         # Dipendenze Python
├── 📄 .env                     # Variabili d'ambiente
├── 📄 Makefile                 # Comandi utili
└── 📄 README.md                # Documentazione
```

## 🚀 Quick Start

### 1. Clona il progetto
```bash
git clone <repository-url>
cd fastapi-crud-project
```

### 2. Configura le variabili d'ambiente

commentare nel file database.py #DATABASE_URL = os.getenv('DATABASE_URL', default='sqlite:///./fastapi_app.db')
e decommentare quella di POSTGRESQL

```bash
cp .env.example .env
# Modifica il file .env con le tue configurazioni
```

### 3. Avvia i servizi
```bash
# Con Docker Compose
docker-compose up -d

# Oppure con Make
make up
```

### 4. Accedi ai servizi

| Servizio | URL | Credenziali |
|----------|-----|-------------|
| 🌐 **App FastAPI** | http://localhost:8000 | - |
| 📚 **API Docs** | http://localhost:8000/docs | - |
| 🗄️ **pgAdmin** | http://localhost:5050 | admin@example.com / admin123 |
| 🌍 **Caddy (Prod)** | http://localhost | - |

## 🔧 Comandi Utili

Il progetto include un `Makefile` con comandi utili:

```bash
# Aiuto
make help

# Gestione servizi
make up              # Avvia tutti i servizi
make down            # Ferma tutti i servizi
make restart         # Riavvia tutti i servizi
make logs            # Mostra i log

# Database
make db-shell        # Accede al database PostgreSQL
make db-backup       # Crea backup del database
make db-reset        # Reset completo (ATTENZIONE!)

# Sviluppo
make shell           # Shell del container FastAPI
make test            # Esegue i test
make clean           # Pulizia completa

# Monitoraggio
make status          # Stato dei container
make urls            # Mostra tutti gli URL
```

## 📊 API Endpoints

### Web Interface (HTML)
- `GET /` - Lista utenti
- `GET /users/create` - Form creazione utente
- `POST /users/create` - Crea nuovo utente
- `GET /users/{id}/edit` - Form modifica utente
- `POST /users/{id}/edit` - Aggiorna utente
- `POST /users/{id}/delete` - Elimina utente

### REST API (JSON)
- `GET /api/users` - Lista utenti (JSON)
- `POST /api/users` - Crea utente (JSON)
- `GET /api/users/{id}` - Dettaglio utente (JSON)
- `GET /docs` - Documentazione Swagger
- `GET /redoc` - Documentazione ReDoc

## 🔒 Configurazione Database

### Connessione a PostgreSQL
```bash
# Via pgAdmin (Web UI)
Server: postgres
Port: 5432
Database: fastapi_db
Username: postgres
Password: password123

# Via command line
make db-shell
# oppure
docker-compose exec postgres psql -U postgres -d fastapi_db
```

### Schema Database
```sql
-- Tabella users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## 🐳 Configurazione Docker

### Servizi inclusi:

1. **FastAPI App** (`fastapi:8000`)
   - Python 3.11
   - Auto-reload in sviluppo
   - Mount dei volumi per sviluppo

2. **PostgreSQL** (`postgres:5432`)
   - PostgreSQL 15 Alpine
   - Volume persistente
   - Inizializzazione automatica

3. **Redis** (`redis:6379`)
   - Redis 7 Alpine
   - Persistenza dati

4. **pgAdmin** (`pgadmin:5050`)
   - Interfaccia web per PostgreSQL
   - Configurazione automatica

5. **Caddy** (`caddy:80/443`)
   - Reverse proxy
   - HTTPS automatico
   - Compressione gzip
   - Servizio file statici

## 🔧 Personalizzazione

### Modificare la configurazione Caddy
Edita il file `Caddyfile` per:
- Aggiungere il tuo dominio
- Configurare HTTPS con Let's Encrypt
- Aggiungere middleware personalizzati

### Estendere il modello User
1. Modifica `app/models.py`
2. Aggiorna `app/schemas.py`
3. Crea migration con Alembic
4. Aggiorna i template HTML

### Aggiungere nuove funzionalità
- Autenticazione utenti
- Upload file
- API rate limiting
- Logging avanzato
- Monitoraggio con Prometheus

## 🚀 Deploy in Produzione

### 1. Configurazione dominio
```bash
# Modifica Caddyfile
your-domain.com {
    reverse_proxy fastapi:8000
    tls your-email@domain.com
}
```

### 2. Variabili d'ambiente produzione
```bash
ENVIRONMENT=production
DEBUG=False
POSTGRES_PASSWORD=secure-password
SECRET_KEY=your-super-secret-key
```

### 3. Deploy
```bash
make prod-up
```

## 🔍 Troubleshooting

### Container non si avvia
```bash
# Verifica stato
make status

# Controlla i log
make logs

# Rebuild se necessario
make build
```

### Problemi database
```bash
# Reset completo database
make db-reset

# Backup prima del reset
make db-backup
```

### Performance
- Redis è configurato per caching
- Caddy comprime automaticamente i file
- PostgreSQL ottimizzato per sviluppo

## 📝 TODO

- [ ] Autenticazione JWT
- [ ] Test automatizzati
- [ ] Migration database con Alembic
- [ ] API rate limiting
- [ ] Logging strutturato
- [ ] Monitoring con Prometheus
- [ ] CI/CD pipeline

## 🤝 Contribuire

1. Fork del progetto
2. Crea feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 🙏 Riconoscimenti

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Caddy](https://caddyserver.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Docker](https://www.docker.com/)

---

⭐ Se questo progetto ti è stato utile, lascia una stella su GitHub!