#!/bin/bash

USER_FOLDER="$1"
python3 -m venv "$USER_FOLDER/env"
source "$USER_FOLDER/env/bin/activate"
sudo apt update && sudo apt upgrade -y && sudo apt install git -y
git clone https://github.com/hikariatama/Hikka "$USER_FOLDER/Hikka"
cd "$USER_FOLDER/Hikka"
pip install -r requirements.txt
HIKKA_OUTPUT=$(python3 -m hikka 2>&1 &)
echo "$HIKKA_OUTPUT" > "$USER_FOLDER/hikka_output.log"
sleep 5
HIKKA_URL=$(tail -n 1 "$USER_FOLDER/hikka_output.log")
echo "Hikka успешно установлен и запущен. Ссылка на Hikka: $HIKKA_URL"
