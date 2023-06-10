# The Goal

Currently, the goal of this project is to utilize the data from zygmuntz ["goodbooks-10k"](https://github.com/zygmuntz/goodbooks-10k) and some personal book review data of mine to obtain some book recommendations. I have cloned the mentioned repo under data/inputs/, and have simply removed the files that I didn't need. 

Under data/inputs/ you will also find a .csv file containing the personal raw data.

# Methodology

Quite simply, I'll be using python's Surprise to pass along the processed data and generate some book recommendations. I plan on eventually using Surprise's results to build a static webpage, displaying the best options of book recommendation for any given user.