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
    if num < 10000 and num > 0.01:
        return round(num, 2)
    else:
        return format(num, '.2e')


def solve():

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
        wrong.grid(row=4, column=0)
        root.mainloop()
    else:
        m = (-b - math.sqrt(D))/(2 * a)
        f_eff = F ** 2 / (2 * N * m)
        Iud = F / (m * g)
        Vi = g * Iud / 0.835
        Ur = M * Vi ** 2 / (2 * e)
        Ir = e * m * 1.25 / M


        # Print solution
        res1 = Label(root, text='Массовый расход: ')
        res1.grid(row=4, column=0)
        res2 = Label(root, text='Тяговый КПД: ')
        res2.grid(row=5, column=0)
        res3 = Label(root, text='Удельный импульс: ')
        res3.grid(row=6, column=0)
        res4 = Label(root, text='Разрядное напряжение: ')
        res4.grid(row=7, column=0)
        res5 = Label(root, text='Разрядный ток: ')
        res5.grid(row=8, column=0)
        res6 = Label(root, text='Средний диаметр: ')
        res6.grid(row=9, column=0)
        res7 = Label(root, text='Ширина канала: ')
        res7.grid(row=10, column=0)
        res8 = Label(root, text='Внешний диаметр канала: ')
        res8.grid(row=11, column=0)
        res9 = Label(root, text='Длина канала: ')
        res9.grid(row=12, column=0)
        res10 = Label(root, text='Толщина стенки канала: ')
        res10.grid(row=13, column=0)

        re = Label(root, text='Результаты расчётов')
        re.grid(row=3, column=1)
        res1a = Label(root, text=reformat(m))
        res1a.grid(row=4, column=1)
        res2a = Label(root, text=reformat(f_eff))
        res2a.grid(row=5, column=1)
        res3a = Label(root, text=reformat(Iud))
        res3a.grid(row=6, column=1)
        res4a = Label(root, text=reformat(Ur))
        res4a.grid(row=7, column=1)
        res5a = Label(root, text=reformat(Ir))
        res5a.grid(row=8, column=1)
        res6a = Label(root, text='-')
        res6a.grid(row=9, column=1)
        res7a = Label(root, text='-')
        res7a.grid(row=10, column=1)
        res8a = Label(root, text='-')
        res8a.grid(row=11, column=1)
        res9a = Label(root, text='-')
        res9a.grid(row=12, column=1)
        res10a = Label(root, text='-')
        res10a.grid(row=13, column=1)
        root.mainloop()


myButton = Button(root, text='Рассчитать', command=solve)
myButton.grid(row=49, column=0)

root.mainloop()


def main():
    pass
