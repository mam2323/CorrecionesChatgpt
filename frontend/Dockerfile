# Usa una imagen oficial de Node.js
FROM node:18-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo package.json e instala dependencias
COPY package*.json ./
RUN npm install

# Copia todo el código
COPY . .

# Expone el puerto 3000
EXPOSE 3000

# Comando por defecto para iniciar React
CMD ["npm", "start"]
