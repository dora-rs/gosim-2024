# gosim-hackathon-2024

Repository for managing the GOSIM Hackathon 2024

## Installation

Get the installation script either from 192.168.3.5

```bash
wget 192.168.3.5:8000/install_default.sh
chmod +x install_default.sh
./install_default.sh
```

## Then connecct to the cloud from the Orange Pi

```bash
ssh root@ssh.openbayes.com -p 30773 -L 53290:0.0.0.0:53290 -R 20001:0.0.0.0:20001 -L 20002:0.0.0.0:20002
```

> Make sure to update the port "30773" to your port

## Once your in the cloud

```bash
# if not already present
# git clone https://github.com/dora-rs/gosim-2024
# cd gosim-2024

cd gosim-2024
./scripts/setup_cloud.sh
# Do it once
dora build qwenvl2_recorder.yml
dora start qwenvl2_recorder.yml
```
