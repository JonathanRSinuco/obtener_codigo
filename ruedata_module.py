class RDModule:
    """
    Clase que representa un módulo para cargar códigos de acceso y encontrar un código secreto.

    Esta clase permite cargar códigos de acceso y determinar un código secreto basado en
    las restricciones de dígitos presentes en los códigos de acceso.

    Attributes:
        __constraints (dict): Un diccionario de restricciones que mapea cada dígito a los dígitos que deben precederlo en un código válido.

    Methods:
        __init__(): Constructor de la clase.
        load_access_codes(access_codes, tamanio_muestra=None): Carga códigos de acceso en el módulo.
        find_code(): Encuentra y devuelve el código secreto basado en las restricciones.
    """

    def __init__(self) -> None:
        """
        Constructor de la clase RDModule.

        Inicializa el diccionario de restricciones como un diccionario vacío.

        """
        self.__constraints = {}  # Diccionario de restricciones

    # Funcion para cargar codigos de acceso
    def load_access_codes(self, access_codes, tamanio_muestra=None) -> None:
        """
        Carga códigos de acceso en el módulo.

        Args:
            access_codes (str/list): Una cadena de texto o lista de códigos de acceso.
            tamanio_muestra (int, optional): El tamaño de la muestra, opcional.

        Returns:
            None

        """
        if isinstance(access_codes, str):
            # Se crea una lista desde la cadena de texto
            access_codes = [line for line in access_codes.split("\n") if line.strip()]

        if tamanio_muestra:
            access_codes = access_codes[:tamanio_muestra]

        for line in access_codes:
            code = line.strip()
            for i in range(len(code)):
                digit = code[i]
                if digit not in self.__constraints:
                    self.__constraints[
                        digit
                    ] = (
                        set()
                    )  # Creamos un conjunto para almacenar los dígitos que deben preceder a este dígito
                for j in range(i + 1, len(code)):
                    self.__constraints[digit].add(code[j])

    # Función para encontrar el código secreto
    def find_code(self) -> str:
        """
        Encuentra y devuelve el código secreto basado en las restricciones.

        Returns:
            str: El código secreto encontrado.

        Raises:
            ValueError: Si no se puede determinar un código secreto válido.

        """
        code = ""
        constraints = self.__constraints.copy()  # Copiamos diccionario original
        print(constraints)
        while constraints:
            # Buscamos un dígito que no tenga restricciones pendientes
            no_constraints_digits = [
                digit for digit in constraints if not constraints[digit]
            ]
            if not no_constraints_digits:
                raise ValueError("No se puede determinar un código secreto válido.")

            # Tomamos el dígito disponible y lo agregamos al código
            digit = no_constraints_digits[0]
            code += digit

            # Eliminamos este dígito de las restricciones pendientes
            del constraints[digit]

            # Eliminamos este dígito de las restricciones de otros dígitos
            for other_digit in constraints:
                constraints[other_digit] -= set(digit)

        # Invertimos el codigo
        code = code[::-1]
        return code
