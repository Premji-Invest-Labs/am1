echo "AM1 - Bringing previous instances of docker containers down"
docker compose down
echo "AM1 - Docker Compose Building..."
docker compose up --build -d
echo "AM1 - Docker Compose Done"