# Seguimiento del aprendizaje — DAW / Python / Backend

## Objetivo

Aprender Python de forma sólida y orientada a la empleabilidad, aprovechando la base de DAW y orientándolo hacia Backend/Python Junior.

Prioridades:

1. Comprender Python.
2. Practicar mucho.
3. Construir proyectos reales.
4. Crear un buen portfolio en GitHub.
5. Aprender tecnologías habituales de backend.
6. Obtener certificaciones como complemento.

---

# Ruta de aprendizaje

1. Python Essentials 1 — Cisco
2. Evaluación práctica
3. Python Essentials 2
4. PCEP / práctica
5. FastAPI
6. PostgreSQL/MySQL y SQL
7. SQLAlchemy
8. Alembic
9. Docker
10. pytest
11. GitHub Actions
12. Proyecto profesional
13. Portfolio y entrevistas

---

# Python

## Python Essentials 1

- Completado el 12/08/2026.
- Evaluación práctica: **49/50**.

## Python Essentials 2

- Completado el 14/09/2026.
- Contenidos: módulos, paquetes, PIP, cadenas, listas, funciones, excepciones, archivos, POO, clases, métodos y herencia.
- Se reforzó especialmente el razonamiento algorítmico y los LABs difíciles.

## LABs trabajados

- Palíndromos.
- Anagramas.
- El Dígito de la Vida.
- ¡Encuentra una palabra!
- Sudoku.
- Histograma de frecuencia.
- Histograma ordenado.
- Evaluando resultados.
- `datetime` / `time`.
- `calendar`.

---

# AWS Cloud

Curso de Commit Academy completado el 21/09/2026.

- Duración: 3 días.
- Certificado obtenido.

---

# FastAPI

Inicio: 21/09/2026.

Conceptos trabajados:

- `FastAPI()`
- rutas/endpoints
- `GET`, `POST`, `PUT`, `DELETE`
- parámetros de ruta y query
- JSON
- `/docs`
- Pydantic
- validación
- `HTTPException`
- códigos HTTP 201 y 404
- `APIRouter`
- `app.include_router()`

## Organización actual

```text
mi_api/
├── app/
│   ├── main.py
│   ├── mini_crud.py
│   ├── retos.py
│   ├── models.py
│   └── database.py
│
├── scripts/
│   └── crear_tablas.py
│
└── ...
```

### `main.py`

Actualmente crea la aplicación FastAPI e incorpora los routers de CRUD y retos:

```python
app.include_router(retos_router)
app.include_router(crud_router)
```

La aplicación dispone del endpoint inicial:

```text
GET /
```

y los routers de `mini_crud.py` y `retos.py`.

---

# Base de datos actual

## PostgreSQL

La base de datos actual del proyecto es:

```text
mi_api
```

Con PostgreSQL ejecutándose en:

```text
localhost:5432
```

La conexión actual utiliza:

```text
postgresql+psycopg
```

`database.py` contiene actualmente el `engine` conectado a PostgreSQL. fileciteturn23file0L1-L5

```python
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/mi_api"

engine = create_engine(DATABASE_URL)
```

> Las referencias antiguas a SQLite de este documento corresponden a una etapa anterior del aprendizaje. El proyecto actual trabaja con PostgreSQL.

---

# SQL

## Conceptos aprendidos

- `CREATE TABLE`
- `DROP TABLE`
- `INSERT INTO`
- `SELECT`
- `WHERE`
- `AND`
- `OR`
- `ORDER BY`
- `ASC` / `DESC`
- `LIMIT`
- `OFFSET`
- `UPDATE`
- `SET`
- `DELETE FROM`
- `COUNT()`
- `AVG()`
- `MAX()`
- `MIN()`
- `SUM()`
- `GROUP BY`
- `HAVING`
- `JOIN` / `INNER JOIN`
- `LEFT JOIN`
- `RIGHT JOIN`
- `COALESCE()`

## JOIN

Se entendió la relación:

```sql
ON usuarios.id = pedidos.usuario_id
```

Conceptos:

