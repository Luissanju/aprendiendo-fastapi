# Seguimiento del aprendizaje — DAW / Python / Backend

## Objetivo
Aprender Python de forma sólida y orientada a la empleabilidad, aprovechando la base de DAW y orientándolo hacia Backend/Python Junior.

## Ruta
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

## Python

### Python Essentials 1
- Completado el 12/08/2026.
- Evaluación práctica: 49/50.

### Python Essentials 2
- Completado el 14/09/2026.
- Módulos, paquetes, PIP, cadenas, listas, funciones, excepciones, archivos, POO, clases, métodos y herencia.
- Se reforzó especialmente el razonamiento algorítmico y los LABs difíciles.

### LABs trabajados
- Palíndromos: `lower()`, `replace()`, `len()`, slicing y condicionales.
- Anagramas: normalización, `replace()`, `sorted()` y comparación.
- El Dígito de la Vida: `for`, `int()`, acumuladores, `%`, `//`, `while`.
- ¡Encuentra una palabra!: `find()`, posiciones y variables bandera.
- Sudoku: listas/matrices, bucles anidados y validación.
- Histograma: archivos, `open()`, `read()`, `with`, `FileNotFoundError`, diccionarios, `os.getcwd()`.
- Histograma ordenado: `sorted()`, `key`, `reverse=True` y escritura de archivos.
- Evaluando resultados: lectura, `split()`, diccionarios y acumuladores.
- `datetime`/`time`: `strftime()` y directivas de fecha/hora.
- `calendar`: herencia, `monthdays2calendar()`, clases y métodos.

## AWS Cloud
Curso de Commit Academy completado el 21/09/2026. Duración: 3 días.
Certificado: https://www.commitacademy.io/app/verify-certificate/cert_HyohJ7cCcJ

Vídeos utilizados:
- https://www.youtube.com/watch?v=nCVXVgEI1ng
- https://www.youtube.com/watch?v=bmgZZXFJisE&t=3s
- https://www.youtube.com/watch?v=FPxn4taI-6w&t=8892s

## FastAPI

Inicio: 21/09/2026.

Conceptos trabajados:
- instalación y ejecución
- `FastAPI()`
- rutas/endpoints
- GET, POST, PUT, DELETE
- parámetros de ruta y query
- JSON
- `/docs`
- Pydantic
- validación
- `HTTPException`
- códigos 201 y 404

### `main.py`
Archivo inicial para practicar endpoints.

### `mini_crud.py`
CRUD independiente de usuarios, inicialmente con una lista en memoria.

Endpoints:
- `POST /usuarios`
- `GET /usuarios`
- `GET /usuarios/{usuario_id}`
- `PUT /usuarios/{usuario_id}`
- `DELETE /usuarios/{usuario_id}`

Modelo:
```python
class Usuario(BaseModel):
    nombre: str
    edad: int
```

## Git/GitHub
Repositorio: `aprendiendo-fastapi`

Flujo:
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

Se utilizó `.gitignore` para `__pycache__/` y `*.pyc`.

## SQL

Se decidió estudiar SQL antes de conectar FastAPI con una base de datos.

### Conceptos aprendidos
- `CREATE TABLE`
- `DROP TABLE`
- `INSERT INTO`
- `SELECT`
- `WHERE`
- `ORDER BY`
- `ASC` / `DESC`
- `LIMIT`
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

### Datos de práctica actuales

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(50),
    edad INTEGER,
    ciudad VARCHAR(50)
);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY,
    usuario_id INTEGER,
    producto VARCHAR(50),
    precio DECIMAL(10,2)
);
```

Usuarios:
```text
1 | Luis   | 30 | Villena
2 | Ana    | 25 | Elda
3 | Carlos | 28 | Ibi
4 | Laura  | 22 | Villena
5 | Pedro  | 35 | Elda
```

Pedidos:
```text
1 | 1 | Teclado     | 45.00
2 | 1 | Raton       | 25.00
3 | 2 | Monitor     | 200.00
4 | 3 | Auriculares | 60.00
5 | 6 | Webcam      | 80.00
6 | 6 | Microfono   | 120.00
```

Los pedidos con `usuario_id = 6` se dejaron intencionadamente para practicar JOINs sin coincidencia.

### JOIN
Se entendió la relación:
```sql
ON usuarios.id = pedidos.usuario_id
```

`INNER JOIN`: solo coincidencias.

`LEFT JOIN`: conserva todos los registros de la tabla izquierda.

`RIGHT JOIN`: conserva todos los registros de la tabla derecha.

### Agregaciones y JOIN
Se practicó:
- dinero gastado por usuario
- número de pedidos por usuario
- dinero gastado por ciudad
- usuarios sin pedidos
- pedidos sin usuario

Ejemplo importante:
```sql
SELECT usuarios.nombre, COALESCE(SUM(pedidos.precio), 0)
FROM usuarios
LEFT JOIN pedidos
ON usuarios.id = pedidos.usuario_id
GROUP BY usuarios.id, usuarios.nombre;
```

`COALESCE(valor, alternativa)` permite sustituir `NULL` por una alternativa, por ejemplo `0`.

### Última consulta completada
```sql
SELECT usuarios.ciudad, SUM(pedidos.precio)
FROM usuarios
JOIN pedidos
ON usuarios.id = pedidos.usuario_id
GROUP BY usuarios.ciudad;
```

## Estado actual — 22/09/2026

DAW → Python Essentials 1 terminado → 49/50 → Python Essentials 2 terminado → LABs y consolidación de Python → AWS Cloud (3 días) con certificado → FastAPI → mini CRUD funcional → Git/GitHub → SQL básico y JOIN practicados.

## Próximo paso

Mañana continuar con `mini_crud.py` y sustituir progresivamente:

```python
usuarios = []
```

por una base de datos.

Objetivo:
```text
FastAPI
↓
mini_crud.py
↓
Base de datos SQL
↓
INSERT / SELECT / UPDATE / DELETE
```

Después:
```text
PostgreSQL
↓
SQLAlchemy
↓
FastAPI + PostgreSQL
↓
Alembic
↓
Docker
↓
pytest
↓
Proyecto backend completo
```

## Metodología
1. Estudiar.
2. Practicar.
3. Traer código o dudas.
4. Revisar.
5. Entender errores.
6. Intentar LABs desde cero.
7. Revisar soluciones difíciles.
8. Construir proyectos propios.

## Objetivo profesional
**Desarrollador Web / Backend Junior con Python**

Stack previsto:
Python, FastAPI, PostgreSQL/MySQL, SQL, SQLAlchemy, Alembic, Git/GitHub, Docker, pytest y GitHub Actions.

Principio: los certificados son complementarios; el objetivo es demostrar habilidades mediante proyectos reales y un GitHub cuidado.
