FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy only the package.json and package-lock.json first to leverage Docker cache
COPY package*.json /app/

# Install dependencies using npm ci for a clean and fast installation
RUN npm ci

# Copy the rest of the application code into the container
COPY . .

# Add a non-root user for security purposes
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Change ownership of the application files to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port your application runs on (e.g., 3000)
EXPOSE 3000

# Start the application
CMD [ "npm", "start" ]