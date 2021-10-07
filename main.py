from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy import stats

nEntry = 0
# Lists of entry widgets
xEntry = []
xerrorEntry = []
yEntry = []
yerrorEntry = []

# Data will be stored in and graphed from these lists
x = []
y = []
xerror = []
yerror = []

# Graph Appearance
options = Tk()
options.withdraw()
options.title("Graph Properties")
# things used for checkboxes im not even sure what they do
v1 = IntVar()
v2 = IntVar()
v3 = IntVar()
# entry widgets for graphing options
o21 = Entry(options)
o22 = Entry(options)
o23 = Entry(options)
o24 = Entry(options)
o25 = Entry(options)
o26 = Entry(options)
o27 = Entry(options)
o28 = Entry(options)

# a list used to store linear regression information
# [equation, Rsquared, gradient-uncertainty]
info = []
# uncertainty of gradient stuff

b = [[0, 0], [0, 0]]
s = [[0, 0], [0, 0]]


def on_click1():
    global nEntry
    nEntry = int(e1.get())

    dataEntry = Tk()
    dataEntry.title("Data Entry")

    xLab = Label(dataEntry, text="x")
    xerrorLab = Label(dataEntry, text="x uncertainty")
    yLab = Label(dataEntry, text="y")
    yerrorLab = Label(dataEntry, text="y uncertainty")
    xLab.grid(row=0, column=1)
    xerrorLab.grid(row=0, column=2)
    yLab.grid(row=0, column=3)
    yerrorLab.grid(row=0, column=4)

    for i in range(nEntry):
        e = Entry(dataEntry)
        e.grid(row=i + 1, column=1)
        xEntry.append(e)
    for i in range(nEntry):
        e = Entry(dataEntry)
        e.grid(row=i + 1, column=2)
        xerrorEntry.append(e)
    for i in range(nEntry):
        e = Entry(dataEntry)
        e.grid(row=i + 1, column=3)
        yEntry.append(e)
    for i in range(nEntry):
        e = Entry(dataEntry)
        e.grid(row=i + 1, column=4)
        yerrorEntry.append(e)

    # button for graph options
    submitData = Button(dataEntry, text="Submit Data", command=on_click2)
    submitData.grid(row=nEntry + 2, column=4)

    dataEntry.mainloop()


def on_click2():

    options.deiconify()
    # button that displays the plot
    plot_button = Button(options, command=plot, height=2, width=10, text="Plot")
    plot_button.grid(row=0, column=1)

    # SUBHEADING 1 - WHAT TO SHOW ================================
    sh1 = Label(options, text="Graph Information")
    sh1.grid(row=1, column=0)

    # trend-line
    l1 = Label(options, text="Show line of best fit")
    l1.grid(row=11, column=1)
    o1 = Checkbutton(options, variable=v1, onvalue=1, offvalue=0)
    o1.grid(row=11, column=2)

    # lines of worst fit
    l2 = Label(options, text="Show lines of worst fit")
    l2.grid(row=12, column=1)
    o2 = Checkbutton(options, variable=v2, onvalue=1, offvalue=0)
    o2.grid(row=12, column=2)

    # show error bars
    l3 = Label(options, text="Show error bars")
    l3.grid(row=13, column=1)
    o3 = Checkbutton(options, variable=v3, onvalue=1, offvalue=0)
    o3.grid(row=13, column=2)

    # SUBHEADING 2 - GRAPH APPEARANCE =============================
    sh2 = Label(options, text="Graph Appearance")
    sh2.grid(row=100, column=0)

    # markercolour
    l21 = Label(options, text="Marker Colour")
    l21.grid(row=101, column=1)
    o21.grid(row=101, column=2)
    o21.insert(0, "#000000")

    # markershape
    l22 = Label(options, text="Marker Shape")
    l22.grid(row=102, column=1)
    o22.grid(row=102, column=2)
    o22.insert(0, "x")

    # errorbar colour
    l23 = Label(options, text="Error-bar Colour")
    l23.grid(row=103, column=1)
    o23.grid(row=103, column=2)
    o23.insert(0, "#000000")

    # errorbar cap size
    l24 = Label(options, text="Error-bar Cap Size")
    l24.grid(row=104, column=1)
    o24.grid(row=104, column=2)
    o24.insert(0, "2")

    # trendline colour
    l25 = Label(options, text="Trendline Colour")
    l25.grid(row=105, column=1)
    o25.grid(row=105, column=2)
    o25.insert(0, "#000000")

    # trendline style
    l26 = Label(options, text="Trendline Style")
    l26.grid(row=106, column=1)
    o26.grid(row=106, column=2)
    o26.insert(0, "-")

    # worstfit colour
    l27 = Label(options, text="Worst-fit-lines Colour")
    l27.grid(row=107, column=1)
    o27.grid(row=107, column=2)
    o27.insert(0, "#000000")

    # worstfit style
    l28 = Label(options, text="Worst-fit-lines Style")
    l28.grid(row=108, column=1)
    o28.grid(row=108, column=2)
    o28.insert(0, "--")

    options.mainloop()


