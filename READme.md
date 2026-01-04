This project is about searching for opinions in Amazon reviews using three different methods: a basic Boolean search, a proximity check to see if words are close together, and a sentiment method that uses review ratings to help match the opinion better.

I used a Conda environment called nlp to run the code. You can create it with:

conda create -n nlp python=3.13.5 -y
conda activate nlp

The only package you really need to install is pandas (pip install pandas). The other modules I used, like re and os, come with Python

To run the code, just make sure you have access to the reviews data pickle file. Then run:

python code1.py

for the baseline

python code2.py

for the other two methods.

Outputs are saved as text files with review IDs in the outputs folders -> commented out
Currently it outputs to terminal the # of retrieved ids of each method according to its query
