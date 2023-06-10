from .utils.imports import os
from .utils.imports import pd
from .utils.imports import PROJECT_PATH

def preprocess():

    # Var                               File                        Description
    # goodbooks_books_raw               books.csv                   Contains raw metadata from books
    # personal_raw                      personal_raw.csv            Contains raw metadata from personal-books

    # personal_rated                    n/a                         Contains titles and ratings of personal-books that have been rated
    # rated_titles                      n/a                         Contains just the titles of personal-books that have been rated 

    # goodbooks_rated                   n/a                         Contains the id and title of books that have been rated

    # merged                            n/a                         Merge of personal_rated and goodbooks_rated

    # personal_preprocessed             personal_preprocessed.csv   Removing title info, adding user_id, renaming columns
    


    goodbooks_books_raw = pd.read_csv(os.path.join(PROJECT_PATH, "data", "inputs", "goodbooks-10k", "books.csv"))
    personal_raw = pd.read_csv(os.path.join(PROJECT_PATH, "data", "inputs", "personal_raw.csv"))

    personal_rated = personal_raw[personal_raw["My Rating"] != 0][["Title", "My Rating"]]
    rated_titles = personal_rated["Title"].to_numpy()

    goodbooks_rated = goodbooks_books_raw[goodbooks_books_raw["title"].isin(rated_titles)][["book_id", "title"]]

    merged = pd.merge(goodbooks_rated, personal_rated, left_on="title", right_on="Title", how="left")

    # Removing book titles
    personal_preprocessed = merged.drop("Title", axis=1)
    personal_preprocessed = personal_preprocessed.drop("title", axis=1)
    # Adding user id
    uid = get_last_user_id() 
    new_user_id_col = [uid] * len(personal_preprocessed)
    personal_preprocessed.insert(0, "user_id", new_user_id_col)
    # Rename ratings column
    personal_preprocessed = personal_preprocessed.rename(columns={"My Rating": "rating"})
    # Saving
    personal_preprocessed.to_csv(os.path.join(PROJECT_PATH, "data", "outputs", "personal_preprocessed.csv"), index=False)

def get_last_user_id():
    ratings = pd.read_csv(os.path.join(PROJECT_PATH, "data", "inputs", "goodbooks-10k", "ratings.csv"))
    last_user = (lambda x: x[0] + 1)(ratings.tail(1)["user_id"].to_list())
    return last_user

def create_final_ratings():
    # Basically just concat the ratings from the goodbooks-10k dataset with the preprocessed personal ratings

    # Raw data
    goodbooks_ratings_raw = pd.read_csv(os.path.join(PROJECT_PATH, "data", "inputs", "goodbooks-10k", "ratings.csv"))
    personal_preprocessed = pd.read_csv(os.path.join(PROJECT_PATH, "data", "outputs", "personal_preprocessed.csv"))

    # Concat
    final_processed = pd.concat([goodbooks_ratings_raw, personal_preprocessed], axis=0, ignore_index=True)

    # Save
    final_processed.to_csv(os.path.join(PROJECT_PATH, "data", "outputs", "final_ratings.csv"), index=False)

def create_data():

    # Do we have final_ratings.csv?
    print("Looking for final_ratings.csv...")
    if not os.path.exists(os.path.join(PROJECT_PATH, "data", "outputs", "final_ratings.csv")):

        print("Not found, creating final_ratings.csv...")

        # Do we have personal_preprocessed.csv?
        print("\tLooking for personal_preprocessed.csv...")
        if not os.path.exists(os.path.join(PROJECT_PATH, "data", "outputs", "personal_preprocessed.csv")):
            
            print("\tNot found, creating personal_preprocessed.csv...")
            preprocess()
            print("\tDone creating personal_preprocessed.csv!")

        else:
            print("\tFound personal_preprocessed.csv!")

        create_final_ratings()
        print("Done creating final_ratings.csv!")
    
    else:
        print("Found final_ratings.csv!")