FROM node:22-alpine
WORKDIR /app
COPY src/cronjob/package.json src/cronjob/cronjob.js ./
RUN npm install --omit=dev
CMD ["node", "cronjob.js"]
