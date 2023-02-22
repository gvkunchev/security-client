# Home security client

* Running  
  mkdir /home/pi/.config/autostart/

  vim /home/pi/.config/autostart/SecurityClient.desktop:
  
    ```
    [Desktop Entry]
    Name=Security Client
    Type=Application
    Comment=Home Security Client GUI
    Exec=/usr/bin/python /home/pi/Desktop/security-client/controller.py
    ```

  chmod +x /home/pi/.config/autostart/SecurityClient.desktop
