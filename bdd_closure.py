from pyeda.inter import *

def calculate_R_edges():
	R = set([])
	for i in range (32):
		for j in range (32):
			if ((i+3)%32 == j%32) or ((i+8)%32 == j%32):
				R.add((i,j))
	return R

def convert_to_binary(num_set):
	binary_set = set([])
	for num in num_set:
		binary_set.add(f'{num:05b}')
	return binary_set
	
def convert_R_to_binary(R_bin):
	binary_set = set([])
	for tup in R_bin:
		binary_set.add(f'{tup[0]:05b}'+f'{tup[1]:05b}')
	return binary_set

def convert_R_to_expression(R):
	R_e = set([])

	for edge in R:
		temp = ""
		for num in range(10):
			if num < 5:
				if edge[num] == "0":
					temp += "~"
				temp += "x[" + str(num) + "] & "
			elif num < 9:
				if edge[num] == "0":
					temp += "~"
				temp += "y[" + str(num-5) + "] & "
			else:
				if edge[num] == "0":
					temp += "~"
				temp += "y[" + str(num-5) + "]"
		R_e.add(temp)
	return R_e

def convert_to_expression(xy, binary):
	exp = set([])

	for edge in binary:
		temp = ""
		for num in range(5):
			if edge[num] == "0":
				temp += "~"
			temp += xy + "[" + str(num) + "] & "
		exp.add(temp[:-3])
	return exp

def convert_to_bdd(exp):
	exp_s = ""
	for e in exp:
		exp_s += e + " | "
	exp_s = exp_s[:-3]
	exp_e = expr(exp_s)
	return expr2bdd(exp_e)

def compose(g1, g2):
	x = bddvars('x', 5)
	y = bddvars('y', 5)
	z = bddvars('z', 5)
	
	g1 = g1.compose({x[0]:z[0], x[1]:z[1], x[2]:z[2], x[3]:z[3], x[4]:z[4]})
	g2 = g2.compose({y[0]:z[0], y[1]:z[1], y[2]:z[2], y[3]:z[3], y[4]:z[4]})
	return (g1 & g2).smoothing(z)

###Sets given
even = set([0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30])
prime = set([3,5,7,11,13,17,19,23,29,31])
R = calculate_R_edges()
print("Calculated R edges...")

### This section is for converting everything to binary strings
R_b = convert_R_to_binary(R)
even_b = convert_to_binary(even)
prime_b = convert_to_binary(prime)
print("Converted even set, prime set, and R edges to binary...")

### This section is for converting everything to expressions
R_e = convert_R_to_expression(R_b)
even_e = convert_to_expression('y', even_b)
prime_e = convert_to_expression('x', prime_b)
print("Converted even binary, prime binary, and R binary to binary expressions...")

### This section is for converting everything to bdds
R_bdd = convert_to_bdd(R_e)
even_bdd = convert_to_bdd(even_e)
prime_bdd = convert_to_bdd(prime_e)
print("Converted even expressions, prime expressions, and R to bdd...")

### This section composes Rs bdd with itself to make RR (R_2)
R_2 = compose(R_bdd, R_bdd)
print("Composed R with itself...")

### This section is for transitive closure of R_2
H_1 = R_2
H_2 = None
while H_1 is not H_2:
	H_2 = H_1
	H_1 = H_1 | compose(H_1, R_2)
R_2 = H_1
print("Performed transitive closure on R_2...")



### This is for checking that u node can reach v node in even number of steps
x = bddvars('x', 5)
y = bddvars('y', 5)

J = (R_2 & even_bdd).smoothing(y)
Q = ~(~(J | ~prime_bdd)).smoothing(x)

print("For each prime node u is there a node v such that u can reach v in an even number of steps?")
print(Q.is_one())

