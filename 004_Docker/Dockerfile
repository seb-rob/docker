FROM node:20-alpine

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY . .

RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

CMD [ "npm", "start" ]