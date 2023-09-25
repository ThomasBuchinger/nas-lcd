build:
	docker build --network host --tag lcd-display:latest .

run:
	docker run -it --rm --name lcd-display --privileged lcd-display:latest
