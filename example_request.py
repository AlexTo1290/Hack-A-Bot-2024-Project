import requests
import numpy as np
import json

exInput = np.ones((1, 180, 180, 3))

data = json.dumps({"signature_name": "serving_default", "inputs":
                   {"input_1": exInput.tolist()}
                   })

headers = {"content-type": "application/json"}
url = "http://localhost:8501/v1/models/model:predict"

json_response = requests.post(url=url, data=data, headers=headers)
print(json_response.text)
