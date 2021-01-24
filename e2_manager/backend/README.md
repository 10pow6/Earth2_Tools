Setup Venv
```
python -m venv venv
venv\Scripts\active
pip install -r requirements.txt
```

```
uvicorn main:app
```

Note -- Only for testing, do not use
```
uvicorn main:app --reload
```

**URLs**

http://localhost:8000

http://localhost:8000/docs