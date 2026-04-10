from dotenv import load_dotenv
import os
load_dotenv()

def main():
    print("Hello from hello-world!")
    print(os.environ.get("GOOGLE_API_KEY"))

if __name__ == "__main__":
    main()