- `INNER JOIN`: devuelve coincidencias.
- `LEFT JOIN`: conserva todos los registros de la tabla izquierda.
- `RIGHT JOIN`: conserva todos los registros de la tabla derecha.

También se practicaron agregaciones junto con JOIN:

- dinero gastado por usuario
- número de pedidos por usuario
- dinero gastado por ciudad
- usuarios sin pedidos
- pedidos sin usuario

---

# FastAPI + SQLAlchemy

Se realizó la migración del CRUD desde consultas SQL directas hacia SQLAlchemy ORM.

## Conceptos consolidados

- `create_engine()`
- modelos SQLAlchemy
- `DeclarativeBase`
- `Mapped`
- `mapped_column`
- `primary_key`
- `ForeignKey`
- `Session(engine)`
- `session.query()`
- `filter()`
- `.first()`
- `.all()`
- `session.add()`
- `session.commit()`
- `session.refresh()`
- `session.delete()`
- `func.count()`
- `func.avg()`
- `func.max()`
- `func.min()`
- `group_by()`
- `having()`
- `order_by()`
- `.desc()`
- `limit()`
- `offset()`
- `join()`

## CRUD actual

`mini_crud.py` mantiene el CRUD de usuarios:

- `GET /usuarios`
- `GET /usuarios/{usuario_id}`
- `POST /usuarios`
- `PUT /usuarios/{usuario_id}`
- `DELETE /usuarios/{usuario_id}`

El router se incorpora desde `main.py`. fileciteturn23file1L27-L38

---

# Retos SQLAlchemy 1–13

Todos los retos 1–13 fueron realizados y comprobados mediante Swagger.

1. Buscar usuarios por ciudad.
2. Buscar usuarios mayores de una edad.
3. Buscar usuarios por ciudad y edad.
4. Obtener estadísticas de una ciudad.
5. Obtener resumen agrupado por ciudad.
6. Ordenar usuarios por edad.
7. Buscar usuarios de dos ciudades mediante `or_()`.
8. Buscar usuarios por nombre parcial mediante `like()`.
9. Buscar usuarios mediante doble condición.
10. Paginación con `limit()` y `offset()`.
11. Combinar filtros, ordenación y paginación.
12. Buscar usuarios dentro de un rango de edad.
13. `GROUP BY + HAVING`.

Ejemplo de consulta compuesta:

```python
usuarios = session.query(Usuario).filter(
    Usuario.ciudad == ciudad,
    Usuario.edad > edad
).order_by(
    Usuario.edad.desc()
).limit(limite).offset(offset).all()
```

---

# Relaciones entre tablas — Reto 14

## Modelo `Pedido`

Se creó una segunda tabla relacionada con `Usuario`.

El modelo actual de `models.py` contiene:

```python
class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    producto: Mapped[str] = mapped_column(String(100))

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id")
    )
```

El modelo `Usuario` mantiene:

```python
class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    edad: Mapped[int] = mapped_column(Integer)
    ciudad: Mapped[str] = mapped_column(String(50))
```

Por tanto:

```text
usuarios
---------
id  ←──────────────┐
nombre             │
edad               │
ciudad             │
                   │
                   │ ForeignKey
                   │
pedidos            │
---------
id                 │
producto           │
usuario_id ────────┘
```

`usuario_id` apunta a `usuarios.id`. fileciteturn23file3L17-L39

## Creación de tablas

Durante la etapa inicial se utilizó `Base.metadata.create_all(engine)` mediante `scripts/crear_tablas.py` para crear las tablas.

Ese script ya no forma parte de la estructura actual del proyecto porque la gestión del esquema se realiza mediante **Alembic**.

La tabla `pedidos` fue creada correctamente en PostgreSQL durante la etapa de aprendizaje.

---

# Reto 14 — Crear pedidos

Se creó `PedidoSchema`:

```python
class PedidoSchema(BaseModel):
    producto: str
    usuario_id: int
```

Y el endpoint:

```text
POST /pedidos
```

