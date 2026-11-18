# Blog API

A RESTful Blog API built with **FastAPI**, **SQLAlchemy** and **PostgreSQL**, featuring **JWT authentication**, Pydantic validation and full CRUD operations.

## Features

- Create, read, update and delete blog posts (CRUD)
- JWT authentication protecting write operations
- PostgreSQL database accessed through the SQLAlchemy ORM
- Request and response validation with Pydantic schemas
- Pagination on the blog list endpoint
- Proper HTTP status codes and error handling (`401` for invalid tokens, `404` for missing blogs)
- Configuration through environment variables (`.env`)
- Interactive API documentation (Swagger UI) at `/docs`

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| Uvicorn | ASGI server |
| SQLAlchemy | ORM (database access) |
| PostgreSQL | Database |
| Pydantic | Data validation and schemas |
| python-jose | JWT creation and verification |
| python-dotenv | Loading environment variables |

## Project Structure

```
blog-api-project/
├── main.py            # FastAPI app and API routes
├── database.py        # Database engine, session and Base
├── models.py          # SQLAlchemy models (database tables)
├── schemas.py         # Pydantic schemas (request/response shapes)
├── auth.py            # JWT token creation and verification
├── requirements.txt   # Python dependencies
├── .env.example       # Example environment variables
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- PostgreSQL installed and running

### 1. Clone the repository

```bash
git clone https://github.com/Annu9111/blog-api-project.git
cd blog-api-project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Open `psql` and run:

```sql
CREATE USER blog_user WITH PASSWORD 'your_password';
CREATE DATABASE blog_db OWNER blog_user;
```

### 5. Configure environment variables

Copy the example file and edit the values:

```bash
cp .env.example .env
```

`.env`:

```
DATABASE_URL=postgresql+psycopg://blog_user:your_password@localhost:5432/blog_db
SECRET_KEY=your-long-random-secret
```

Generate a strong secret key with:

```bash
openssl rand -hex 32
```

> If your password contains special characters such as `@` or `#`, URL-encode them in `DATABASE_URL` (for example `@` becomes `%40`).

### 6. Run the server

```bash
uvicorn main:app --reload
```

The tables are created automatically on startup. Open the interactive docs at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

<!-- Add a screenshot of the Swagger UI: save it as docs/swagger.png and uncomment the next line -->
<!-- ![Swagger UI](docs/swagger.png) -->

## API Endpoints

| Method | Endpoint | Auth required | Description |
|---|---|---|---|
| `GET` | `/` | No | Health check |
| `POST` | `/login` | No | Get a JWT access token |
| `POST` | `/blogs` | Yes | Create a new blog |
| `GET` | `/blogs` | No | List blogs (supports `skip` and `limit`) |
| `GET` | `/blogs/{id}` | No | Get a single blog by id |
| `PUT` | `/blogs/{id}` | Yes | Update a blog |
| `DELETE` | `/blogs/{id}` | Yes | Delete a blog |

### Status codes

| Code | Meaning |
|---|---|
| `200` | Success |
| `201` | Blog created |
| `401` | Missing, invalid or expired token |
| `404` | Blog not found |
| `422` | Validation error (invalid request body or parameters) |

## Example Usage

**1. Get a token**

```bash
curl -X POST http://127.0.0.1:8000/login
```

```json
{
  "access_token": "<your-jwt-token>",
  "token_type": "bearer"
}
```

**2. Create a blog (replace `TOKEN` with your token)**

```bash
curl -X POST http://127.0.0.1:8000/blogs \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My first blog", "content": "Hello from FastAPI and PostgreSQL"}'
```

```json
{
  "id": 1,
  "title": "My first blog",
  "content": "Hello from FastAPI and PostgreSQL"
}
```

**3. List blogs**

```bash
curl "http://127.0.0.1:8000/blogs?skip=0&limit=10"
```

## How Authentication Works

1. The client calls `/login` and receives a signed JWT (JSON Web Token).
2. The client sends the token in the `Authorization: Bearer <token>` header on protected routes.
3. A FastAPI dependency (`verify_token`) checks the token's signature and expiry before the route runs.
4. If the token is invalid or expired, the API returns `401` and the route is never executed.

## Database Model

**Table: `blogs`**

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key, indexed |
| `title` | String | Blog title |
| `content` | Text | Blog body |

## Future Improvements

- User registration with hashed passwords (bcrypt) and a `users` table
- Link each blog to its author so users can only edit their own posts
- Database migrations with Alembic
- Search and filtering by title
- Automated tests with pytest
- Docker setup and deployment

## Author

**Annu Soni**

- GitHub: [@Annu9111](https://github.com/Annu9111)
