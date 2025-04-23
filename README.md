Denne side dokumenterer forskellige scripts og kommandoer til opsætning og styring af software på en Raspberry Pi. Den dækker blandt andet oprettelse af brugere, mappehåndtering, visning af systeminformation, og eksekvering af Python-scripts. Derudover beskriver den brugen af shell- og bash-scripts, samt hvordan man opretter og administrerer en systemd-tjeneste ved hjælp af en Makefile.

```

# 1. Opret en ny bruger kaldet "testbruger"
echo "Opretter bruger 'testbruger'..."
sudo adduser --disabled-password --gecos "" testbruger

# 2. Log ind som testbruger og opret en mappe "Projekter"
echo "Opretter mappen 'Projekter' som testbruger..."
sudo -u testbruger mkdir -p /home/testbruger/Projekter

# 3. Udskriv systeminformation og kernel-version
echo "Systeminformation og kernel-version:"
uname -a

# 4. Udskriv information om Linux-distributionen
echo "Information om Linux-distribution:"
cat /etc/os-release
```

| **Feature** | **Shell Script** | **Bash Script** |
| --- | --- | --- |
| **Shebang** | #!/bin/sh | #!/bin/bash |
| **Shell kompatibilitet** | Kører på POSIX shell (mere generisk) | Specifik for Bash shell (flere features) |
| **Execution Environment** | Simpelt og universelt | Avanceret med arrays, funktioner m.m. |
| **Ekstra feature** | Simpelt og bærbart | Understøtter [[ ]], (( )), herestrings, etc. |

```bash
#!/bin/bash

# 1. Vis brugerens hjemmemappe
echo "Brugermappe: $HOME"

# 2. Naviger til brugerens hjemmemappe
cd "$HOME" || exit

# 3. Udskriv filer og mapper i brugermappen
echo "Indhold i brugermappen:"
ls -la

# 4. Opret folder: LinuxEmbedded
mkdir -p "$HOME/LinuxEmbedded"
echo "Mappen LinuxEmbedded er oprettet."

# 5. Opret Python-script: hello_world.py
cat << EOF > "$HOME/LinuxEmbedded/hello_world.py"
print("Hello, World!")
EOF
echo "Python script 'hello_world.py' er oprettet."

# 6. Eksekver Python-scriptet
echo "Kører hello_world.py:"
python3 "$HOME/LinuxEmbedded/hello_world.py"
```

Terminal udtag

```bash
momoamer@momopi:~/Documents $ chmod +x linux_demo.sh

momoamer@momopi:~/Documents $ ./linux_demo.sh
Brugermappe: /home/momoamer
Indhold i brugermappen:
total 100
drwx------ 18 momoamer momoamer 4096 Apr 22 11:09 .
drwxr-xr-x  4 root     root     4096 Apr 22 11:02 ..
-rw-r--r--  1 momoamer momoamer  220 Nov 19 14:32 .bash_logout
-rw-r--r--  1 momoamer momoamer 3523 Nov 19 14:32 .bashrc
drwxr-xr-x  2 momoamer momoamer 4096 Nov 19 14:36 Bookshelf
drwx------  5 momoamer momoamer 4096 Apr 22 10:55 .cache
drwx------  4 momoamer momoamer 4096 Nov 19 14:44 .config
drwxr-xr-x  2 momoamer momoamer 4096 Nov 19 14:44 Desktop
drwxr-xr-x  2 momoamer momoamer 4096 Apr 22 11:08 Documents
drwxr-xr-x  3 momoamer momoamer 4096 Apr 22 10:57 .dotnet
drwxr-xr-x  2 momoamer momoamer 4096 Nov 19 14:44 Downloads
drwxr-xr-x  2 momoamer momoamer 4096 Apr 22 11:09 LinuxEmbedded
drwxr-xr-x  4 momoamer momoamer 4096 Nov 19 14:44 .local
drwxr-xr-x  2 momoamer momoamer 4096 Nov 19 14:44 Music
drwxr-xr-x  2 momoamer momoamer 4096 Nov 19 14:44 Pictures
-rw-r--r--  1 momoamer momoamer  807 Nov 19 14:32 .profile
drwxr-xr-x  2 momoamer momoamer 4096 Nov 19 14:44 Public
drwx------  2 momoamer momoamer 4096 Nov 19 14:43 .ssh
-rw-r--r--  1 momoamer momoamer    0 Nov 19 14:44 .sudo_as_admin_successful
drwxr-xr-x  2 momoamer momoamer 4096 Nov 19 14:44 Templates
drwxr-xr-x  2 momoamer momoamer 4096 Nov 19 14:44 Videos
drwxr-x---  5 momoamer momoamer 4096 Apr 22 10:55 .vscode-server
-rw-r--r--  1 momoamer momoamer  183 Apr 22 10:54 .wget-hsts
-rw-------  1 momoamer momoamer   51 Nov 19 14:44 .Xauthority
-rw-------  1 momoamer momoamer 5831 Nov 19 14:44 .xsession-errors
Mappen LinuxEmbedded er oprettet.
Python script 'hello_world.py' er oprettet.
Kører hello_world.py:
Hello, World!
momoamer@momopi:~/Documents $
```

```makefile
# Makefile for Binary Clock 

TEMP_DIR=Temp
SCRIPT=binaryClock.py
SERVICE_NAME=binaryclock.service
SERVICE_PATH=/etc/systemd/system/$(SERVICE_NAME)
ROTATE ?= 0

.PHONY: setup run clean stopservice startservice create_service_file all

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

startservice: stopservice create_service_file
	sudo systemctl enable $(SERVICE_NAME)
	sudo systemctl start $(SERVICE_NAME)

all: setup run clean stopservice create_service_file startservice
```

Terminal udtag:

```bash
momoamer@momopi:~/Documents $ make startservice ROTATE=180
sudo systemctl stop binaryclock.service
sudo systemctl disable binaryclock.service
Removed "/etc/systemd/system/multi-user.target.wants/binaryclock.service".
sudo rm -f /etc/systemd/system/binaryclock.service
sudo systemctl daemon-reload
echo "[Unit]" | sudo tee /etc/systemd/system/binaryclock.service > /dev/null
echo "Description=Binary Clock for Sense HAT" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
echo "After=multi-user.target" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
echo "" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
echo "[Service]" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
echo "ExecStart=/usr/bin/python3 /home/momoamer/Documents/binaryClock.py -r 180" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
echo "Restart=always" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
echo "User=momoamer" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
echo "" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
echo "[Install]" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
echo "WantedBy=multi-user.target" | sudo tee -a /etc/systemd/system/binaryclock.service > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable binaryclock.service
Created symlink /etc/systemd/system/multi-user.target.wants/binaryclock.service → /etc/systemd/system/binaryclock.service.
sudo systemctl start binaryclock.service
```