El endpoint crea un `Pedido`, lo añade a la sesión, hace `commit()`, utiliza `refresh()` para recuperar el ID generado y devuelve los datos del pedido. fileciteturn23file4L13-L15 fileciteturn23file4L439-L466

Se probó correctamente desde Swagger.

Ejemplo real probado:

```json
{
    "producto": "Pilas",
    "usuario_id": 2
}
```

Resultado:

```json
{
    "id": 6,
    "producto": "Pilas",
    "usuario_id": 2
}
```

Esto confirmó que la `ForeignKey` permite asociar el pedido con el usuario correspondiente.

---

# Reto 15 — JOIN entre Usuario y Pedido

Se creó:

```text
GET /pedidos
```

La consulta utilizada:

```python
resultados = session.query(Pedido, Usuario).join(
    Usuario,
    Pedido.usuario_id == Usuario.id
).all()
```

Conceptualmente:

```text
Pedido.usuario_id
       ↓
       ↓
Usuario.id
```

El endpoint devuelve información combinada del pedido y del usuario:

```json
[
    {
        "pedido_id": 6,
        "producto": "Pilas",
        "usuario_id": 2,
        "usuario": "..."
    }
]
```

El Reto 15 fue probado correctamente mediante Swagger. fileciteturn23file4L468-L490

---

# Reto 16 — Pedidos de un usuario concreto

Se creó:

```text
GET /usuarios/{usuario_id}/pedidos
```

La consulta combina:

```python
JOIN
```

para relacionar las tablas:

```python
Usuario.id == Pedido.usuario_id
```

y:

```python
filter()
```

para seleccionar el usuario solicitado:

```python
Usuario.id == usuario_id
```

Consulta actual:

```python
resultados = session.query(Usuario, Pedido).join(
    Pedido,
    Usuario.id == Pedido.usuario_id
).filter(
    Usuario.id == usuario_id
).all()
```

Esto permite consultar, por ejemplo:

```text
GET /usuarios/2/pedidos
```

y obtener únicamente los pedidos asociados al usuario 2.

El Reto 16 fue probado correctamente mediante Swagger. fileciteturn23file4L493-L517

## Concepto clave aprendido

Hay que diferenciar:

```python
Usuario.id == Pedido.usuario_id
```

de:

```python
Usuario.id == usuario_id
```

El primero define **cómo se relacionan las tablas**.

El segundo define **qué usuario queremos consultar**.

---

# Estado actual — 01/10/2026

Ruta completada:

```text
DAW
 ↓
Python Essentials 1
 ↓
Evaluación 49/50
 ↓
Python Essentials 2
 ↓
LABs y consolidación
 ↓
AWS Cloud
 ↓
FastAPI
 ↓
CRUD
 ↓
SQL
 ↓
PostgreSQL
 ↓
SQLAlchemy ORM
 ↓
Retos SQLAlchemy 1–13
 ↓
ForeignKey
 ↓
Tabla Pedido
 ↓
Crear pedidos
 ↓
JOIN
 ↓
Filtrar pedidos por usuario
 ↓
AHORA
```

## Situación técnica actual

- PostgreSQL funcionando.
- FastAPI funcionando.
- Swagger `/docs` funcionando.
- CRUD de usuarios funcionando.
- SQLAlchemy ORM funcionando.
- Modelo `Usuario` funcionando.
- Modelo `Pedido` funcionando.
- Tabla `pedidos` creada en PostgreSQL.
- `ForeignKey("usuarios.id")` funcionando.
- `POST /pedidos` funcionando.
- `GET /pedidos` con JOIN funcionando.
- `GET /usuarios/{usuario_id}/pedidos` funcionando.
- Retos 1–16 completados.

Los archivos actuales enviados para revisar confirman esta estructura y estado:

