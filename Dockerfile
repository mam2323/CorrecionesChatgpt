# Usa una imagen oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código del proyecto
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando por defecto para iniciar Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "miPrimerProyecto.asgi:application"]
