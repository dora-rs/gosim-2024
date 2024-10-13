BASEDIR=$(dirname $0)
sudo cp $BASEDIR/dora-daemon.service /etc/systemd/system/dora-daemon.service

sudo systemctl daemon-reload
sudo systemctl enable dora-daemon.service
sudo systemctl start dora-daemon.service