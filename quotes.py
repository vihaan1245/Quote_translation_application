import requests

class Quotes:
    url = 'https://dummyjson.com/quotes/random'
    def get(self):
        try:
            response = requests.get(self.url)
            content = response.json()
            quote = content.get('quote')
            author = content.get('author')
            print(quote,author)
            return quote,author
        except Exception as e:
            print(e)
            return None, None

if __name__ == "__main__":
    obj = Quotes()
    print(obj.get())