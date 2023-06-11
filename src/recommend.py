def cross_validation(k=5): 
    from .utils.imports import PROJECT_PATH, os, pd
    from .utils.imports import Dataset, Reader, SVD, dump, cross_validate 
    
    # Get the final ratings data
    ratings = pd.read_csv(os.path.join(PROJECT_PATH, "data", "outputs", "final_ratings.csv"))

    # Create Reader object
    reader = Reader(rating_scale=(1, 5))

    # Create Dataset
    data = Dataset.load_from_df(ratings, reader=reader)

    algorithm = SVD()

    # Split the data into 5 groups, run cross validation of SVD for "RMSE and MEA" accuracy measures
    cross_validate(algorithm, data, measures=["RMSE", "MAE"], cv=k, verbose=True)

def model_full_svd():
    from .utils.imports import PROJECT_PATH, os, pd
    from .utils.imports import Reader, Dataset, SVD, dump

    # Get the final ratings data
    print("\tLoading ratings data")
    ratings = pd.read_csv(os.path.join(PROJECT_PATH, "data", "outputs", "final_ratings.csv"))

    # Create the reader
    print("\tCreating reader")
    reader = Reader(rating_scale=(1, 5))

    # Create the Dataset using the ratings DataFrame and the Reader
    print("\tCreating dataset")
    data = Dataset.load_from_df(ratings, reader=reader)

    # Create the trainset from the full Dataframe
    print("\tCreating train set as full data")
    trainset = data.build_full_trainset()

    # Select SVD as the algorithm
    print("\tCreating SVD algorithm")
    algorithm = SVD()

    # Training (essentially creating the model) with the created trainset
    print("\tTraining algorithm on trainset")
    algorithm.fit(trainset)

    # # Create the testset as the anti of the trainset
    # # If the trainset consists of all known ratings,
    # # the testset will consist of all unknown ratings
    # print("\tCreating test set as anti of train set")
    # testset = trainset.build_testset()

    # # Generate the predictions of our model for the testset
    # print("\tCreating predictions by testing trained algorithm on testset")
    # predictions = algorithm.test(testset)

    # Save the generated predictions and the model
    print("\tSaving created model")
    dump.dump(os.path.join(PROJECT_PATH, "data", "outputs", "surprises", "model_pred.pickle"),
              algo=algorithm)

def model_pred_part_svd():
    from .utils.imports import PROJECT_PATH, os, pd
    from .utils.imports import Reader, Dataset, SVD, dump, train_test_split

    # Get the final ratings data
    print("\tLoading ratings data")
    ratings = pd.read_csv(os.path.join(PROJECT_PATH, "data", "outputs", "final_ratings.csv"))

    # Create the reader
    print("\tCreating reader")
    reader = Reader(rating_scale=(1, 5))

    # Create the Dataset using the ratings DataFrame and the Reader
    print("\tCreating dataset")
    data = Dataset.load_from_df(ratings, reader=reader)

    # Create the trainset (75%) and the testset (25%)
    print("\tCreating train and test set as sharing part of data")
    trainset, testset = train_test_split(data, test_size=0.25)

    # Select SVD as the algorithm
    print("\tCreating SVD algorithm")
    algorithm = SVD()

    # Training (essentially creating the model) with the created trainset
    print("\tTraining algorithm on trainset")
    algorithm.fit(trainset)

    # Generate the predictions of our model for the testset
    print("\tCreating predictions by testing trained algorithm on testset")
    predictions = algorithm.test(testset)

    # Save the generated predictions and the model
    print("\tSaving created model and predictions")
    dump.dump(os.path.join(PROJECT_PATH, "data", "outputs", "surprises", "model_pred.pickle"),
              predictions=predictions, 
              algo=algorithm)


def create_model_or_not():
    from .utils.imports import os, PROJECT_PATH

    # If we cannot find the model and predictions
    print("Looking for model_pred.pickle ...")
    if not os.path.exists(os.path.join(PROJECT_PATH, "data", "outputs", "surprises", "model_pred.pickle")):

        # Create them
        print("Not found, creating model_pred.pickle ...")
        model_full_svd()
        print("Done creating model_pred.pickle !")

    else:

        print("Found model_pred.pickle !")

def load_model(model_path):
    from .utils.imports import dump

    predictions, model = dump.load(model_path)

    return model

def get_top_n_iids(uid, n=10):
    from .utils.imports import PROJECT_PATH, os

    # Load in the created model
    model = load_model(os.path.join(PROJECT_PATH, "data", "outputs", "surprises", "model_pred.pickle"))

    # Empty list for the ids of recommended items
    best_predictions = []

    # Get the top-n predictions
    for iid in range(1, 10001):
        # Prediction is a tuple(uid, iid, real rating, estimated rating, _)
        prediction = model.predict(uid, iid, verbose=False)

        # If there are no recommendations:
            # Append the new recommendation
            # Go to next recommendation
        # Else:
            # Follow through normally

        # If there are already n recommendations:
            # If the new recommendation is better than existing ones:
                # Remove the lowest rated existing recommendation
                # Add the new recommendation
                # Go to the next recommendation
            # Else:
                # Go to next recommendation
        # Else
            # Append the new recommendation
            # Go to the next recommendation

        if not best_predictions:
            best_predictions.append(prediction) 
            continue

        # print(iid, best_predictions)

        if len(best_predictions) == n:

            current_ratings_too_low = prediction[3] > min(best_predictions, key=lambda x: x[3])[3]
            if current_ratings_too_low:
                best_predictions.sort(key=lambda x: x[3])
                best_predictions.pop(0)
                best_predictions.append(prediction)
            else:
                continue
            
        else:
            best_predictions.append(prediction)
            continue

    best_predictions.sort(key=lambda x: x[3])
    # tuple(iid, est)
    best_recommendations = [(i[1], i[3]) for i in best_predictions] 

    return best_recommendations

def get_top_n_titles(uid, n=10):
    best_recommendations = get_top_n_iids(uid, n)

    from src.utils.imports import PROJECT_PATH, os, pd

    goodbooks_books_raw = pd.read_csv(os.path.join(PROJECT_PATH, "data", "inputs", "goodbooks-10k", "books.csv"))

    print(f"\nTop {n} book recommendations for user id {uid}")

    for index, book in enumerate(reversed(best_recommendations), start=1):
        book_id = book[0]
        book_est = book[1]
        book_title = (goodbooks_books_raw.query("book_id == @book_id"))["title"].to_numpy()[0]
        print(f"{index}) \"{book_title}\", estimated rating: {book_est:.3g}")