# Tarea 1 desarrollo web

# Iniciar proyecto
La tarea fue realizada con el gestor de ambientes uv.  
Makefile define dos comandos:

Para ejecutar el proyecto:
```
make run
```
Para borrar la base de datos y ejecutar los scripts (+ información inicial)
```
make db-reset
```

String de conexión usada:

```
"mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2"  
```
Se puede modificar al comienzo de app.py


*De todas formas se realizó un pip freeze > requirements.txt por si se prefiere otro gestor de ambiente.  

## Detalles para la corrección

### Tarea 2
- sql_scripts incluye populate_users.sql para llenar la tabla de miembros con usuarios predefinidos
- formularios se validan dos veces, una en el frontend y otra en el backend. 
- la tabla de usuarios ordena y filtra todos los datos a la vez, esto por simplicidad y por la baja cantidad de datos, una futura mejora seria usar AJAX o parametros en la ruta para ir a buscar los datos dinamicamente.
- las validaciones principales se realizaron en validators.py
- los modelos de SQLAlchemy se encuentran en models.py
- se usó flashes para mandar mensajes al frontend desde el backend
- base.html es el template base, del cual todos los otros htmls extienden el bloque content.
- fotos se suben a carpeta ./uploads
### Tarea 3
- En templates/estadisticas se encuentran las templates con los graficos pedidos, estos usan highcharts.js
- En app.py se definieron endpoints /api/... para que los graficos obtengan los datos. Cada punto va a buscar a la base de datos los resultados esperados.