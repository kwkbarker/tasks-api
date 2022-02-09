# tasks-api

TO RUN API:
cd api
source venv/bin/activate
python3 -m pip install -r requirements.txt
export FLASK_APP=main.py
flask run

TO RUN FRONTEND:
cd frontend
yarn install
yarn vite --config vite.config.js /src
