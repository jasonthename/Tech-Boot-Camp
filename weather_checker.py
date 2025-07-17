#Try running this on your system or on Google Colab - https://colab.research.google.com/

import requests

city = "London"
url = f"https://wttr.in/{city}?format=3"

response = requests.get(url)
print(response.text)