run:
	python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

build:
	docker build -t spatialist-backend .

local: build
	docker run -d -p 8000:8000 spatialist-backend:latest

release: build
	docker kill $(docker ps -a -q)
	docker --context spatialist-backend run -d spatialist-backend