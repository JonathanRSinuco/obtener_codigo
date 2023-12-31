from flask import Flask, jsonify, request
from http import HTTPStatus
from io import BytesIO
from ruedata_module import RDModule
from waitress import serve

app = Flask(__name__)


@app.errorhandler(HTTPStatus.NOT_IMPLEMENTED)
def not_implemented_error(error):
    return_data = {"message": "Metodo no implementado"}
    return jsonify(return_data), HTTPStatus.NOT_IMPLEMENTED


@app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def not_implemented_error(error):
    return_data = {"message": "Metodo no implementado"}
    return jsonify(return_data), HTTPStatus.METHOD_NOT_ALLOWED


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
        return "Tipo de archivo no válido", HTTPStatus.BAD_REQUEST

    # Lee el contenido del archivo desde la solicitud
    file_data = request.data

    # Crea un objeto BytesIO y carga los datos binarios
    file_stream = BytesIO(file_data)

    # Lee el contenido de texto del objeto BytesIO
    text_content = file_stream.read().decode("utf-8")

    rd_module = RDModule()

    try:
        rd_module.load_access_codes(text_content)
    except ValueError as e:
        return_data = {"error": str(e)}
        return jsonify(return_data), HTTPStatus.BAD_REQUEST

    try:
        code = rd_module.find_code()
    except ValueError as e:
        return_data = {"error": str(e)}
        return jsonify(return_data), HTTPStatus.BAD_REQUEST

    return_data = {"code": code}
    if not code:
        return_data.update(error="No fue posible obtener codigo secreto")

    return jsonify(return_data), HTTPStatus.OK


if __name__ == "__main__":
    PORT = 5000
    print(f"Iniciando servicio en puerto {PORT}")
    serve(app, host="0.0.0.0", port=PORT)
