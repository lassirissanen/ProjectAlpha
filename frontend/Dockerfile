# Choose Node.js version 17 as the base image
FROM node:17 as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . ./
ENV REACT_APP_BACKEND_URL=/api
RUN npm run build

# production env
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]