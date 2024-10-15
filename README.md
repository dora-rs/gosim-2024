## Gosim Hackathon 2024

> Repository for managing the GOSIM Hackathon 2024

#### OrangePi Installation

- Get the installation script either from 192.168.3.5

```bash
wget 192.168.3.5:8000/gosim-2024/install_orangepi.sh
chmod +x install_orangepi.sh
./install_orangepi.sh
source ~/.bashrc
```

If this is successful, you should be able to:

```bash
dora --help
```

---

#### Follower Dora Daemon Linux Service

- Then you should create a dora daemon service

```
wget 192.168.3.5:8000/gosim-2024/start_follower_dora_daenon_service.sh
chmod +x start_follower_dora_daenon_service.sh
./start_follower_dora_daenon_service.sh
```

If this is successful, you should not have error when calling:

```bash
sudo systemctl status dora-daemon.service
```

Return:

```bash
● dora-daemon.service
     Loaded: loaded (/etc/systemd/system/dora-daemon.service; enabled; preset: enabled)
     Active: active (running) since Tue 2024-10-15 00:25:58 CEST; 13min ago
   Main PID: 256635 (dora)
      Tasks: 34 (limit: 37374)
     Memory: 3.2M
        CPU: 122ms
     CGroup: /system.slice/dora-daemon.service
             └─256635 dora daemon --inter-daemon-addr 0.0.0.0:20002
```

---

#### Follower SSH Linux Service

- Then you should create a ssh service

```bash
export SSH_CONNECTION=peter@192.168.3.112
ssh-copy-id $SSH_CONNECTION
chmod +x ./scripts/start_ssh_service.sh
./scripts/start_ssh_service.sh
```

If this is successful, you should not have error when calling:

```bash
sudo systemctl status ssh-client.service
```

```bash
● ssh-client.service
     Loaded: loaded (/etc/systemd/system/ssh-client.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2024-10-15 11:05:06 CST; 1h 44min ago
   Main PID: 4302 (ssh)
      Tasks: 1 (limit: 27120)
     Memory: 2.2M
     CGroup: /system.slice/ssh-client.service
             └─4302 ssh -N peter@192.168.3.112 -L 53290:0.0.0.0:53290 -R 20001:0.0.0.0:20001 -L 20002:0.0.0.0:20002
```

---

#### SSH Connection to the cloud from the Orange Pi

Now you should be able to connect to the cloud from any computers

```bash
ssh root@ssh.openbayes.com -p 30773
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
```

#### Testing Hardware

##### Testing cameras

```bash
## Within the orangepi
ls /dev/video*
```

If you connected 2 cameras properly, this should return

```
/dev/video0  /dev/video1 /dev/video2  /dev/video3
```

##### Testing car

Run:

```bash
## Within the orangepi
robot
```

If the installation is successful, you should get:

```bash
Error: env variable DORA_NODE_CONFIG must be set. Are you sure your using `dora start`?

Caused by:
    environment variable not found

Location:
    /home/HwHiAiUser/.cargo/registry/src/index.crates.io-6f17d22bba15001f/dora-node-api-0.3.6/src/node/mod.rs:67:57
```

If not you should try:

```bash
sudo chmod 777 /dev/ttyUSB0
```

If you get `serial connect fail` means that there is a problem with the board.

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

---

### To start on your own computer

#### Leader Dora Daemon Linux Service

- Then you should create a dora daemon service

```
chmod +x ./scripts/start_leader_dora_daenon_service.sh
./scripts/start_leader_dora_daenon_service.sh
```

If this is successful, you should not have error when calling:

```bash
sudo systemctl status dora-daemon.service
```

Return:

```bash
● dora-daemon.service
     Loaded: loaded (/etc/systemd/system/dora-daemon.service; enabled; preset: enabled)
     Active: active (running) since Tue 2024-10-15 00:25:58 CEST; 13min ago
   Main PID: 256635 (dora)
      Tasks: 34 (limit: 37374)
     Memory: 3.2M
        CPU: 122ms
     CGroup: /system.slice/dora-daemon.service
             └─256635 dora daemon --inter-daemon-addr 0.0.0.0:20001
```

---

#### Leader Dora Coordinator Linux Service

- Then you should create a dora coordinator service

```
chmod +x ./scripts/start_leader_dora_coordinator_service.sh
./scripts/start_leader_dora_coordinator_service.sh
```

If this is successful, you should not have error when calling:

```bash
sudo systemctl status dora-coordinator.service
```

Return:

```bash
● dora-coordinator.service
     Loaded: loaded (/etc/systemd/system/dora-coordinator.service; enabled; preset: enabled)
     Active: active (running) since Tue 2024-10-15 00:54:12 CEST; 2s ago
   Main PID: 315394 (dora)
      Tasks: 34 (limit: 37374)
     Memory: 3.2M
        CPU: 62ms
     CGroup: /system.slice/dora-coordinator.service
             └─315394 dora coordinator

Oct 15 00:54:12 peter-rog systemd[1]: Started dora-coordinator.service.
Oct 15 00:54:12 peter-rog bash[315394]: Listening for incoming daemon connection on 53290
```

---
