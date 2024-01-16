# Use an official Node.js runtime as a base image
FROM node:21-alpine

VOLUME /usr/src/app
# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install
# Copy the rest of the application code to the working directory
COPY . .

# Expose the port on which your Svelte app will run
EXPOSE 8082

# Start the application with hot reload
CMD ["npm", "run", "dev","--","--host", "0.0.0.0"]
