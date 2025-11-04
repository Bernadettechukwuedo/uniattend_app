# ---- Build stage ----
FROM node:18-alpine AS build

# 👇 Declare the argument so Render can inject it
ARG VITE_API_BASE_URL

# 👇 Make it available as an environment variable inside the container
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# 👇 Debug line — make sure this prints your actual backend URL during Render build
RUN echo "Building frontend with VITE_API_BASE_URL=$VITE_API_BASE_URL"

RUN npm run build
