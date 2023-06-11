from src.utils.imports import os
PROJECT_PATH = os.getcwd()

def main():

    # Decide whether or not to create the necessary data
    from src.utils.imports import create_data_or_not
    create_data_or_not()

    # Decide whether or not to create the model
    from src.utils.imports import create_model_or_not
    create_model_or_not()

    # Just testing the model
    from src.utils.imports import get_top_n_titles
    gil_id = 49926
    import random as rand
    random_id = rand.randint(1, 49926)
    get_top_n_titles(random_id)

if __name__ == "__main__":
    main()