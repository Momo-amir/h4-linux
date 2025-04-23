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