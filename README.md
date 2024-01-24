# aigic-docker

sudo docker build -t aigic .

sudo docker tag aigic ctwel/aigic:0125

sudo docker push ctwel/aigic:0119

sudo docker run --gpus all -d  -p 5001:5001  ctwel/aigic:0125