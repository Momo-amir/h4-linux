
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