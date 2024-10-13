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
