import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline, make_union
from itertools import chain
from sklearn.linear_model import LogisticRegression
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import AdaBoostClassifier
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import os

from sklearn.base import BaseEstimator, TransformerMixin

class C1(BaseEstimator, TransformerMixin):

		def fit(self, X, y=None, **fit_params):
				return self

		def transform(self, X, **transform_params):
				lst = [_.strip() for _ in chain.from_iterable(X.str.split('.').tolist())]
				print(lst)
				return lst

class Lemmatizer:

	def __init__(self):

		self.wnl = WordNetLemmatizer()
		self.stemmer = PorterStemmer()

	def __call__(self, doc):

		return [self.stemmer.stem(t) for t in word_tokenize(doc)]

class Coookings:

	def __init__(self):

		self.train_data = pd.read_json('data/train.json', orient='records')
		self.test_data = pd.read_json('data/test.json', orient='records')

	def split(self):

		X = self.train_data['ingredients'].str.join('. ')
		y = self.train_data['cuisine']

		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, 
					test_size=0.25, random_state=111, stratify=y)

		return self

	def train_model(self):

		self.pipeline = make_pipeline(CountVectorizer(tokenizer=Lemmatizer(), strip_accents='ascii', 
											analyzer='word', ngram_range=(1,2)),
												LogisticRegression())
		print('fitting pipeline...')

		self.pipeline.fit(self.X_train, self.y_train)

		return self

	def predict(self):

		print('making prediction...')
		# note: prediction is a numpy array
		self.y_pred = self.pipeline.predict(self.X_test)

		print('creating submission..')
		yhat = pd.Series(self.pipeline.predict(self.test_data['ingredients'].str.join('. ')), 
													name='cuisine', 
														index=self.test_data['id'])

		if not os.path.exists('submission'):
			os.mkdir('submission')

		yhat.to_csv('submission/submission.csv', header=True)

		return self


		

	def get_metrics(self):

		self.accuracy = accuracy_score(self.y_test, self.y_pred)
		print(f'accuracy: {self.accuracy: .4f}')


if __name__ == '__main__':

	cook = Coookings().split().train_model().predict().get_metrics()