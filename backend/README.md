<div align="center">
  <h1 align="center">AVISSA backend</h1>
  <img src="./documents/static/logo.png" alt="Logo" width="80">
</div>

## ¿Qué es AVISSA?
Es una aplicación web salvadoreña de planificación de viajes de transporte público urbano en el área metropolitana, donde cualquier usuario puede seleccionar un origen y un destino en un mapa interactivo de la ciudad y obtener la ruta o rutas a seguir, ofreciendo una solución integral para planificar viajes de manera eficiente y conveniente.

Para el cálculo de ruta se utiliza algoritmos de planificación que devuelvan un resultado óptimo que el usuario ve representado en el mapa, especificando hacia dónde debe dirigirse para abordar cada bus y el momento de descender y dirigirse a su destino.

¿Dónde encuentro el frontend? [Aquí](https://github.com/Avissa-dev/frontend)

![](documents/static/front_example.png)

## Requisitos

Para poder ejecutar el backend se necesita:

- Python 3
- PIP
- PostGIS

## Ejecución

1. Clonar el repositorio
```bash
 git clone https://github.com/Avissa-dev/backend.git
```
2. Navegar a la carpeta del repositorio
```bash
 cd backend
```
3. Instalar las dependencias del proyecto
```console
 pip install Flask

 pip install psycopg

 pip install Flask-Cors

 pip install python-dotenv

 pip install "psycopg[binary]"
```
4. Crear la base de datos en PostgreSQL
```sql
 create datebase NameOfYourDB;
```
5. Restaurar la base de datos que se encuentra dentro de `backend/data`
```console
 pg_restore -d NameOfYourDB elsalvador_avissa.tar -c -U YourDBConnectionUsername
```
Or
``` console
psql -U postgres -d trustbus -f backend/data/elsalvador_avissar/database.sql
```

6. Crear el archivo `.env` y guardar lo siguiente
```html
 DB_HOST=<YourDBConnectionHost>
 DB_PORT=<YourDBConnectionPort>
 DB_NAME=<NameOfYourDB>
 DB_USER=<YourDBConnectionUsername>
 DB_PASSWORD=<YourDBConnectionPassword>
```
7. Ejecutar el proyecto
```bash
 python server.py
```

## Documentación

Puede consultar documentación más detallada en la carpeta [documents](https://github.com/Avissa-dev/backend/tree/main/documents), que incluyen:

- Manual de usuario
- Manual técnico
- Análisis de licencia

## Descargas

Puede descargar la última versión del software desde las [releases ](https://github.com/Avissa-dev/backend/releases) de este repositorio.

## Bugs & Issues

Si desea informar un problema, puede enviarlo al [issue tracker](https://github.com/Avissa-dev/backend/issues) de este repositorio.

## Contribución y desarrollo

¡Las contribuciones son bienvenidas! Hay varias formas de participar en este proyecto, que incluyen:

- Corrección de errores.
- Pruebas beta.
- Enhancement.

Para mayor información sobre cómo contribuir, favor contactar a [00043920@uca.edu.sv](mailto:00043920@uca.edu.sv).

## Licencia

El código contenido en este repositorio y las distribuciones ejecutables tienen licencia bajo los términos de la licencia GPL-3.0, consulte `LICENSE` para obtener más información. Si tiene preguntas sobre el licenciamiento, contáctenos en [00051120@uca.edu.sv](mailto:00051120@uca.edu.sv).