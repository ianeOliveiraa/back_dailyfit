# DATABASE
docker run -d \
	--name some-postgres \
    -p 5433:5432 \
	-e POSTGRES_PASSWORD=123456 \
    -e POSTGRES_DB=dailyFit \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	postgres

docker start aa65599900d3

docker exec -it aa65599900d3 psql -U postgres
\c dailyFit


# 