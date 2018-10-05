run:
	docker-compose stop
	docker-compose build
	docker-compose up -d

rund:
	docker-compose stop
	docker-compose build
	docker-compose up