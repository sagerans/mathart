import numpy as np
import matplotlib.pyplot as plt

# Function to generate synthetic data
def generate_data(n_samples=200):
    np.random.seed(0)
    X = np.random.randn(n_samples, 2)
    Y = (X[:, 0] * X[:, 1] > 0).astype(int).reshape(-1, 1)
    return X, Y

# Activation functions and their derivatives
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(a):
    return a * (1 - a)

def relu(z):
    return np.maximum(0, z)

def relu_derivative(a):
    return (a > 0).astype(float)

# Function to initialize parameters
def initialize_parameters(n_x, n_h, n_y):
    np.random.seed(1)
    W1 = np.random.randn(n_x, n_h) * 0.01
    b1 = np.zeros((1, n_h))
    W2 = np.random.randn(n_h, n_y) * 0.01
    b2 = np.zeros((1, n_y))
    return W1, b1, W2, b2

# Forward propagation function
def forward_propagation(X, W1, b1, W2, b2):
    Z1 = np.dot(X, W1) + b1
    A1 = relu(Z1)
    Z2 = np.dot(A1, W2) + b2
    A2 = sigmoid(Z2)
    cache = (Z1, A1, W1, b1, Z2, A2, W2, b2)
    return A2, cache

# Cost computation function
def compute_cost(A2, Y):
    m = Y.shape[0]
    cost = - (1/m) * np.sum(Y * np.log(A2 + 1e-8) + (1 - Y) * np.log(1 - A2 + 1e-8))
    return cost

# Backward propagation function
def backward_propagation(X, Y, cache):
    Z1, A1, W1, b1, Z2, A2, W2, b2 = cache
    m = X.shape[0]

    dZ2 = A2 - Y
    dW2 = (1/m) * np.dot(A1.T, dZ2)
    db2 = (1/m) * np.sum(dZ2, axis=0, keepdims=True)

    dA1 = np.dot(dZ2, W2.T)
    dZ1 = dA1 * relu_derivative(A1)
    dW1 = (1/m) * np.dot(X.T, dZ1)
    db1 = (1/m) * np.sum(dZ1, axis=0)

    grads = (dW1, db1, dW2, db2)
    return grads

# Parameter update function
def update_parameters(W1, b1, W2, b2, grads, learning_rate):
    dW1, db1, dW2, db2 = grads
    W1 -= learning_rate * dW1
    b1 -= learning_rate * db1
    W2 -= learning_rate * dW2
    b2 -= learning_rate * db2
    return W1, b1, W2, b2

# Model training function
def model(X, Y, n_h, num_iterations=10000, learning_rate=1.2, print_cost=False):
    n_x = X.shape[1]
    n_y = Y.shape[1]
    W1, b1, W2, b2 = initialize_parameters(n_x, n_h, n_y)

    for i in range(num_iterations):
        A2, cache = forward_propagation(X, W1, b1, W2, b2)
        cost = compute_cost(A2, Y)
        grads = backward_propagation(X, Y, cache)
        W1, b1, W2, b2 = update_parameters(W1, b1, W2, b2, grads, learning_rate)

        if print_cost and i % 1000 == 0:
            print(f"Cost after iteration {i}: {cost}")

    parameters = (W1, b1, W2, b2)
    return parameters

# Prediction function
def predict(X, parameters):
    W1, b1, W2, b2 = parameters
    A2, _ = forward_propagation(X, W1, b1, W2, b2)
    predictions = (A2 > 0.5).astype(int)
    return predictions

# Function to plot the data
def plot_data(X, Y):
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=Y.ravel(), cmap=plt.cm.Spectral, edgecolors='k')
    plt.title("Data Visualization")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.show()

# Function to plot the decision boundary
def plot_decision_boundary(model_func, X, Y):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:,1].min() -1, X[:,1].max() +1
    h = 0.01
    xx, yy = np.meshgrid(np.arange(x_min,x_max,h), np.arange(y_min,y_max,h))
    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = model_func(grid)
    Z = Z.reshape(xx.shape)
    plt.figure(figsize=(8,6))
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral, alpha=0.8)
    plt.scatter(X[:,0], X[:,1], c=Y.ravel(), cmap=plt.cm.Spectral, edgecolors='k')
    plt.title("Decision Boundary")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.show()

# Main execution
if __name__ == "__main__":
    X, Y = generate_data()
    plot_data(X, Y)  # Plot the data before training

    parameters = model(X, Y, n_h=4, num_iterations=10000, learning_rate=1.2, print_cost=True)
    predictions = predict(X, parameters)
    accuracy = np.mean(predictions == Y) * 100
    print(f'Accuracy: {accuracy}%')

    # Plot the decision boundary after training
    plot_decision_boundary(lambda x: predict(x, parameters), X, Y)
