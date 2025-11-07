import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from IPython.display import display

cake = pd.read_csv("cake.csv")

def runplt():   
    plt.figure()
    plt.title("cake price plotted against size")
    plt.xlabel("size")
    plt.ylabel("price")
    plt.grid(True)
    plt.xlim(0, 20)
    plt.ylim(0, 110)
    return plt

x = cake.loc[:, "size"].values
y = cake.loc[:, "price"].values
plt = runplt()
plt.plot(x, y, "b*")
plt.show()

model = LinearRegression()
X = x.reshape((-1, 1))
Y = y
model.fit(X, Y)
display(model.intercept_)
display(model.coef_)

X2 = [[0],[16],[20],[25]]
Y2 = model.predict(X2)
plt = runplt()
plt.plot(X, Y, "k.")
plt.plot(X2, Y2, "b-")
plt.show()