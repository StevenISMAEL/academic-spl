"""
Core Asset — CedulaValidator (CA-01)

Validador reutilizable del número de cédula ecuatoriana.

Este es el ejemplo exacto de lo que un Core Asset debe ser:
- Lógica de negocio del dominio (algoritmo del Registro Civil Ecuador)
- Reutilizable por cualquier feature o producto de la línea
- Sin ninguna referencia a productos específicos
- Testeable de forma independiente, sin necesidad de levantar FastAPI

Algoritmo: Módulo 10 — Coeficientes [2,1,2,1,2,1,2,1,2]
  1. Los primeros 9 dígitos se multiplican por los coeficientes
  2. Si el resultado >= 10, se suma sus dígitos (o equivalente: resultado - 9)
  3. La suma total debe dar un múltiplo de 10 cuando se añade el dígito verificador

Usado por:
  - PersonaRepository.create_persona()     → valida antes de insertar
  - PersonaRepository.update_persona()     → valida si se cambia el documento
  - Cualquier feature futuro que registre personas

Referencia: Registro Civil del Ecuador — algoritmo público.
"""
from __future__ import annotations


class CedulaValidator:
    """Valida números de cédula de identidad ecuatorianos.

    Todos los métodos son estáticos: no necesita instanciarse.
    Se puede usar directamente como Core Asset en cualquier contexto.
    """

    # Provincias válidas (primeros 2 dígitos: 01-24, más 30 para extranjeros)
    _PROVINCIAS_VALIDAS = set(range(1, 25)) | {30}

    # Coeficientes del algoritmo módulo 10 del Registro Civil
    _COEFICIENTES = [2, 1, 2, 1, 2, 1, 2, 1, 2]

    @classmethod
    def validate(cls, cedula: str) -> bool:
        """Verifica si una cédula ecuatoriana es válida.

        Args:
            cedula: Cadena de texto con el número de cédula.
                    Acepta formatos con o sin guiones: "0912345678" o "091-234-5678".

        Returns:
            True si la cédula es válida según el algoritmo del Registro Civil.
            False en cualquier otro caso.

        Ejemplo:
            >>> CedulaValidator.validate("0912345678")
            True
            >>> CedulaValidator.validate("1234567890")
            False
        """
        # Normalizar: eliminar guiones y espacios
        cedula_limpia = cedula.replace("-", "").replace(" ", "")

        # Validaciones estructurales
        if not cedula_limpia.isdigit():
            return False
        if len(cedula_limpia) != 10:
            return False

        # Validar código de provincia (primeros 2 dígitos)
        provincia = int(cedula_limpia[:2])
        if provincia not in cls._PROVINCIAS_VALIDAS:
            return False

        # Validar tercer dígito (debe ser < 6 para personas naturales)
        tercer_digito = int(cedula_limpia[2])
        if tercer_digito >= 6:
            return False

        # Algoritmo módulo 10
        suma = 0
        for i, coef in enumerate(cls._COEFICIENTES):
            producto = int(cedula_limpia[i]) * coef
            if producto >= 10:
                producto -= 9
            suma += producto

        digito_verificador = int(cedula_limpia[9])
        residuo = suma % 10
        digito_esperado = 0 if residuo == 0 else (10 - residuo)

        return digito_verificador == digito_esperado

    @classmethod
    def validate_or_raise(cls, cedula: str) -> str:
        """Valida la cédula y la retorna normalizada (sin guiones).

        Versión conveniente para usar en repositorios: valida y lanza
        ValueError con mensaje claro si la cédula es inválida.

        Args:
            cedula: Número de cédula a validar.

        Returns:
            La cédula normalizada (10 dígitos, sin guiones) si es válida.

        Raises:
            ValueError: Si la cédula no cumple el algoritmo del Registro Civil.
        """
        cedula_limpia = cedula.replace("-", "").replace(" ", "")
        if not cls.validate(cedula_limpia):
            raise ValueError(
                f"El documento '{cedula}' no es una cedula ecuatoriana valida. "
                "Verifique que los 10 digitos sean correctos."
            )
        return cedula_limpia

    @classmethod
    def is_foreign_id(cls, cedula: str) -> bool:
        """Indica si la cédula corresponde a un extranjero (prefijo 30).

        Args:
            cedula: Número de cédula a verificar.

        Returns:
            True si los primeros 2 dígitos son '30' (extranjero residente).
        """
        limpia = cedula.replace("-", "").replace(" ", "")
        if len(limpia) < 2:
            return False
        return limpia[:2] == "30"
