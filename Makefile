start-docker:
	docker compose up -d

start-service:
	sudo systemctl start app

stop:
	docker compose down

status:
	sudo systemctl status app

build:
	docker compose up --build &&\
	docker compose down

deploy:
	sudo cp ./app.service /etc/systemd/system/ && \
	sudo systemctl enable app && \
	sudo systemctl restart app
