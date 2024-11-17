# Utilise une image de base Ubuntu
FROM debian:11-slim

# Met à jour et installe les outils nécessaires
RUN apt-get update && apt-get install -y \
python3-minimal \
python3-pip \
binwalk \
squashfs-tools \
less \
binutils \
vim \
libusb-1.0-0-dev \
xxd \
grep \
liblzma-dev \
bsdmainutils \
flashrom \
minicom \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Installe miniterm.py via pyserial
RUN python3 -m pip install pyserial

# Crée un dossier de travail
WORKDIR /workspace

# Définis le point d’entrée en bash pour les sessions interactives
CMD ["/bin/bash"]
