# PROYECTO BACKEND
## E-commerce ```handmade``` - Tienda de regalos personalizados :gift::package:



<p align="center" style="backgound-color:white; font-size:"45px"> PROYECTO BACKEND HANDMADE M&A </p>
![GitHub Logo](https://cdn-icons-png.flaticon.com/512/4243/4243409.png)


## ***Autores***: 

> :octocat: Marigrace Silva Salas

### IDEA DEL PROYECTO:
Se implementará un ecommerce de producto realizados a mano con la finalidad de facilitar a los clientes con la elección de productos.

### SOLUCIÓN 

* Agilizara el proceso de venta vía web para así poder brindarles seguridad y cumpliendo los protocolos de sanidad al momento de su envió y entrega de productos.
* Implementar un apartado para que el administrador que ejecute labores de control de ventas.

### Contruído con :hammer_and_wrench: :

> Framework: Django <img src="https://img.icons8.com/color/48/000000/django.png" style="width:20px;height:20px;"/>

> Base de datos: Postgres <img src="https://img.icons8.com/color/50/000000/postgreesql.png" style="width:20px;height:20px;"/>

> Tester: Postman <img src="https://img.icons8.com/dusk/64/000000/postman-api.png" style="width:20px;height:20px;"/>

> Editor de código: VSCode <img src="https://img.icons8.com/fluency/48/000000/visual-studio-code-2019.png" style="width:20px;height:20px;"/>
### MODELO ENTIDAD RELACIÓN 
![image text](https://raw.githubusercontent.com/ks161297/proyecto_backend/avance01/E-commerce%20MER.png)

> 
# INSTRUCCIONES PARA EL REPOSITORIO
_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento._

Para una descarga diresta: 
1. Puedes descargar ó usango Git puede clonarlo. 

```
                       git clone https://github.com/ks161297/proyecto_backend.git
```
2. Ya descargado o clonado, se creará la carpeta ```proyecto_backend``` en la rama ```main``` por defecto. Deberá ingresar a la rama ```avance01``` con el siguiente comando. 

``` 
                                                git chechout avance01
```

3. Para empezarlo a utilizar, se deberá instalar el entorno virtual

```
                                              virtualenv <nombre_entorno>
```

4. Asegurese que este corriendo el entorno virtual 

```
                                         source <nombre_entorno>/Scripts/activate
```

4. Una vez creado el entorno virtual, se deben intalar lo requerimiento - librerías para no tener errores

```
                                              pip install -r requirements.txt
```

5. Cree la base de datos `tiendah_django`

6. Eliminar migraciones existentes y crear nuevas con los siguientes comandos

```
                                  python manage.py makemigrations handmade --name <nombre_migracion>
                                  python manage.py makemigrations facturacion --name <nombre_migracion>
```

7. Para que sean visibles las migracions realizadas ejecutar los siguientes comandos.

```
                                                    python manage.py migrate handmade
                                                    python manage.py migrate handmade
```
8. Ejecutamos en el servidor 

```
                                                        python manage.py runserver
```
### PROYECTO_BACKEND :raised_hands:

- [X] Usar una BD (SQL o No SQL) - postgres
- [X] Al menos un CRUD con lógica - clientes, productos
- [X] Manejo de archivos multimedia - Fotos cloudinary
- [X] Rutas protegidas - JWT Login
- [X] Paso de valores 
- [X] Despliegue Heroku
- [X] Documentación de la API - Swagger
- [X] Markdown - indicaciones 
- [X] Test de los controladores - cliente, categoria
- [X] Github actions para Pull Request

