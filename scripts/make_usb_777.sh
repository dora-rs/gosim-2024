sudo tee /etc/udev/rules.d/99-usb.rules << EOF
KERNEL=="ttyUSB0", MODE="0777"
EOF

sudo udevadm control --reload-rules