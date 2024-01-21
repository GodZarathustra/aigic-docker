cd /app/stable-diffusion-webui
python3 launch.py --ckpt /app/stable-diffusion-webui/models/Stable-diffusion/Realistic_Vision_V1.4.safetensors --api &
cd /app/server
# sudo chmod -R 777 . || true
python3 aipaint.py
# tail -f aipaint.py