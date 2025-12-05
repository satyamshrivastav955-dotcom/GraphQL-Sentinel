FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY dashboard/package*.json ./

# Install dependencies
RUN npm install

# Copy app source
COPY dashboard/ .

# Expose port
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
