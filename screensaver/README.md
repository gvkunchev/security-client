```
# See "Adjust if needed" lines in the shell file
sudo cp ./touchscreen-idle.sh /usr/local/bin
sudo chmod +x /usr/local/bin/touchscreen-idle.sh
sudo cp ./touchscreen-idle.service /etc/systemd/system/touchscreen-idle.service
sudo systemctl daemon-reload
sudo systemctl enable --now touchscreen-idle.service
```