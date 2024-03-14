from matplotlib import pyplot as plt
from fpdf import FPDF

# Step 1: Generate Line Graphs with Matplotlib
def create_line_graph(x_data, y_data, title, ylabel, filename):
    plt.figure()
    plt.plot(x_data, y_data)
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

# Example data
years = [2010, 2011, 2012, 2013, 2014, 2015]
amounts = [1000, 1500, 1200, 1800, 1300, 1700]

# Create two line graphs
create_line_graph(years, amounts, 'Sales Over Years', 'Amount ($)', 'graph1.png')
create_line_graph(years, [x*0.8 for x in amounts], 'Projected Sales', 'Amount ($)', 'graph2.png')

# Step 2 & 3: Create a PDF and Insert the Graphs
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.image('graph1.png', x=10, y=8, w=180)
pdf.image('graph2.png', x=10, y=148, w=180)
pdf.output('line_graphs.pdf')
