FROM node:22-alpine
WORKDIR /app
COPY src/job/package.json src/job/job.js ./
RUN npm install --omit=dev
CMD ["node", "job.js"]
