# Makefile for Binary Clock Project

TEMP_DIR=Temp
SCRIPT=binaryClock.py
SERVICE_NAME=binaryclock.service
SERVICE_PATH=/etc/systemd/system/$(SERVICE_NAME)
ROTATE ?= 0


setup:
	mkdir -p $(TEMP_DIR)
	cp $(SCRIPT) $(TEMP_DIR)/
	chmod +x $(TEMP_DIR)/$(SCRIPT)

manpage:
	@echo "Generating man page..."
	# e.g. pandoc -s -t man binaryClock.md -o binaryClock.1
	# sudo cp binaryClock.1 /usr/local/share/man/man1/

run:
	python3 $(SCRIPT) -r $(ROTATE)

clean:
	rm -rf $(TEMP_DIR)

stopservice:
	sudo systemctl stop $(SERVICE_NAME)
	sudo systemctl disable $(SERVICE_NAME)
	sudo rm -f $(SERVICE_PATH)
	sudo systemctl daemon-reload

create_service_file:
	echo "[Unit]" | sudo tee $(SERVICE_PATH) > /dev/null
	echo "Description=Binary Clock for Sense HAT" | sudo tee -a $(SERVICE_PATH) > /dev/null
	echo "After=multi-user.target" | sudo tee -a $(SERVICE_PATH) > /dev/null
	echo "" | sudo tee -a $(SERVICE_PATH) > /dev/null
	echo "[Service]" | sudo tee -a $(SERVICE_PATH) > /dev/null
	echo "ExecStart=/usr/bin/python3 /home/momoamer/Documents/$(SCRIPT) -r $(ROTATE)" | sudo tee -a $(SERVICE_PATH) > /dev/null
	echo "Restart=always" | sudo tee -a $(SERVICE_PATH) > /dev/null
	echo "User=momoamer" | sudo tee -a $(SERVICE_PATH) > /dev/null
	echo "" | sudo tee -a $(SERVICE_PATH) > /dev/null
	echo "[Install]" | sudo tee -a $(SERVICE_PATH) > /dev/null
	echo "WantedBy=multi-user.target" | sudo tee -a $(SERVICE_PATH) > /dev/null
	sudo systemctl daemon-reload

startservice: create_service_file
	sudo systemctl enable $(SERVICE_NAME)
	sudo systemctl start $(SERVICE_NAME)

all: setup clean manpage stopservice create_service_file startservice