- `database.py` — conexión PostgreSQL. fileciteturn23file0L1-L5
- `main.py` — aplicación FastAPI y registro de routers. fileciteturn23file1L1-L3 fileciteturn23file1L27-L38
- `mini_crud.py` — CRUD de usuarios con SQLAlchemy. fileciteturn23file2L1-L17
- `models.py` — modelos `Usuario` y `Pedido`. fileciteturn23file3L17-L39
- `retos.py` — retos SQLAlchemy 1–16. fileciteturn23file4L399-L517
- `crear_tablas.py` — creación de tablas mediante `Base.metadata.create_all(engine)`. fileciteturn23file5L1-L7

---

# Camino restante para terminar el proyecto

## Estado tras la sesión del 05/10/2026

Se completó la consolidación de SQLAlchemy y el trabajo de **Alembic/migraciones**.

### Alembic completado

- Alembic configurado e integrado con PostgreSQL.
- Primera revisión/migración inicial creada.
- Base de datos marcada con `stamp head`.
- Migración para añadir `email` a `Usuario`.
- `upgrade head` ejecutado correctamente.
- `downgrade` probado correctamente.
- `upgrade head` vuelto a ejecutar correctamente.
- Se comprobó el estado actual con `alembic current`.
- La base de datos quedó en `4e1fd8048407 (head)`.

### Limpieza realizada

Se revisaron `tests/` y `scripts/`. Se eliminaron los scripts obsoletos de conexión PostgreSQL y creación de tablas. Se mantienen temporalmente las pruebas manuales de SQLAlchemy y `relationship()` hasta la llegada de pytest.

También se corrigió la gestión de `email` en el CRUD y se resolvió el conflicto de la ruta `/usuarios/buscar`, manteniendo como endpoint activo el de consolidación.

## Camino restante

```text
Limpieza y reorganización del proyecto  ← AHORA
 ↓
Docker
 ↓
pytest
 ↓
Tests del CRUD
 ↓
Tests de pedidos y relaciones
 ↓
Tests de errores y casos límite
 ↓
Pulido de la API
 ↓
README profesional
 ↓
GitHub Actions / CI
 ↓
Prueba final sin guía
 ↓
Añadir una pequeña funcionalidad propia
 ↓
Revisión completa
 ↓
mi_api = PRIMER PROYECTO BACKEND TERMINADO
```

### Bloque 9 — Limpieza del proyecto

- Revisar archivos de aprendizaje, scripts y tests.
- Separar claramente aplicación, tests y scripts.
- Revisar nombres y responsabilidades de módulos.
- Eliminar código histórico que ya no pertenezca a la versión final.
- Confirmar que PostgreSQL sea la base de datos de la versión final.
- Revisar configuración y evitar subir credenciales a GitHub.

### Bloque 10 — Docker

- Entender imagen, contenedor y Dockerfile.
- Crear Dockerfile para FastAPI.
- Crear configuración Compose para API + PostgreSQL.
- Utilizar variables de entorno.
- Ejecutar API y PostgreSQL mediante Docker.
- Comprobar el flujo de Alembic con Docker.
- Documentar cómo levantar el proyecto desde cero.

### Bloque 11 — pytest

- Instalar y configurar pytest.
- Practicar `assert` y fixtures.
- Probar endpoints de usuarios.
- Probar creación, modificación y eliminación.
- Probar pedidos y relaciones.
- Probar usuarios inexistentes y errores.
- Probar casos límite.
- Ejecutar toda la suite de forma reproducible.

### Bloque 12 — Pulido profesional

Revisar:
- códigos HTTP.
- validaciones Pydantic.
- `HTTPException`.
- respuestas y errores.
- parámetros obligatorios/opcionales.
- nombres y coherencia de endpoints.
- posibles conflictos entre rutas específicas y dinámicas.
- documentación OpenAPI/Swagger.
- configuración mediante variables de entorno.

### Bloque 13 — README y GitHub

El README final deberá explicar:
- objetivo de la API.
- tecnologías utilizadas.
- estructura del proyecto.
- requisitos.
- instalación.
- configuración de PostgreSQL y variables de entorno.
- ejecución local.
- ejecución con Docker.
- migraciones Alembic.
- ejecución de tests.
- ejemplos de endpoints.
- acceso a Swagger.

Mantener el flujo:
`git status` → `git add` → `git commit` → `git push`

