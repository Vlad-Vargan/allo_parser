import requests

url = "https://allo.ua/ua/catalogsearch/ajax/suggest/?currentTheme=main&currentLocale=uk_UA"

res = requests.post(url, data={"q": "гмо"})
print(res.json())