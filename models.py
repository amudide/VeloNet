'''
Model architecture for LagNet:
	A: adjacency matrix (N x N)
	X: expression matrix (N x g)
	L: number of lags to look back
	K: number of layers in the model
	d: number of nodes in hidden layers
'''

import torch
import torch.nn as nn
import torch.nn.functional as F

class LagNet(nn.Module):
	def __init__(self,A,X,L,K,d,final_activation=None):
		super(LagNet, self).__init__()

		self.A = A
		self.X = X
		self.L = L
		self.K = K
		self.d = d
		self.final_activation = final_activation

		self.N = self.X.size(dim=0)
		self.g = self.X.size(dim=1)

		cur = torch.clone(self.X)
		for i in range(1, self.L + 1):
			cur = torch.matmul(self.A.t(), cur)
			setattr(self,'ax{}'.format(i),cur)

		for i in range(1, self.L + 1):
			setattr(self,'fc1_{}'.format(i),nn.Linear(self.g, self.d))
		
		for i in range(2, self.K):
			setattr(self,'fc{}'.format(i),nn.Linear(self.d, self.d))

		setattr(self,'fc{}'.format(self.K),nn.Linear(self.d, 1))


	def forward(self):

		ret = 0

		#print(f'The size of A*X should be {self.N}x{self.g} and it is: {self.ax1.size()}')

		for i in range(1, self.L + 1):
			ret = ret + getattr(self,'fc1_{}'.format(i))(getattr(self,'ax{}'.format(i)))
		ret = F.relu(ret)

		#print(f'The size of h(1) should be {self.N}x{self.d} and it is: {ret.size()}')

		for i in range(2, self.K):
			ret = getattr(self,'fc{}'.format(i))(ret)
			ret = F.relu(ret)

		#print(f'The size of h(K-1) should be {self.N}x{self.d} and it is: {ret.size()}')

		ret = getattr(self,'fc{}'.format(self.K))(ret)

		#print(f'The size of h(K) should be {self.N}x{1} and it is: {ret.size()}')

		if self.final_activation == 'exp':
			ret = torch.exp(ret)

		#print(f'The size of h(K) should be {self.N}x{1} and it is: {ret.size()}')

		return ret

'''
A = torch.tensor([[0, 1, 0, 0],
				  [0, 0, 1, 0],
				  [0, 0, 0, 1],
				  [0, 0, 0, 0]])

X = torch.tensor([[4, 5],
				  [1, 2],
				  [0, 3],
				  [7, 10]])

model = LagNet(A, X, L=6, K=4, d=10, final_activation='exp')

print(model)

print(model())
'''