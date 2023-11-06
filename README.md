## build image
sudo docker build -t spatialist-backend .

## run container
sudo docker run -it --rm -p 8000:8000 --name spatialist-backend spatialist-backend