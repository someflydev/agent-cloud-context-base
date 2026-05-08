FROM node:22-alpine
WORKDIR /app
COPY src/worker/package.json src/worker/worker.js ./
RUN npm install --omit=dev
CMD ["node", "worker.js"]
