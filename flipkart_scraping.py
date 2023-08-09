from bs4 import BeautifulSoup
import requests
import csv


def flipkart():
    try:
        response1 = requests.get("https://www.flipkart.com/search?q=laptop")
        response1.raise_for_status()
        soup1 = BeautifulSoup(response1.content, 'html.parser')

        page_number = soup1.find('div', {'class': '_2MImiq'}).find('span').text.split(' ')[-1]

        laptop_data = []

        for number in range(1, int(page_number)):
            response = requests.get(f"https://www.flipkart.com/search?q=laptop&page={number}")
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            main_content = soup.find_all('div', {'class': '_2kHMtA'})

            for laptop in main_content:
                name_element = laptop.find('div', {'class': '_4rR01T'})
                name = name_element.text.strip() if name_element else "N/A"

                price_element = laptop.find('div', {'class': '_30jeq3'})
                price = price_element.text.strip() if price_element else "N/A"

                rating_element = laptop.find('div', {'class': '_3LWZlK'})
                rating = rating_element.text.strip() if rating_element else "N/A"

                features_element = laptop.find('ul', {'class': '_1xgFaf'})

                processor = ''
                ram = ''
                os = ''
                display = ''
                warranty = ''
                storage = ''

                if features_element:
                    for element in features_element.find_all('li'):
                        if 'processor' in element.get_text(strip=True).lower():
                            processor += element.get_text(strip=True)

                        elif 'ram' in element.get_text(strip=True).lower():
                            ram += element.get_text(strip=True)

                        elif 'operating' in element.get_text(strip=True).lower():
                            os += element.get_text(strip=True)

                        elif 'display' in element.get_text(strip=True).lower():
                            display += element.get_text(strip=True)

                        elif 'warranty' in element.get_text(strip=True).lower():
                            warranty += element.get_text(strip=True)

                        elif 'gb' in element.get_text(strip=True).lower():
                            words = element.get_text(strip=True).split()
                            for word in words:
                                if word.isdigit():
                                    storage += element.get_text(strip=True)

                        else:
                            continue

                laptop_data.append({
                    "Name": name,
                    "Price": price,
                    "Rating": rating,
                    "Processor": processor,
                    "RAM": ram,
                    "OS": os,
                    "Display": display,
                    "Storage": storage,
                    "Warranty": warranty,
                })

        csv_file = "laptop_data.csv"
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Name", "Price", "Rating", "Processor", "RAM", "OS", "Display", "Storage", "Warranty"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(laptop_data)

        print(f"Data saved to {csv_file}")

    except requests.exceptions.RequestException as e:
        print("Error fetching Flipkart content:", e)
        return "Error fetching data."


flipkart()
