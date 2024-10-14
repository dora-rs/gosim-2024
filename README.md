## Gosim Hackathon 2024

> Repository for managing the GOSIM Hackathon 2024

#### OrangePi Installation

Get the installation script either from 192.168.3.5

```bash
wget 192.168.3.5:8000/gosim-2024/install_orangegi.sh
chmod +x install_orangegi.sh
./install_orangegi.sh
```

---

#### SSH Connection to the cloud from the Orange Pi

```bash
ssh root@ssh.openbayes.com -p 30773 -L 53290:0.0.0.0:53290 -R 20001:0.0.0.0:20001 -L 20002:0.0.0.0:20002
```

> Make sure to update the port "30773" to your port

---

#### Cloud Installation

```bash
# if not already present
git clone https://github.com/dora-rs/gosim-2024
cd gosim-2024
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/dora-rs/dora/main/install.sh | bash -s -- --tag v0.3.7rc0

source ~/.bashrc
dora build qwenvl2_recorder.yml
```

---

#### Cloud Usage

```bash

cd gosim-2024
# Do it once

./scripts/setup_cloud.sh

dora start qwenvl2_recorder.yml
```

---

#### Training

```bash
cd $HOME/LLaMA-Factory

vim  examples/train_lora/qwen2vl_lora_sft.yaml
llamafactory-cli train examples/train_lora/qwen2vl_lora_sft.yaml
```
