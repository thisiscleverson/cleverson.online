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

deploy: build stop
	sudo cp ./app.service /etc/systemd/system/ && \
	sudo systemctl enable app && \
	sudo systemctl restart app
