from tkinter import *
import scipy.constants as const
import math

# Create input window

root = Tk()
root.title('Расчет параметров ЭРД')

power = Label(root, text='Мощность двигателя: ')
power.grid(row=0, column=0)
ePower = Entry(root)
ePower.grid(row=0, column=1)
ePower.insert(0, '1350')
vt = Label(root, text='Вт')
vt.grid(row=0, column=2)

thrust = Label(root, text='Тяга двигателя: ')
thrust.grid(row=1, column=0)
eThrust = Entry(root)
eThrust.grid(row=1, column=1)
eThrust.insert(0, '8')
vr = StringVar()
vr.set('г')
measure = OptionMenu(root, vr, 'г', 'мН')
measure.grid(row=1, column=2)


fuel = Label(root, text='Рабочее тело: ')
fuel.grid(row=2, column=0)
propellant = StringVar()
propellant.set('Xe')
rt = OptionMenu(root, propellant, 'Xe', 'Ar', 'Bi', 'Kr', 'I')
rt.grid(row=2, column=1)

res = Label(root)
result = Label(root)
rasm = Label(root)
wrong = Label(root)


# CONST

mp = const.proton_mass
e = const.e
me = const.electron_mass
g = const.g
mu0 = 4 * const.pi * 10 ** (-7)


# Additional data
delta = 2
kpot = 2
B = 0.03
Bmax = 2
jkat = 1.5
Ik = 1


def reformat(num):
    if 10000 > num > 0.01:
        return round(num, 2)
    else:
        return format(num, '.2e')


def diam(m):
    return 0.00195 * m**3 - 0.267035 * m**2 + 13.149984 * m + 20.49869


def y(m):
    return 1.176*10**-9 * m**4 - 7.995457*10**-7*m**3 + 1.736478*10**-4*m**2 - 9.85489 * 10**-3*m + 0.3865574


def solve():
    global res
    global result
    global rasm
    global wrong
    res.destroy()
    result.destroy()
    rasm.destroy()
    wrong.destroy()

    # Get variables
    if vr.get() == 'мН':
        F = float(eThrust.get()) / 1000
    else:
        F = float(eThrust.get()) * g / 1000

    if propellant.get() == 'Xe':
        prop_atom_mass = 131
        prop_fi = 12.13
    elif propellant.get() == 'Ar':
        prop_atom_mass = 40
        prop_fi = 15.76
    elif propellant.get() == 'Bi':
        prop_atom_mass = 209
        prop_fi = 7.29
    elif propellant.get() == 'Kr':
        prop_atom_mass = 84
        prop_fi = 14
    else:
        prop_atom_mass = 127
        prop_fi = 10.45
    N = float(ePower.get())
    M = prop_atom_mass * mp

    # Solve
    a = 3.7 * prop_fi * e / M
    b = - N / 1.25
    c = F ** 2 / (2 * 0.835 ** 2)
    D = b ** 2 - 4 * a * c
    if D < 0:
        wrong = Label(root, text='Невозможно рассчитать')
        wrong.grid(row=5, column=0)
        root.mainloop()
    else:
        m = (-b - math.sqrt(D))/(2 * a)
        f_eff = F ** 2 / (2 * N * m) * 100
        Iud = F / (m * g)
        Vi = g * Iud / 0.835
        Ur = M * Vi ** 2 / (2 * e)
        Ir = e * m * 1.25 / M
        Dsr = diam(m*10**6)
        w = y(m*10**6)
        Sk = N/w
        bk = Sk/(const.pi * Dsr)
        Dvn = Dsr + bk
        lk = 2 * bk
        st = 0.5 * bk

        # Print solution
        res_label = Label(root, text='Результаты расчётов')
        res_label.grid(row=4, column=1)

        space = Label(root, text='\n')
        space.grid(row=5, column=3)

        res = Label(root, text="""Массовый расход: \n
        Тяговый КПД: \n
        Удельный импульс: \n
        Разрядное напряжение: \n
        Разрядный ток: \n
        Средний диаметр: \n
        Ширина канала: \n
        Внешний диаметр канала: \n
        Длина канала: \n
        Толщина стенки канала: 
        """)
        res.grid(row=6, column=0)

        result = Label(root, text =
        '{} \n \n {} \n \n{} \n \n {} \n \n {} \n \n {} \n \n {} \n \n {} \n \n {} \n \n {}\n'.format(
                                                                             reformat(m*10**6),
                                                                             round(f_eff, 1),
                                                                             round(Iud),
                                                                             round(Ur),
                                                                             reformat(Ir),
                                                                             round(Dsr),
                                                                             round(bk),
                                                                             round(Dvn),
                                                                             round(lk), round(st)))
        result.grid(row=6, column=1)

        rasm = Label(root, text="""        мг/c \n
            % \n
            сек \n
            В \n
            А \n
            мм \n
            мм \n
            мм \n
            мм \n
            мм 
                """)
        rasm.grid(row=6, column=2)

        root.mainloop()


myButton = Button(root, text='Рассчитать', command=solve)
myButton.grid(row=3, column=0)

root.mainloop()


def main():
    pass
