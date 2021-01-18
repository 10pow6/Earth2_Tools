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

Console 2 Activate Venv & Do Unit Tests (later this will be frontend instructions)
```
venv\Scripts\active
unit_testing.py
```

Sample Output
```
==Hello World==
{"Made with love":"by Dworak and butt"}
==E2 Countries==
{'data': {'getTilePrices': [{'countryCode': 'US', 'tradeAverage': 6.394, 'final': 38.802, 'totalTilesSold': 597176}, {'countryCode': 'NU', 'tradeAverage': 0.175, 'final': 0.274, 'totalTilesSold': 101183}]}}
==Current DB Countries Prior Load==
[{'country_code': 'US', 'update_time': '2021-01-15T23:22:02.046000', 'trade_average': 6.393, 'final': 38.802, 'total_tiles_sold': 597169, 'id': 1}, {'country_code': 'NU', 'update_time': '2021-01-15T23:22:02.046000', 'trade_average': 0.175, 'final': 0.274, 'total_tiles_sold': 101183, 'id': 2}]
==Current DB Countries After Load==
[{'country_code': 'US', 'update_time': '2021-01-15T23:26:55.545000', 'trade_average': 6.394, 'final': 38.802, 'total_tiles_sold': 597176, 'id': 1}, {'country_code': 'NU', 'update_time': '2021-01-15T23:26:55.545000', 'trade_average': 0.175, 'final': 0.274, 'total_tiles_sold': 101183, 'id': 2}]
==Get just US==
[{'country_code': 'US', 'update_time': '2021-01-15T23:26:55.545000', 'trade_average': 6.394, 'final': 38.802, 'total_tiles_sold': 597176, 'id': 1}]
```



http://localhost:8000