def plot():
    window = Tk()
    window.title('Graph')
    fig = Figure(figsize=(5, 5), dpi=100)

    # EXTRACT THE X AND Y FROM THE TABLE AND STUFF
    x = []
    y = []
    xerror = []
    yerror = []
    for en in xEntry:
        x.append(float(en.get()))
    for en in yEntry:
        y.append(float(en.get()))

    for en in xerrorEntry:
        xerror.append(float(en.get()))
    for en in yerrorEntry:
        yerror.append(float(en.get()))

    # calculate gradient uncertainty (original algorithm)
    # assuming that the x data points are sorted
    ymax = []
    ymin = []
    for i in range(nEntry):
        ymax.append(y[i] + yerror[i])
    for i in range(nEntry):
        ymin.append(y[i] - yerror[i])

    global b
    global s
    # line of maximum gradient
    b = [[x[0], ymin[0]], [x[nEntry - 1], ymax[nEntry - 1]]]
    # shift the left side anchor first
    for i in range(nEntry):
        if (b[1][1] - b[0][1]) / (b[1][0] - b[0][0]) * (x[i] - b[0][0]) + b[0][1] < ymin[i]:
            b[0] = [x[i], ymin[i]]
    # shift the right anchor
    for i in range(nEntry):
        i = nEntry - 1 - i
        if b[0][0] == b[1][0]:
            break
        if (b[1][1] - b[0][1]) / (b[1][0] - b[0][0]) * (x[i] - b[0][0]) + b[0][1] > ymax[i]:
            b[1] = [x[i], ymax[i]]

    # line of minimum gradient
    s = [[x[0], ymax[0]], [x[nEntry - 1], ymin[nEntry - 1]]]
    # shift the right side anchor first
    for i in range(nEntry):
        i = nEntry - 1 - i
        if (s[1][1] - s[0][1]) / (s[1][0] - s[0][0]) * (x[i] - s[0][0]) + s[0][1] < ymin[i]:
            s[1] = [x[i], ymin[i]]
    # shift the left side anchor
    for i in range(nEntry):
        if s[0][0] == s[1][0]:
            break
        if (s[1][1] - s[0][1]) / (s[1][0] - s[0][0]) * (x[i] - s[0][0]) + s[0][1] > ymax[i]:
            s[0] = [x[i], ymax[i]]

    lowline = []
    highline = []
    for i in x:
        highline.append((b[1][1] - b[0][1]) / (b[1][0] - b[0][0]) * (i - b[0][0]) + b[0][1])
    for i in x:
        lowline.append((s[1][1] - s[0][1]) / (s[1][0] - s[0][0]) * (i - s[0][0]) + s[0][1])

    # CONSTRUCT THE PLOT USING THE OPTIONS ==============================
    plot1 = fig.add_subplot(111)
    plot1.plot(x, y, marker=o22.get(), markeredgecolor=o21.get(), markerfacecolor=o21.get(), linewidth=0)
    result = stats.linregress(x, y)

    # making errorbars
    if v3.get() == 1:
        plot1.errorbar(x, y, xerr=xerror, yerr=yerror, fmt=' ', ecolor=o23.get(), capsize=int(o24.get()))

    # drawing trendline
    if v1.get() == 1:
        plot1.plot(x, [result[0]*e+result[1] for e in x], "-", color=o25.get())

    # drawing lines of worst fit
    if v2.get() == 1:
        plot1.plot(x, highline, o28.get(), color=o27.get())
        plot1.plot(x, lowline, o28.get(), color=o27.get())

    # graph information
    # this is the worst code i have ever written i have no idea what is going on
    info.append("y = " + str(result[0]) + "x + " + str(result[1]))  # equation
    info.append(str(result[2] ** 2))  # rsquared
    info.append("fuck you")  # gradient uncertainty

    infoButton = Button(window, text="Graph Information", command=info_window)
    infoButton.pack()

    # other weird stuff
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
    canvas.get_tk_widget().pack()
    window.mainloop()


def info_window():
    infoW = Tk()
    infoW.title("Graph Information")
    # equation
    eqnL = Label(infoW, text="equation: ")
    eqnL.grid(row=1, column=0)
    eqntext = Label(infoW, text=info[0])
    eqntext.grid(row=1, column=1)

    # R squared Value
    rSqL = Label(infoW, text="R squared: ")
    rSqL.grid(row=2, column=0)
    rsqtext = Label(infoW, text=info[1])
    rsqtext.grid(row=2, column=1)

    # gradient uncertainty
    grUL = Label(infoW, text="Uncertainty in gradient: ")
    grUL.grid(row=3, column=0)
    grUText = Label(infoW, text=str(((b[1][1]-b[0][1])/(b[1][0]-b[0][0])-(s[1][1]-s[0][1])/(s[0][1]-s[0][0]))/2))
    grUText.grid(row=3, column=1)

    infoW.mainloop()


# the main Tkinter window
root = Tk()
root.title('Logger Bro')
root.geometry("500x50")

text1 = Label(root, text="Enter the number of entries:")
text1.grid(row=0, column=0)

e1 = Entry(root)
e1.grid(row=0, column=1)
e1.insert(0, "5")

submit = Button(root, text="Submit", command=on_click1)
submit.grid(row=0, column=2)

root.mainloop()
