FROM node:12 as build-stage
WORKDIR /app
COPY  ./public/package*.json ./
RUN npm install
COPY ./public/ .
RUN cp _config.js config.js
RUN npm run build

FROM debian:bullseye
RUN apt update
RUN apt install -y nodejs \
    npm \
    vim \
    net-tools

WORKDIR /app
COPY . .
RUN npm install package.json
COPY --from=build-stage /app/dist /app/public/dist
CMD node index.js