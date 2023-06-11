# PROJECT_PATH must come after os, else cyclical import happens
import os
from main import PROJECT_PATH

import numpy as np
import pandas as pd

from ..output_ratings_data_creator import create_data_or_not

from surprise import Dataset, Reader, SVD, dump
from surprise.model_selection import train_test_split, cross_validate
from ..recommend import create_model_or_not

from ..recommend import get_top_n_titles