import numpy as np
import pandas as pd
from catboost import CatBoostClassifier
from datetime import datetime

def get_ml(X, y):
	"""
	Provides with machine learning magic
	"""
	start = datetime.now()

	response = 'Using CatBoostClassifier**\n'

	response += 'Categorical features recognized:\n'
	cat_features = []
	for f in list(X.columns):
		if not X[f].dtype in [np.dtype('int'), np.dtype('float64')]:
			cat_features.append(f)
			response += ('* ' + f + '\n')
	response += '\n'

	cat_features = [list(X.columns).index(f) for f in cat_features]

	mdl = CatBoostClassifier()
	mdl.fit(np.array(X), y, cat_features=cat_features)
	response += 'Accuracy of the model: {}.\n\n'.format(round((mdl.predict(np.array(X), y) == y).mean(), 2))

	response += 'Most important features:\n'
	n_features = 3
	imp_f = np.array(X.columns)[np.argsort(mdl.feature_importance_)[-n_features:]][::-1]
	imp_fi = np.round(np.sort(mdl.feature_importance_)[-n_features:],2)[::-1]
	for i in range(n_features):
		response += '* {}: {}\n'.format(imp_f[i], imp_fi[i])

	elapsed = (datetime.now() - start).seconds
	response += '\n'
	response += 'Time elapsed: {} seconds'.format(elapsed)

	return response