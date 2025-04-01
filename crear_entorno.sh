#!/bin/bash

# Verifica si se pasó una ruta
if [ -z "$1" ]; then
  echo "❌ Por favor indica la ruta donde deseas crear el entorno virtual."
  echo "Uso: ./crear_entorno.sh /ruta/a/mi_proyecto/env"
  exit 1
fi

RUTA_ENV=$1

# Crea el entorno virtual
echo "📦 Creando entorno virtual en: $RUTA_ENV"
python3 -m venv "$RUTA_ENV"

# Verifica si se creó correctamente
if [ $? -eq 0 ]; then
  echo "✅ Entorno virtual creado con éxito."

  echo "💡 Para activarlo, ejecuta:"
  echo "source \"$RUTA_ENV/bin/activate\""
else
  echo "❌ Hubo un error al crear el entorno virtual."
fi
