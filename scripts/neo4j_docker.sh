#!/bin/bash

# Script to start Neo4j using Docker
# This is an example script - you may need to adjust based on your Neo4j setup

echo "🚀 Starting Neo4j with Docker..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    echo "Please install Docker to run Neo4j"
    exit 1
fi

# Check if Neo4j container is already running
if docker ps | grep -q neo4j-kant; then
    echo "⚠️  Neo4j container 'neo4j-kant' is already running"
    echo "To stop it: docker stop neo4j-kant"
    exit 0
fi

# Start Neo4j container
echo "🐳 Running Neo4j container..."
docker run -d \
  --name neo4j-kant \
  -p 7687:7687 \
  -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/kantphilosophy \
  neo4j:latest

# Wait a moment for container to start
sleep 10

# Check if container is running
if docker ps | grep -q neo4j-kant; then
    echo "✅ Neo4j is now running!"
    echo "📊 Access Neo4j Browser at: http://localhost:7474"
    echo "🔑 Default credentials: neo4j / kantphilosophy"
    echo ""
    echo "To stop Neo4j: docker stop neo4j-kant"
    echo "To remove container: docker rm neo4j-kant"
else
    echo "❌ Failed to start Neo4j container"
    echo "Check Docker logs with: docker logs neo4j-kant"
fi