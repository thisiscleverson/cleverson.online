start-docker:
	docker compose up -d

start-service:
	sudo systemctl start app

stop:
	docker compose down

status:
	sudo systemctl status app

build:
	docker compose up --build

deploy: 
	docker compose down \
	docker compose pull \
	docker compose up -d \