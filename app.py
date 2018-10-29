
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy
import tkinter as tk
from tkinter import ttk, Tk

LARGE_FONT = ("Verdana", 12)

class Computations:

    # function - y*y/(x*x) - 2
    def f(x, y):
        return y * y / (x * x) - 2

    # exact solution
    def exact(x):
        return x * (-1 + 3 / (1 + 0.5 * x ** 3))

    # Euler Method
    def euler(x, y, h, X):
        while x < X:
            y = y + h * Computations.f(x, y)
            x = x + h

        return y

    # Improved Euler Method
    def euler_imp(x, y, h, X):

        while x < X:
            temp = y + h * Computations.f(x, y)
            y = y + h / 2 * (Computations.f(x, y) + Computations.f(x + h, temp))
            x = x + h

        return y

    # Runge-Kutta Method
    def runge_kutta(x, y, h, X):
        n = (int)((X - x) / h)
        for i in range(1, n + 1):
            k1 = h * Computations.f(x, y)
            k2 = h * Computations.f(x + 0.5 * h, y + 0.5 * k1)
            k3 = h * Computations.f(x + 0.5 * h, y + 0.5 * k2)
            k4 = h * Computations.f(x + h, y + k3)

            y = y + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

            x = x + h
        return y

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Solutions of DE")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        frame = Page(container, self)

        self.frames[Page] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Page)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Initial values", font=LARGE_FONT).place(x = 15, y = 5)

        tk.Label(self, text="X0", font=LARGE_FONT).place(x = 15, y = 40)
        entry_x0 = tk.Entry(self)
        entry_x0.place(x =60 , y = 40)
        entry_x0.insert(0, "1")

        tk.Label(self, text="Y0", font=LARGE_FONT).place(x = 15, y = 80)
        entry_y0 = tk.Entry(self)
        entry_y0.place(x = 60, y = 80)
        entry_y0.insert(0, "1")

        tk.Label(self, text="X", font=LARGE_FONT).place(x = 20, y = 120)
        entry_xf = tk.Entry(self)
        entry_xf.place(x = 60, y = 120)
        entry_xf.insert(0, "10.3")

        tk.Label(self, text="Number of steps", font=LARGE_FONT).place(x = 5, y = 150)
        entry_n = tk.Entry(self)
        entry_n.place(x = 60, y = 180)
        entry_n.insert(0, "21")

        def draw_plots():
            f = Figure(figsize=(7.5, 7.5), dpi=100)

            x0 = float(entry_x0.get())
            y0 = float(entry_y0.get())
            xf = float(entry_xf.get())
            n = int(entry_n.get())

            h = (xf - x0) / (n - 1)

            x = numpy.linspace(x0, xf, n)
            y1 = numpy.zeros([n])
            y2 = numpy.zeros([n])
            y3 = numpy.zeros([n])
            y4 = numpy.zeros([n])
            y1[0] = y0
            y2[0] = y0
            y3[0] = y0
            y4[0] = y0
            for i in range(1, n):
                y1[i] = Computations.euler(x0, y0, h, x[i])
                y2[i] = Computations.euler_imp(x0, y0, h, x[i])
                y3[i] = Computations.runge_kutta(x0, y0, h, x[i])
                y4[i] = Computations.exact(x[i])

            x_limit = (x0 - 1, xf + 1)
            y_limit = (min(y1[n - 1], y2[n - 1], y3[n - 1], y4[n - 1]) - 1, y0 + 1)

            ax1 = f.add_axes([0.1, 0.55, 0.8, 0.35], xlim=(x_limit[0], x_limit[1]), ylim=(y_limit[0], y_limit[1]),
                             title="Solutions of DE y' = " r"$\frac{y^2}{x^2}$ - 2")
            ax1.plot(x, y1, ':', linewidth=2.0)
            ax1.plot(x, y2, ':')
            ax1.plot(x, y3, ':', linewidth=2.0)
            ax1.plot(x, y4, linewidth=1.0)

            f.legend(("Euler Method", "Improved Euler Method", "Runge-Kutta Method", "Exact solution of IVP"))

            ax2 = f.add_axes([0.1, 0.1, 0.8, 0.35], xlim=(0, n), ylim=(-1, 1), title="Errors")
            er1 = numpy.zeros([n])
            er2 = numpy.zeros([n])
            er3 = numpy.zeros([n])
            step = numpy.zeros([n])
            for i in range(0, n):
                er1[i] = y4[i] - y1[i]
                er2[i] = y4[i] - y2[i]
                er3[i] = y4[i] - y3[i]
                step[i] = i

            ax2.plot(step, er1, linewidth=1.0)
            ax2.plot(step, er2, linewidth=1.0)
            ax2.plot(step, er3, linewidth=1.0)
            canvas = FigureCanvasTkAgg(f, self)

            # canvas.show()
            canvas.draw()
            canvas.get_tk_widget().place(x = 250, y = 10)

            canvas._tkcanvas.place(x = 250, y = 10)

        update_button = ttk.Button(self, text="draw plots",command=draw_plots)
        update_button.place(x = 70, y = 740)

app = App()
app.geometry("1020x780+300+300")
app.mainloop()