## SSH
SSH_CONNECTION = peter@192.168.3.112

sudo tee /etc/systemd/system/ssh-client.service << EOF
Description=SSH Client 
After=network.target

[Service]
User=HwHiAiUser
User=HwHiAiUser
ExecStart=/bin/bash --login  -c 'source /home/HwHiAiUser/.bashrc && ssh -N $SSH_CONNECTION -L 53290:0.0.0.0:53290 -R 20001:0.0.0.0:20001 -L 20002:0.0.0.0:20002'
Restart=always
RestartSec=3
StartLimitInterval=60
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ssh-client.service
sudo systemctl restart ssh-client.service