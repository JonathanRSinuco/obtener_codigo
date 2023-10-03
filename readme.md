# INSTALACIÓN

Asegurate de tener python instalado en el sistema.

## Creación de entorno virtual (Opcional)
Se recomienda crear un entorno virtual para evitar conflictos. Puedes crear un entorno virtual usando *venv*:

`python -m venv myenv`  

### En Linux
`source myenv/bin/activate`  

### En Windows: 
`myenv\Scripts\activate`


### Instalación de dependencias

los requerimientos del servicio estan listados en el archivo req.txt, para instalar todas las dependencias abra una terminal y escriba el siguiente comando:

`pip install -r req.txt`

## Ejecución

Una vez se instalen las dependencias, se puede ejecutar el servicio escribiendo:

`python ruedata_api.py`

La aplicacion se iniciara en el puerto 5000 por defecto


# Funcionamiento

## Descripción
Este endpoint permite cargar un archivo de texto con extension .txt, procesarlo para encontrar un código secreto y devuelve un JSON con el código encontrado.

## Ruta del Endpoint 

`PUT /api/upload/<filename.txt>`

## Parametros de la Solicitud

filename (str): El nombre del archivo de texto que se va a procesar.

## Respuesta de la Solicitud

### Respuesta Exitosa
* Código de estado: 200 OK
* Cuerpo de la respuesta
```
    {
        "code": <int: Codigo secreto>
    }
```

### Errores Posibles
* Código de estado: 400 Bad Request
    * Si la solicitud esta incompleta
    * Si el archivo contiene codigos de acceso incorrectos
* Cuerpo de la respuesta
```
    {
        "error": <str: Descripción del error>
    }
```

### Prueba
para realizar una prueba usando cURL
```
curl --location --request PUT 'http://URL/api/upload/test.txt' \
--header 'Content-Type: text/plain' \
--data '@/C:/path_del archivo/test.txt'   
```
