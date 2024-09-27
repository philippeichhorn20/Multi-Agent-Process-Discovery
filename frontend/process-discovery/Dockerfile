# Use a base Node.js image
FROM node:20.13.1

# Set the working directory inside the container
WORKDIR /app

# Copy the rest of the application code to the container
COPY . .

# Install npm packages
RUN npm install

# Expose the port that the server will listen on
EXPOSE 3000

# Start the Express server
CMD ["npm", "start"]