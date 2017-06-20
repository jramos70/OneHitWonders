import numpy
from sklearn.linear_model import LogisticRegression
import csv
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.gaussian_process.kernels import RBF

def do_ml():
	train_features = []
	train_labels = []
	with open("train_data.csv", 'r', encoding='latin1') as file_reader:
		reader = csv.reader(file_reader)
		next(reader, None)
		for row in reader:
			train_labels.append(row[8].lower())
			features = row[0].split('/') + row[5:7]
			features = list(map( lambda x: float(x), features))
			train_features.append(features)
	train_labels = numpy.array(train_labels)
	train_features = numpy.array(train_features)
	
	#classifier = AdaBoostClassifier()
	#classifier = RandomForestClassifier()
	#classifier = LogisticRegression()
	#classifier = BernoulliNB(binarize=None)
	classifier = KNeighborsClassifier()
	#classifier = MLPClassifier()
	#classifier = DecisionTreeClassifier()
	# classifier = QuadraticDiscriminantAnalysis()
	# classifier = GaussianProcessClassifier(1.0*RBF(1.0), warm_start=True)
	classifier.fit(train_features, train_labels)
	scores = cross_val_score(classifier, train_features, train_labels, scoring='accuracy', cv=100)

	#Test code
	train_features = []
	train_labels = []
	with open("test_data.csv", 'r', encoding='latin1') as file_reader:
		reader = csv.reader(file_reader)
		next(reader, None)
		for row in reader:
			train_labels.append(row[8].lower())
			features = row[0].split('/') + row[5:7]
			features = list(map( lambda x: float(x), features))
			train_features.append(features)
		
	predicted_labels = classifier.predict(train_features)

	print('predicted mean accuracy:')
	print(classifier.score(train_features, train_labels))

	print('sklearn confusion matrix:')
	print(confusion_matrix(train_labels, predicted_labels))

print(do_ml())
