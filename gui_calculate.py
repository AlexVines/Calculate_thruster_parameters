from tkinter import *
from PIL import ImageTk, Image
import scipy.constants as const
import math

# Create input window
root = Tk()
root.title('Расчет параметров ЭРД')
root.iconbitmap('Pictures/di.ico')
root.geometry('900x600')

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
img_label = Label(root)
magnet_button = Button(root)


# CONST

mp = const.proton_mass
e = const.e
me = const.electron_mass
g = const.g
mu0 = 4 * const.pi * 10 ** (-7)


# Additional data
bt = 2
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

def solve_magnet():
    # global res
    # global result
    # global rasm
    # global wrong
    # res.destroy()
    # result.destroy()
    # rasm.destroy()
    # wrong.destroy()

    # Get variables
    n = int(pereferi.get())
    bm2 = bm / 1000
    ik = float(eCur.get())
    d_sr = float(eDiam.get())/1000
    fi = 1.9 * const.pi * d_sr * B * bm2
    Iw = kpot * bm2 * fi/ (mu0 * const.pi * d_sr * 3 * bm2)
    N = Iw/ik
    Dc = math.sqrt(4 * 10**6 * fi/(const.pi*Bmax))
    Dper = Dc/2.449
    Nc = N/2
    Nper = Nc/n

    # Print solution
    res_mag = Label(top, text='Результаты расчётов:')
    res_mag.grid(row=4, column=1)

    space = Label(top, text='\n')
    space.grid(row=5, column=3)

    res_mag = Label(top, text="""          Магнитный поток в зазоре: \n
            Число ампер витков: \n
            Минимальный диаметр центрального сердечника: \n
            Минимальный диаметр периферийного сердечника: \n
            Число витков на центральной катушке: \n
            Число витков на периферийных катушках: \n
            """)
    res_mag.grid(row=6, column=0)

    result = Label(top, text=
    '{} \n \n {} \n \n {} \n \n {} \n \n {}\n \n {}\n \n'.format(
        reformat(fi),
        round(Iw),
        round(Dc),
        round(Dper),
        round(Nc),
        round(Nper)))
    result.grid(row=6, column=1)

    rasm_mag = Label(top, text="""               Вб \n
                А в \n
                мм \n
                мм \n
                  \n
                  \n
                    """)
    rasm_mag.grid(row=6, column=2)
    root.mainloop()

def open_magnet_calc():
    global top
    global eCur
    global eDiam
    global pereferi

    top = Toplevel()
    top.title('Расчёт магнитной системы')
    top.iconbitmap('Pictures/di2.ico')

    sred_diam = Label(top, text='Средний диаметр: ')
    sred_diam.grid(row=0, column=0)
    eDiam = Entry(top)
    eDiam.grid(row=0, column=1)
    eDiam.insert(0, '70')
    draz = Label(top, text='мм')
    draz.grid(row=0, column=2)

    thrust_m = Label(top, text='Ток в катушках: ')
    thrust_m.grid(row=1, column=0)
    eCur = Entry(top)
    eCur.grid(row=1, column=1)
    eCur.insert(0, '1')
    peref = Label(top, text='А')
    peref.grid(row=1, column=2)

    fuel = Label(top, text='Количество переферийных катушек: ')
    fuel.grid(row=2, column=0)

    pereferi = StringVar()
    pereferi.set('3')
    per_cat = OptionMenu(top, pereferi, '3', '4', '6', '8')
    per_cat.grid(row=2, column=1)

    rasch_mag = Button(top, text='Рассчитать', command=solve_magnet)
    rasch_mag.grid(row=3, column=0)


def solve():
    global res
    global result
    global rasm
    global wrong
    global img_label
    global magnet_button
    global Dsr
    global bm
    res.destroy()
    result.destroy()
    rasm.destroy()
    wrong.destroy()
    img_label.destroy()
    magnet_button.destroy()

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
        bm = bk + 2 * st + 2 * bt

        # Print solution
        res_label = Label(root, text='Результаты расчётов:')
        res_label.grid(row=4, column=1)

        space = Label(root, text='\n')
        space.grid(row=5, column=3)

        res = Label(root, text="""Массовый расход: \n
        Тяговый КПД: \n
        Удельный импульс: \n
        Разрядное напряжение: \n
        Разрядный ток: \n
        Средний диаметр (Dср): \n
        Ширина канала (bk): \n
        Внешний диаметр канала (D): \n
        Длина канала (lk): \n
        Толщина стенки канала (δ): \n
        Межполюсной зазор: (bm)
        """)
        res.configure(anchor='e')
        res.grid(row=6, column=0)

        result = Label(root, text =
        '{} \n \n {} \n \n{} \n \n {} \n \n {} \n \n {} \n \n {} \n \n {} \n \n {} \n \n {}\n \n {}\n'.format(
                                                                             reformat(m*10**6),
                                                                             round(f_eff, 1),
                                                                             round(Iud),
                                                                             round(Ur),
                                                                             reformat(Ir),
                                                                             round(Dsr),
                                                                             round(bk),
                                                                             round(Dvn),
                                                                             round(lk), round(st), round(bm)))
        result.grid(row=6, column=1)

        # dsr = Label(root, text=str(round(Dsr)))
        # dsr.place(x=960, y=155)

        rasm = Label(root, text="""        мг/c \n
            % \n
            сек \n
            В \n
            А \n
            мм \n
            мм \n
            мм \n
            мм \n
            мм \n
            мм
                """)
        rasm.grid(row=6, column=2)

        image = Image.open('Pictures/Geometry.jpg')
        resized = image.resize((500, 400), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        img_label = Label(root, image=img)
        img_label.grid(row=6, column=5, sticky='nw')

        magnet_button = Button(root, text='Рассчитать магнитную систему', command=open_magnet_calc)
        magnet_button.grid(row=8, column=0)

        root.mainloop()

myButton = Button(root, text='Рассчитать', command=solve)
myButton.grid(row=3, column=0)

root.mainloop()
