from src.utils.imports import os
PROJECT_PATH = os.getcwd()

def main():

    # Decide whether or not to create the necessary data
    from src.utils.imports import create_data 
    create_data()

if __name__ == "__main__":
    main()