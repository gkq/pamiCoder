import numpy as np
from sklearn import datasets, linear_model, cross_validation

# Load the diabetes dataset
diabetes = datasets.load_diabetes()

# Split the data into training/testing sets
diabetes_X_train = diabetes.data[:-20]
diabetes_X_test = diabetes.data[-20:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

# Create linear regression object
# regr = linear_model.LinearRegression()

# Create linear regression object
# regr = linear_model.Ridge( alpha=0)

# Create linear regression object
regr = linear_model.Lasso( alpha=0)




# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

# alphas = np.logspace(-4, -.5, 30)
# scores = list()
# scores_std = list()
# for alpha in alphas:
#       regr.alpha = alpha
#       this_scores = cross_validation.cross_val_score(regr, diabetes_X_train, diabetes_y_train, n_jobs=1)
#       scores.append(np.mean(this_scores))
#       scores_std.append(np.std(this_scores))
# print(alphas[scores.index(max(scores))])

# The coefficients

print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(diabetes_X_test) - diabetes_y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(diabetes_X_test, diabetes_y_test))