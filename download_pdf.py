import requests

url = "https://ncfe.org.in/wp-content/uploads/2023/11/BEAWARE07032022.pdf"
output_path = "data/ncfe_books/BEAWARE07032022.pdf"

response = requests.get(url, verify=False)
with open(output_path, 'wb') as f:
    f.write(response.content)

print(f"Downloaded to {output_path}")
