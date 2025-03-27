This script retrieve pulse from many energy counter referenced in a dict variable, made a mean kWh, and inject them in influxdb


You can add it as a service, creating /etc/systemd/systemm/energymeter.service

[Unit]
Description=Lancement de la capture impulsion
After=network.target

[Service]
ExecStart=/opt/Energymeter/.venv/bin/python3 /opt/Energymeter/energymeter.py
WorkingDirectory=/opt/Energymeter
StandardOutput=journal
StandardError=inherit
Restart=always
User=OKTO
Group=OKTO
Environment="INFLUXDB_TOKEN=VIuV15zmKXnXSRaYltEz4Qaxa8EmqVQ5WzuecDHuS3PltDd3oHxQZUL7VQkfHcOOG-Eb19LdGvw1Tk36ZsFdmQ=="

[Install]
WantedBy=multi-user.target
