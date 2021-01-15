from tkinter import *
from PIL import ImageTk, Image
import scipy.constants as const
import math

root = Tk()
root.title('Расчет параметров ЭРД')
root.iconbitmap('Pictures/1.ico')


labels = ['Мощность двигателя:', 'Тяга двигателя:', 'Рабочее тело:',

          'Массовый расход:', 'Тяговый КПД:', 'Удельный импульс:', 'Разрядное напряжение:', 'Разрядный ток:',
          'Средний диаметр (Dср):', 'Ширина канала (bk):', 'Внешний диаметр канала (D):', 'Длина канала (lk):',
          'Толщина стенки канала (δ):', 'Межполюсной зазор (bm):',
          'Средний диаметр:', 'Ток в катушках:', 'Количество переферийных катушек',

          'Магнитный поток в зазоре:', 'Число ампер витков:', 'Минимальный диаметр центрального сердечника:',
          'Минимальный диаметр периферийного сердечника:', 'Число витков на центральной катушке:',
          'Число витков на периферийных катушках:']

dimensions = ['Вт', 'мг/с', '%', 'сек', 'В', 'А', 'мм', 'мм', 'мм', 'мм', 'мм', 'мм', 'мм', 'A', 'Вб', 'А в', 'мм',
              'мм', '', '']

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


class InputLine:
    def __init__(self, master, label_text, row, insert, dimension):
        self.first = Label(master, text=label_text).grid(row=row, column=0, sticky='e', pady=5)
        self.enter = Entry(master)
        self.enter.grid(row=row, column=1)
        self.enter.insert(0, insert)
        self.dimension = Label(master, text=dimension).grid(row=row, column=2, padx=5)


class OutputLine:
    def __init__(self, master, label_text, row, result, dimension):
        self.first = Label(master, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky='e')
        self.first = Label(master, text=result).grid(row=row, column=1)
        self.dimension = Label(master, text=dimension).grid(row=row, column=2, padx=5)


def solve_magnet():
    results = calculate_magnet()
    for j in range(6):
        OutputLine(top, labels[j + 17], j + 5, results[j], dimensions[j + 14])


def create_second_window():
    global top
    global pereferi
    global cur
    global med_diam

    top = Toplevel()
    top.title('Расчёт магнитной системы')
    top.iconbitmap('Pictures/2.ico')

    inserts = ['70', '1']
    med_diam = InputLine(top, labels[14], 0, inserts[0], dimensions[12])
    cur = InputLine(top, labels[15], 1, inserts[1], dimensions[13])

    Label(top, text='Количество периферийных катушек: ').grid(row=2, column=0, sticky='e')
    pereferi = StringVar()
    pereferi.set('3')
    OptionMenu(top, pereferi, '3', '4', '6', '8').grid(row=2, column=1)

    Button(top, text='Рассчитать', command=solve_magnet).grid(row=4, column=0, pady=15)


def calculate_magnet():
    bm = calculate()[-1]
    n = int(pereferi.get())
    bm2 = bm / 1000
    ik = float(cur.enter.get())
    d_sr = float(med_diam.enter.get()) / 1000
    fi = 1.9 * const.pi * d_sr * B * bm2
    Iw = kpot * bm2 * fi / (mu0 * const.pi * d_sr * 3 * bm2)
    N = Iw / ik
    Dc = math.sqrt(4 * 10 ** 6 * fi / (const.pi * Bmax))
    Dper = Dc / 2.449
    Nc = N / 2
    Nper = Nc / n
    return [reformat(fi), round(Iw), round(Dc), round(Dper), round(Nc), round(Nper)]


def solve():
    # Clear frame
    for widget in output_frame.winfo_children():
        widget.destroy()

    # Print result
    result1 = calculate()
    if result1:
        for j in range(11):
            OutputLine(output_frame, labels[j + 3], j, result1[j], dimensions[j + 1])

        img = ImageTk.PhotoImage(Image.open('Pictures/Skhema.png').resize((500, 400), Image.ANTIALIAS))
        Label(output_frame, image=img).grid(row=0, column=5, rowspan=11)

        Button(output_frame, text='Рассчитать магнитную систему', command=create_second_window).grid(row=12, column=5,
                                                                                               pady=20, sticky='w')
        root.mainloop()


def calculate():
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

    N = float(power.enter.get())
    M = prop_atom_mass * mp

    # Calculations
    a = 3.7 * prop_fi * e / M
    b = - N / 1.25
    c = F ** 2 / (2 * 0.835 ** 2)
    D = b ** 2 - 4 * a * c
    if D < 0:
        wrong = Label(output_frame, text='Невозможно получить заданные параметры')
        wrong.grid(row=5, column=0)
    else:
        m = (-b - math.sqrt(D)) / (2 * a)
        f_eff = F ** 2 / (2 * N * m) * 100
        Iud = F / (m * g)
        Vi = g * Iud / 0.835
        Ur = M * Vi ** 2 / (2 * e)
        Ir = e * m * 1.25 / M
        Dsr = diam(m * 10 ** 6)
        w = y(m * 10 ** 6)
        Sk = N / w
        bk = Sk / (const.pi * Dsr)
        Dvn = Dsr + bk
        lk = 2 * bk
        st = 0.5 * bk
        bm = bk + 2 * st + 2 * bt
        results = [reformat(m*10**6), round(f_eff, 1), round(Iud), round(Ur), reformat(Ir), round(Dsr), round(bk),
                   round(Dvn), round(lk), round(st), round(bm)]
        return results


def reformat(num):
    if 10000 > num > 0.01:
        return round(num, 2)
    else:
        return format(num, '.2e')


def diam(m):
    return 0.00195 * m**3 - 0.267035 * m**2 + 13.149984 * m + 20.49869


def y(m):
    return 1.176*10**-9 * m**4 - 7.995457*10**-7*m**3 + 1.736478*10**-4*m**2 - 9.85489 * 10**-3*m + 0.3865574


# Create input field
input_frame = Frame(root, padx=10, pady=10)
input_frame.pack()
power = InputLine(input_frame, labels[0], 0, '1350', 'Вт')

Label(input_frame, text='Тяга двигателя: ').grid(row=1, column=0, sticky='e')

eThrust = Entry(input_frame)
eThrust.grid(row=1, column=1)
eThrust.insert(0, '8')
vr = StringVar()
vr.set('г')
OptionMenu(input_frame, vr, 'г', 'мН').grid(row=1, column=2)

Label(input_frame, text='Рабочее тело: ').grid(row=2, column=0, sticky='e')
propellant = StringVar()
propellant.set('Xe')
OptionMenu(input_frame, propellant, 'Xe', 'Ar', 'Bi', 'Kr', 'I').grid(row=2, column=1)

Button(input_frame, text='Рассчитать', command=solve).grid(row=4, column=0)

# Create output field
output_frame = Frame(root, padx=20, pady=20)
output_frame.pack()

root.mainloop()
