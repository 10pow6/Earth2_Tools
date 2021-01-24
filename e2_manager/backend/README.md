Setup Venv
```
python -m venv venv
venv\Scripts\active
pip install -r requirements.txt
```

Console 1 Activate Venv & Start Backend Server
```
venv\Scripts\active
uvicorn main:app
```

Note -- Only for testing, do not use
```
uvicorn main:app --reload
```

**URL**
http://localhost:8000
http://localhost:8000/docs