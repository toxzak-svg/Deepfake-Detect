FROM node:20-alpine
WORKDIR /app
COPY package.json /app/package.json
RUN npm install --production
COPY . /app
EXPOSE 3000
CMD ["npx", "next", "start", "-p", "3000"]
