FROM node:22-alpine
WORKDIR /app
COPY services/api/package.json ./package.json
COPY services/api/src ./src
COPY catalog ./catalog
ENV NODE_ENV=production PORT=3001
EXPOSE 3001
USER node
CMD ["node", "src/server.js"]
