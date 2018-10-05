run:
	docker-compose stop
	docker-compose build
	docker-compose up

rund:
	docker-compose stop
	docker-compose build
	docker-compose up -d

launch: rund
	ssh -R koalasTEST:80:localhost:80 serveo.net

stop:
	docker-compose stop