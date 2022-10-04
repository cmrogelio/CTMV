from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


 
# Get current size
fig_size = plt.rcParams["figure.figsize"]
 
# Prints: [8.0, 6.0]
print "Current size:", fig_size
 
# Set figure width to 12 and height to 9
fig_size[0] = 12
fig_size[1] = 9
plt.rcParams["figure.figsize"] = fig_size



d=[1,2,3,4,5,6,7,8,9]

# Create a Figure
fig = plt.figure()

# Set up Axes
ax = fig.add_subplot(111)

ax.grid(b=1,axis='both', color='k')

pp = PdfPages('prueba.pdf')

# Scatter the data
ax.plot(d, color='lightblue', linewidth=3)
#ax.scatter(np.linspace(0, 1, 5), np.linspace(0, 5, 5))
ax.set(title="prueba", xlabel="x1")

# save plot
#plt.savefig("prueba.png")

# save plot pdf
#pp.savefig()


#pp.close()

# Show the plot
plt.show()


