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
  
- Para manejar la asincronia en los comentarios se usó el framework htmx https://htmx.org/ por su simplicidad
- El flujo es que cuando se sube un comentario, se postea el form a la ruta especificada, si el contenido es valido el backend realiza un trigger que actualiza la tabla de comentarios sin recargar la pagina. Si el form es invalido el bakcend retorna un html con los errores del form, el cual se reemplaza en el div de errores ubicado en _form_comentarios.html.
- !IMPORTANTE La validación de w3c falla para la sintaxis de htmx, sin embargo al probar la ruta el resto de elementos está bien definido.
- Entradas maliciosas son manejadas aprovechando los frameworks usados: (SQL Injection lo maneja SQLalchemy nativamente), (template injection se maneja usando los metodos adecuados de jinja2), (con el setup actual de htmx no hay inyecciones, ya que los swap solo reemplazan datos del servidor y los datos ingresados por el usuario siempre se renderizan con jinja2)