pip install dora-keyboard==0.3.7rc0
pip install opencv-video-capture==0.3.7rc0
sudo wget 192.168.3.5:8000/dora -O -nc /usr/local/bin/dora
sudo wget 192.168.3.5:8000/rerun -O -nc /usr/local/bin/rerun
sudo wget 192.168.3.5:8000/dora-rerun -O -nc /usr/local/bin/dora-rerun
sudo wget 192.168.3.5:8000/robot -O -nc /usr/local/bin/robot

sudo chmod +x /usr/local/bin/dora
sudo chmod +x /usr/local/bin/rerun
sudo chmod +x /usr/local/bin/dora-rerun
sudo chmod +x /usr/local/bin/robot
