FROM node:22-alpine
WORKDIR /app
COPY src/api/package.json src/api/server.js ./
RUN npm install --omit=dev
EXPOSE 8080
CMD ["node", "server.js"]
