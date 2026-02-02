FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:stable-alpine
# Copy built files from the first stage
COPY --from=build /app/dist /usr/share/nginx/html
# If you use React Router, you'll need a custom nginx config here
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]