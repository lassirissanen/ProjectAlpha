# Choose Node.js version 17 as the base image
FROM node:17

# Create a directory for the application
WORKDIR /app

# Copy the package list and install dependencies
COPY package*.json ./
RUN npm install

# Copy the application to the directory
COPY . .

# Build the application
RUN npm run build

# Expose the port used to listen to the application
EXPOSE 3000

# Start the application. The backend URL is passed to the frontend using the Docker network instead of using localhost
CMD ["npm", "start", "--", "--backendUrl=http://backend:5000"]