from flask import Flask, jsonify, request
from io import BytesIO
from ruedata_module import RDModule

app = Flask(__name__)


@app.route("/api/upload/<filename>", methods=["PUT"])
def upload_file(filename):
    """
    Endpoint para determinar el código secreto usando un archivo de códigos de acceso.

    Este endpoint permite cargar un archivo de texto con extension .txt, procesarlo para
    encontrar un código secreto y devuelve un JSON con el código encontrado.

    Args:
        filename (str): El nombre del archivo de texto que se va a procesar.

    Returns:
        dict: Un diccionario JSON con el código secreto encontrado.

    Raises:
        BadRequest (400): Si el archivo no tiene la extensión .txt.

    Example:
        Para cargar un archivo llamado "ejemplo.txt", realiza una solicitud PUT a:
        /api/upload/ejemplo.txt
    """

    # Verifica si el archivo tiene la extensión .txt
    if not filename.endswith(".txt"):
        return "Tipo de archivo no válido", 400

    # Lee el contenido del archivo desde la solicitud
    file_data = request.data

    # Crea un objeto BytesIO y carga los datos binarios
    file_stream = BytesIO(file_data)

    # Lee el contenido de texto del objeto BytesIO
    text_content = file_stream.read().decode("utf-8")

    rd_module = RDModule()
    rd_module.load_access_codes(text_content)
    code = rd_module.find_code()

    return_data = {"code": code}

    return jsonify(return_data), 200


if __name__ == "__main__":
    app.run(debug=True)