### Bloque 14 — GitHub Actions / CI

Crear un workflow que instale dependencias y ejecute los tests automáticamente para comprobar los cambios enviados al repositorio.

### Bloque 15 — Prueba final

Realizar una prueba práctica sin guía paso a paso sobre:
- SQL.
- SQLAlchemy.
- FastAPI.
- relaciones.
- debugging.
- migraciones.
- tests.
- una pequeña funcionalidad nueva.

### Bloque 16 — Funcionalidad propia y cierre

Añadir una pequeña funcionalidad diseñada por el usuario para demostrar el paso de ejercicios guiados a una necesidad real. Después se hará la revisión final, ejecución de tests, comprobación de Docker, Alembic, README y GitHub.

Cuando estos bloques estén completados, `mi_api` se considerará el **primer proyecto backend completo** del recorrido.

---


## Reto 17 — `relationship()` de SQLAlchemy

El siguiente objetivo es aprender la relación ORM de SQLAlchemy para poder trabajar conceptualmente con:

```python
usuario.pedidos
```

en lugar de construir siempre manualmente el `JOIN`.

Conceptos previstos:

1. `relationship()`
2. relación `Usuario` → `Pedido`
3. relación `Pedido` → `Usuario`
4. `back_populates`
5. consultas utilizando relaciones ORM
6. comparación entre `JOIN` manual y `relationship()`
7. creación de endpoints más limpios

Después:

```text
relationship()
 ↓
relaciones ORM
 ↓
JOINs más limpios
 ↓
Alembic
 ↓
Docker
 ↓
pytest
 ↓
Proyecto backend completo
```

---

# Organización actual del proyecto

```text
mi_api/
├── alembic/
├── app/
│   ├── main.py
│   ├── mini_crud.py
│   ├── reto_consolidacion.py
│   ├── retos.py
│   ├── models.py
│   └── database.py
├── docs/
├── scripts/
│   └── probar_relationship.py   # temporal
├── tests/
│   └── prueba_sqlalchemy.py      # temporal
├── .gitignore
└── alembic.ini
```

### Responsabilidad actual

- `main.py` → crea FastAPI y registra los routers activos.
- `mini_crud.py` → CRUD principal de usuarios.
- `reto_consolidacion.py` → endpoint de consolidación de filtros, ordenación y paginación.
- `retos.py` → material de aprendizaje; no se considera parte de la API final.
- `models.py` → modelos SQLAlchemy.
- `database.py` → conexión `engine` con PostgreSQL.
- `alembic/` → migraciones y control del esquema de PostgreSQL.
- `scripts/probar_relationship.py` → prueba manual temporal.
- `tests/prueba_sqlalchemy.py` → prueba manual temporal que se convertirá en pytest.

---

# Git / GitHub

Repositorio:

```text
aprendiendo-fastapi
```

Flujo habitual:

```text
Modificar código
↓
git status
↓
git add
↓
git commit
↓
git push
```

Se utiliza `.gitignore` para archivos como:

```text
__pycache__/
*.pyc
```

No se añade al seguimiento ningún incidente puntual relacionado con Git que se haya decidido excluir.

---

# Metodología de aprendizaje

1. Estudiar.
2. Entender el concepto.
3. Intentar el código.
4. Recibir pistas cuando sea posible.
5. Corregir errores.
6. Probar en Swagger/PostgreSQL.
7. Consolidar lo aprendido.
8. Aumentar progresivamente la dificultad.
9. Construir proyectos reales.

Cuando se proporciona código, debe llevar comentarios explicando los bloques y comandos relevantes para facilitar el aprendizaje.

---

# Objetivo profesional

**Desarrollador Web / Backend Junior con Python**

Stack previsto:

```text
Python
FastAPI
PostgreSQL
SQL
SQLAlchemy
Alembic
Git/GitHub
Docker
pytest
GitHub Actions
```

Principio:

> Los certificados son complementarios. El objetivo principal es demostrar habilidades mediante proyectos reales, práctica y un GitHub cuidado.
