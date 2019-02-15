# demo_game

## Back-end setup
Install pip packages to your virtual environment.
```
pip install -r backend/requirements.txt
```

Migrate models. (In backend folder)
```
python manage.py migrate
```

Run server. (In backend folder)
```
python manage.py runserver
```

## Front-end setup
Install npm.
```
https://www.npmjs.com/get-npm
```

Install npm packages.
*Need to setup proxy https://jjasonclark.com/how-to-setup-node-behind-web-proxy/*
```
cd frontend && npm install
```

Run. (In frontend folder)
```
npm run serve
```