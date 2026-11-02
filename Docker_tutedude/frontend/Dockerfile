# ---------- Express Frontend ----------
FROM node:20-alpine

ENV NODE_ENV=production \
    PORT=3000

WORKDIR /app

# Install dependencies first (better layer caching)
COPY package*.json ./
RUN npm install --omit=dev

# Copy application code
COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
