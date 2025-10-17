import requests
import sys


BASE_URL = "https://v6.exchangerate-api.com/v6/" #Базовая ссылка
API_KEY = "38bc386b7b0424144fb3caad/latest/"
def fetch_exchange_rate(base_currency, target_currency):
    url = f"{BASE_URL}{API_KEY}{base_currency.upper()}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() #Автоматическая обрабтка ошибок 4хх 
        
        data = response.json()
        
        if data['result'] == 'error':
            return f"Ошибка API: {data.get('error-type', 'Неизвестная ошибка')}"
        
        # Получение курса для целевой валюты
        rate = data['conversion_rates'].get(target_currency.upper())
        
        if rate is None:
            return f"Ошибка: Валюта '{target_currency.upper()}' не найдена."
            
        return rate
        
    except requests.exceptions.RequestException as e:
        return f"Ошибка подключения или сети: {e}"
    except KeyError:
        return "Ошибка: Неправильный формат ответа от API."

def main():
    # Проверка, что переданы 2 аргумента: базовая и целевая валюты
    if len(sys.argv) != 3:
        print("Использование: python main.py <Базовая_Валюта> <Целевая_Валюта>")
        print("Пример: python main.py USD RUB")
        sys.exit(1)

    base = sys.argv[1]
    target = sys.argv[2]
    
    print(f"Запрос курса: 1 {base.upper()} -> {target.upper()}...")
    
    rate = fetch_exchange_rate(base, target)
    
    if isinstance(rate, float):
        print("---------------------------------------")
        print(f"Курс: 1 {base.upper()} = {rate:.4f} {target.upper()}")
        print("---------------------------------------")
    else:
        print(f"Не удалось получить курс: {rate}")

if __name__ == "__main__":
    main()