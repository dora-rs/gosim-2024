sudo tee /etc/systemd/system/dora-coordinator.service << EOF
Description=Dora Coordinator
After=network.target

[Service]
User=$USER
Environment='PATH=$PATH'
WorkingDirectory=/home/$USER
ExecStart=/bin/bash -c 'source /home/$USER/.bashrc && source $CONDA_PREFIX/bin/activate base && dora coordinator'
Restart=always
RestartSec=3
StartLimitInterval=60
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable dora-coordinator.service
sudo systemctl restart dora-coordinator.service
