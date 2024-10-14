pip install dora-keyboard==0.3.7rc0
pip install opencv-video-capture==0.3.7rc0
sudo wget 192.168.3.5:8000/dora -O /usr/local/bin/dora
sudo wget 192.168.3.5:8000/rerun -O /usr/local/bin/rerun
sudo wget 192.168.3.5:8000/dora-rerun -O /usr/local/bin/dora-rerun
sudo wget 192.168.3.5:8000/robot -O /usr/local/bin/robot

sudo chmod +x /usr/local/bin/dora
sudo chmod +x /usr/local/bin/rerun
sudo chmod +x /usr/local/bin/dora-rerun
sudo chmod +x /usr/local/bin/robot

sudo tee /etc/systemd/system/dora-daemon.service << EOF
Description=Dora Daemon in Conda Environment
After=network.target

[Service]
User=HwHiAiUser
Environment='PATH=$PATH'
WorkingDirectory=/home/HwHiAiUser
ExecStart=/bin/bash --login  -c 'source /home/HwHiAiUser/.bashrc && source $CONDA_PREFIX/bin/activate base && dora daemon --inter-daemon-addr 0.0.0.0:20001 --machine-id $(cat /etc/machine-id | head -c 3)'
Restart=always
RestartSec=3
StartLimitInterval=60
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable dora-daemon.service
sudo systemctl restart dora-daemon.service
