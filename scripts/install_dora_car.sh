apt-get update
apt-get install wget unzip curl build-essential tmux -y 

wget https://repo.anaconda.com/miniconda/Miniconda3-py311_23.5.2-0-Linux-x86_64.sh
chmod +x  ./Miniconda3-py311_23.5.2-0-Linux-x86_64.sh
./Miniconda3-py311_23.5.2-0-Linux-x86_64.sh -bu
export PATH=$PATH:$HOME/miniconda3/bin
conda init bash
source ~/.bashrc
conda activate

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"

curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/dora-rs/dora/main/install.sh | bash
source ~/.bashrc

MACHINE_ID=$(cat /etc/machine-id | head -c 4)

sudo tee /etc/systemd/system/dora-daemon.service << EOF
[Unit]
Description=Dora Daemon in Conda Environment
After=network.target

[Service]
Environment="PATH=$PATH"
User=HwHiAiUser
WorkingDirectory=/home/HwHiAiUser
ExecStart=/bin/bash --login  -c 'source /home/HwHiAiUser/.bashrc && source $CONDA_PATH/bin/activate base && dora daemon --inter-daemon-addr 0.0.0.0:20001'
Restart=always
RestartSec=3
StartLimitInterval=60
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable dora-daemon.service
sudo systemctl start dora-daemon.service