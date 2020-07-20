import tkinter as tk
import customize as c
import numpy.random as random


class MatChainMul(tk.Frame):

    def __init__(self, dimension, matrices, transition_time):
        tk.Frame.__init__(self)
        self.dims = dimension
        self.matrices = matrices
        self.transition_time = transition_time
        n = len(self.dims)
        self.c = [[0 for x in range(n)] for y in range(n)]
        self.grid()
        self.master.title('Matrix Chain Multiplication -Dynamic Programming')
        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=2, width=1000, height=500)
        self.main_grid.grid(pady=(130, 4))
        self.cells = []
        self.make_grid()
        self.cost = 0
        self.seq = []
        for j in range(n-1):
            self.seq.append(chr(65 + j))
        self.last = self.seq[-1]
        self.matrix_chain_multiplication()
        self.mainloop()

    def make_grid(self):

        for i in range(len(self.dims)):
            row = []
            for j in range(len(self.dims)):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=75,
                    height=65)
                cell_frame.grid(row=i, column=j, padx=2, pady=2)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        cost_frame = tk.Frame(self)
        cost_frame.place(relx=0.5, y=20, anchor="center")
        self.cost_label = tk.Label(cost_frame, text="", font=c.VALUE_FONT)
        self.cost_label.grid(row=0)

        eqn_frame = tk.Frame(self)
        eqn_frame.place(x=5, y=80, anchor="w")
        self.eqn_label = tk.Label(eqn_frame, text="", font=c.LABEL_FONT)
        self.eqn_label.grid(row=0)
        self.k_label = tk.Label(eqn_frame, text="", font=c.LABEL_FONT)
        self.k_label.grid(row=1)
        self.order_label = tk.Label(eqn_frame, text="", font=c.VALUE_FONT)
        self.order_label.grid(row=2)

    def matrix_chain_multiplication(self):

        n = len(self.dims)
        k_values = set()
        # assigning the row and column headers
        for i in range(n):
            for j in range(n):
                if i == 0 and j > 0:
                    self.c[i][j] = j
                if j == 0 and i > 0:
                    self.c[i][j] = i
        self.update_gui()
        # main logic for finding the minimum costs for sub-problems
        for length in range(2, n):
            for i in range(1, n - length + 1):
                j = i + length - 1
                self.c[i][j] = float('inf')
                for k in range(i, j):
                    self.cost = self.c[i][k] + self.c[k + 1][j] + self.dims[i - 1] * self.dims[k] * self.dims[j]
                    if self.cost < self.c[i][j]:
                        self.c[i][j] = self.cost
                        best_k = k
                        self.eqn_label.configure(text="c[{},{}] = min (c[{},k] + c[(k+1),{}] + {} x dim(k) x {}) , {}≤k<{}".format(i, j, i, j, self.dims[i-1], self.dims[j], i, j))
                # Storing the optimal value of k for c[i][j], in the cell c[j][i]
                self.c[j][i] = best_k
                if i == 1:
                    k_values.add(best_k)
                self.k_label.configure(text="Optimal value of k = {} for c[{},{}] -> stored in c[{},{}]".format(best_k, i, j, j, i))
                self.update_gui()
        for K in k_values:
            self.parenthesize(K)
        self.cost_label.configure(text="Minimum Cost = {}".format(self.c[1][n - 1]))
        print("Minimum Cost: ", self.c[1][n - 1])
        sequence = ' '.join([str(elem) for elem in self.seq])
        self.order_label.configure(text="Optimal Order = {}".format(sequence))
        print("Optimal Order of multiplication: ", sequence)
        # self.matrix_multiply(self.seq)
        # product = eval(sequence, self.matrices)
        # print("Final Product =\n", product)
        return self.c[1][n - 1]

    def parenthesize(self, k):

        self.seq.insert(0, '(')
        q = 0
        for p in self.seq:
            if p != "(" and p != ")":
                q += 1
                if q == k and p != self.last:
                    self.seq.insert(self.seq.index(p)+1, ")")
                    self.seq.insert(self.seq.index(p)+2, "(")
                    break
        self.seq.append(')')
    '''
    def matrix_multiply(self, tokens):

        values = []
        ops = []
        result = {}
        i, j = 0, 0
        while i < len(tokens):
            if tokens[i] == ' ':
                i += 1
                continue
            elif tokens[i] == '(':
                ops.append(tokens[i])
            elif tokens[i] == ')':
                mat1 = values.pop()
                if type(mat1) == 'str' and mat1 < chr(80):
                    mat1 = self.matrices.get(mat1)
                elif mat1 >= chr(80):
                    mat1 = result.get(mat1)
                mat2 = values.pop()
                if type(mat2) == 'str' and mat2 < chr(80):
                    mat2 = self.matrices.get(mat2)
                elif mat2 >= chr(80):
                    mat2 = result.get(mat2)
                mat3 = int(mat1) * int(mat2)
                result.update({chr(80 + j): mat3})
                values.append(chr(80 + j))
                j += 1
                print("{} x {} = {}".format(mat1, mat2, mat3))
            else:
                values.append(tokens[i])
            i += 1
    '''
    def update_gui(self):

        self.after(self.transition_time)
        n = len(self.dims)
        for i in range(0, n):
            for j in range(0, n):
                cell_value = self.c[i][j]
                if i == 0 and j == 0:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[3])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[3],
                        fg=c.CELL_NUMBER_COLORS[2],
                        font=c.CELL_NUMBER_FONTS[2],
                        text="k \\ C")
                elif i == j:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=c.EMPTY_CELL_COLOR,
                        fg=c.CELL_NUMBER_COLORS[1],
                        font=c.CELL_NUMBER_FONTS[1],
                        text="0")
                elif i == 0 or j == 0:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[2])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[2],
                        fg=c.CELL_NUMBER_COLORS[2],
                        font=c.CELL_NUMBER_FONTS[1],
                        text=str(cell_value))
                    continue
                elif cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(
                        bg=c.EMPTY_CELL_COLOR,
                        fg=c.CELL_NUMBER_COLORS[1],
                        font=c.CELL_NUMBER_FONTS[1],
                        text="")
                else:
                    self.cells[i][j]["frame"].configure(
                        bg=c.CELL_COLORS[1])
                    self.cells[i][j]["number"].configure(
                        bg=c.CELL_COLORS[1],
                        fg=c.CELL_NUMBER_COLORS[1],
                        font=c.CELL_NUMBER_FONTS[1],
                        text=str(cell_value))
        self.update()


# Driver code
file = open('Input.txt', 'r')
dims = []
while 1:
    dim = file.read(1)
    if not dim:
        break
    if dim != ' ':
        dims.append(dim)

for i in range(len(dims)):
    dims[i] = int(dims[i])
print("Dimensions = ", dims)

chain = {}
random.seed(4)
i = 0
while True:
    m = dims[i]
    n = dims[i+1]
    chain.update({chr(65 + i): random.randint(10, size=(m, n))})
    i += 1
    if i == len(dims)-1:
        break

print("The Matrices are:")
for name, matrix in chain.items():
    print(name, " =\n", matrix)

# transition_time is to given in milliseconds (for adjusting speed of animation)
MatChainMul(dimension=dims, matrices=chain, transition_time=2000)
