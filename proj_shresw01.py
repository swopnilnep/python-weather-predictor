""" temp_analysis.py: Takes temperature data formateed in the format in 'annual_maxTemp.txt', 'annual_minTemp.txt' and presents it to the user in a readable formatto the user"""
__author__ = "Swopnil N. Shrestha"
__copyright__ = "Copyright 2018, Luther College"
__version__ = "0.0.1"
__email__ = "shresw01@luther.edu"
__status__ = "prototype"
__date__ = "06/05/2018"


import numpy as np
from turtle import Turtle, Screen

# Functions

def read_data(c_var):
    d_files = {'max_temp': 'annual_maxTemp.txt', 'min_temp': 'annual_minTemp.txt'}
    data_file = open(d_files[c_var], 'r')
    lines = data_file.readlines()
    n_rows = len(lines)
    n_cols = len(lines[0].split()) - 1
    d_a = np.zeros((n_rows, n_cols), dtype=int)
    for r in range(n_rows):
        p = lines[r].strip().split()[1:]
        for c in range(len(p)):
            d_a[r, c] = p[c]
    return d_a
def clc_ave(a_list, p_error):
    num_missing = (a_list == -99).sum()
    if float(num_missing)/len(a_list) >= p_error: return -99
    else: b_list = [a for a in a_list if a != -99] # Filters the list for 
    return float(sum(b_list))/len(b_list) # Returns the average of b_list
def clc_ave_li(a_list, error):
    num_missing = a_list.count(-99)
    if float(num_missing)/len(a_list) >= error: return -99
    else: b_list = [a for a in a_list if a != -99] # Filters the list for
    return float(sum(b_list))/len(b_list) # Returns the average of b_list
def julian_2_mn_day(j):
    m_r = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
    mon = 0
    while (m_r[mon] < j): mon += 1
    return mon , j - m_r[mon - 1] #left = month, right = day
def mn_2_julian(m_no):
    m_ran = [[1,31], [32,59], [60,90],[91,120],[121,151],[152,181],[182,212],[213,243],[244,273],[274,304],[305,334],[335,365]]
    return m_ran[m_no - 1][0], m_ran[m_no - 1][1] # returns low, high
def daily_ave(max, min):
    all_alist = (max + min) / 2
    return all_alist
def annual_ave_t(a_in):
    # Only evaluates if < 3% of data is missing
    a_ave = []
    for i in range(len(a_in)):
        a_ave.append(clc_ave(a_in[i]), 0.03)
    return a_ave
def monthly_ave_t(a_in, m_no, yr_s, yr_e):
    a_out = []
    j_lo, j_hi = mn_2_julian(m_no)
    
    # Calibrate it according to the list 
    j_lo -= 1 
    j_hi -= 1 
    yr_s -= 1893 
    yr_e -= 1893 
    # Sets the smaller one to yr_s 
    if yr_s > yr_e: yr_s, yr_e = yr_e, yr_s
    for yr in range(yr_s, yr_e + 1):
        month = a_in[yr, j_lo:j_hi + 1]
        a_out.append(clc_ave(month), 0.03)
    return a_out
def rank_list(l_in, yr_b):
    l = []
    # Convert to 2d list
    for item in range(len(l_in)):
        l.append([l_in[item], yr_b + item])
    # Sort according to the algorithm  
    for i in range(len(l)):
        for j in range(len(l) - 1):
            if l[j][0] < l[j+1][0]:l[j+1], l[j] = l[j], l[j+1]
            elif l[j][0] == l[j+1][0]: 
                if l[j][1] < l[j+1][1]:l[j+1], l[j] = l[j], l[j+1]
    return l
def plot_temp_vs_day(t_list):
    # # t_list = [t_year, t_ave]
    t = Turtle()
    wn = Screen()
    wn.tracer(0)
    # t.speed(100)
    t.ht()
    
    # Setting grid coordinates
    x_max = len(t_list[1])
    x_min = 0
    y_max = int(max(t_list[1]))
    y_min = 0
    if min(t_list[1]) < 0: y_min = int(min(t_list[1]) - 10)
    
    # Grid Scales
    x_scl = 20
    y_scl = 20
    
    wn.setworldcoordinates(x_min - 20, y_min - 20, x_max + 20, y_max + 20)
    
    # Draw axis 
    axis = [[x_min, y_min],[x_max, y_min],[0.0, y_min],[0.0, y_max]]
    for i in range(0, 4, 2):
        t.up()
        t.goto(axis[i][0],axis[0][1]) # Origin x,y (0,2) 
        t.down()
        t.goto(axis[i + 1][0], axis[i + 1][1]) # highest point x,y (0,2)
        t.up()
        
    # Draw lines
    
    # x-lines
    t.up()
    t.goto(x_min, y_min) #goes to origin 
    for i in range(x_max//x_scl):
        t.up()
        t.forward(x_scl)
        t.left(90)
        t.forward(1)
        t.down()
        t.forward(-2)
        t.up()
        t.forward(-4)
        t.write(str(i * x_scl), font=("Arial", 14, "normal"))
        t.forward(5)
        t.right(90)
        
    # y-lines
    t.up()
    t.goto(x_min, y_min) #goes to origin 
    t.left(90)
    for i in range(y_max//y_scl):
        t.up()
        t.forward(y_scl)
        t.left(90)
        t.forward(1)
        t.forward(8)
        t.write(str(i * x_scl), font=("Arial", 14, "normal"))
        t.forward(-8)
        t.down()
        t.forward(-2)
        t.up()
        t.forward(1)
        t.right(90)    
    
    t.up()
    # Draw the graph 
    t.color('blue')
    t.goto(x_min, y_min)
    t.down()
    for i in range(len(t_list[1])):
        if t_list[1][i] != -99: 
            # t.up()
            t.goto(i, t_list[1][i])
            t.down()
            t.dot()

    t.up()
    # Draw the graph
    t.color('green')
    t.goto(x_min, y_min)
    t.down()
    for i in range(len(t_list[0])):
        if t_list[0][i] != -99:
            #t.up()
            t.goto(i * 2.8969, t_list[0][i])
            t.down()
            t.dot()
    wn.update()
    wn.exitonclick()

def n_day_average(a_in, n):
    li_a = list(a_in)
    li_out = []
    for i in range(len(li_a)):
        li_out.append([])
        for j in range(n // 2):
            li_out[i].append(-99)

        for j in range(n//2, len(li_a[i]) - n//2):
            li_slice = li_a[i][j -  n//2: j + n//2 + 1]
            day_ave = clc_ave(li_slice, 0.3)
            li_out[i].append(day_ave)

        for j in range(n // 2):
           li_out[i].append(-99)
    a_out = np.array(li_out)
    return(a_out)

# Write to file

def wrt_file_t03(l1, l2):
    o_f = open('ann_ave_temp_his.txt', 'w')
    o_f.write('{0:^16s}|{1:^19s}\n'.format('Chronilogical', 'Ranked'))
    o_f.write('{0:^16s}|{1:^19s}\n'.format('-' * 16, '-' * 19))
    o_f.write('{0:^7s}{1:^9s}|{2:^6s}{3:^6s}{4:^7s}\n'.format('Year', 'Ave', 'No.', 'Year', 'Ave'))
    o_f.write('{0:^16s}|{1:^19s}\n'.format('-' * 16, '-' * 19))
    for i in range(len(l1)):
        o_f.write('{0:^7d}{1:^9.2f}|{2:^6d}{3:^6d}{4:^7.2f}\n'.format(i+1893,l1[i],i+1,l2[i][1]+1893,l2[i][0]))
    o_f.close
def wrt_file_t04(l1, l2, mn):
    o_f = open('m'+str(mn)+'_ave_temp_his.txt', 'w')
    n_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    o_f.write('{0:^36s}\n'.format(n_list[mn-1]+' Temperature History'))
    o_f.write('{0:^16s}|{1:^19s}\n'.format('Chronilogical', 'Ranked'))
    o_f.write('{0:^16s}|{1:^19s}\n'.format('-' * 16, '-' * 19))
    o_f.write('{0:^7s}{1:^9s}|{2:^6s}{3:^6s}{4:^7s}\n'.format('Year', 'Ave', 'No.', 'Year', 'Ave'))
    o_f.write('{0:^16s}|{1:^19s}\n'.format('-' * 16, '-' * 19))
    for i in range(len(l1)):
        o_f.write('{0:^7d}{1:^9.2f}|{2:^6d}{3:^6d}{4:^7.2f}\n'.format(i+1893,l1[i],i+1,l2[i][1]+1893,l2[i][0]))
    o_f.close()
def wrt_file_t05(l1, l2, mn):
    o_f = open('m' + str(mn) + '_daily_ave_temps.txt', 'w')
    n_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    d_s =[0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    m_l = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    o_f.write('{0:^28s}\n'.format('Ave Max & Min Temps for '+n_list[mn-1]))
    o_f.write('{0:^28s}\n'.format('-'*28))
    o_f.write('{0:^6s}|{1:^10s}|{2:^10s}\n'.format('Day','Ave Max','Ave Min'))
    o_f.write('{0:^6s}|{1:^10s}|{2:^10s}\n'.format('-'*6,'-'*10,'-'*10))
    for i in range(m_l[mn-1]):
        o_f.write('{0:^6d}|{1:^10.2f}|{2:^10.2f}\n'.format(i+1,l1[i+d_s[mn-1]],l2[i+d_s[mn-1]]))

# Tasks
def task_03():
    # Get the values from the text file
    t_max = read_data('max_temp')
    t_min = read_data('min_temp')
    d_ave = daily_ave(t_max, t_min)

    # Calculate Annual Average
    a_ave = annual_ave_t(d_ave)

    # Rank Annual Average
    r_ave = rank_list(a_ave, 0)

    wrt_file_t03(a_ave, r_ave)

def task_04():
    # Get the values from the text file
    t_max = read_data('max_temp')
    t_min = read_data('min_temp')
    d_ave = daily_ave(t_max ,t_min)

    for m_no in range(1, 13):
        m_ave = monthly_ave_t(d_ave, m_no, 1893, 2018)
        r_ave = rank_list(m_ave, 0)
        wrt_file_t04(m_ave, r_ave, m_no)

def task_05():
    t_max = read_data('max_temp')
    t_min = read_data('min_temp')

    l_max = []
    l_min = []
    for i in range(365):
        l_max.append([])
        l_min.append([])
        for j in range(126):
            l_max[i].append(t_max[j][i])
            l_min[i].append(t_min[j][i])

    a_t_max = []
    a_t_min = []

    for i in range(365):
        a_t_max.append(clc_ave_li(l_max[i]), 0.03)
        a_t_min.append(clc_ave_li(l_min[i]), 0.03)



    for i in range(1,13):
        wrt_file_t05(a_t_max, a_t_min, i)


def task_06():
    t_max = read_data('max_temp')
    t_min = read_data('min_temp')

    t_ann = daily_ave(t_max, t_min)
    a_ave = annual_ave_t(t_ann)

    plot_temp_vs_day([a_ave,t_ann[119]])

def task_07():
    t_max = read_data('max_temp')
    t_min = read_data('min_temp')
    d_ave = (daily_ave(t_max, t_min))

    ave_3_day = (n_day_average(d_ave, 3))
    rank_ave = []
    rank_li = []

    # Ranking the list
    for i in range(len(ave_3_day)):
        rank_ave.append(rank_list(ave_3_day[i],0))

    # Inserting Year
    for i in range(len(rank_ave)):
        for j in range(len(rank_ave[i])):
            rank_ave[i][j].insert(1, i + 1893)

    # Flatten List
    for i in range(len(rank_ave)):
        for j in range(len(rank_ave[i])):
            rank_li.append(rank_ave[i][j])

    l = rank_li
    # Sort Using List Sort
    for i in range(len(l)):
        for j in range(len(l) - 1):
            if l[j][0] < l[j + 1][0]: l[j + 1], l[j] = l[j], l[j + 1]

    print("Hottest 3 Day Intevals\nTemp\tYear\tMonth\tDay")
    for i in range(10):
        temp = rank_li[i][0]
        year = rank_li[i][1]
        month, day = julian_2_mn_day(rank_li[i][2])
        print('%0.2f\t%0.2f\t%0.2f\t%0.2f\t' % (temp, year, month, day))

def task_08():
    t_max = read_data('max_temp')
    t_min = read_data('min_temp')
    d_ave = (daily_ave(t_max, t_min))

    ave_7_day = (n_day_average(d_ave, 7))
    rank_ave = []
    rank_li = []

    # Ranking the list
    for i in range(len(ave_7_day)):
        rank_ave.append(rank_list(ave_7_day[i],0))

    # Inserting Year
    for i in range(len(rank_ave)):
        for j in range(len(rank_ave[i])):
            rank_ave[i][j].insert(1, i + 1893)

    # Flatten List
    for i in range(len(rank_ave)):
        for j in range(len(rank_ave[i])):
            rank_li.append(rank_ave[i][j])

    l = rank_li
    # Sort Using List Sort
    for i in range(len(l)):
        for j in range(len(l) - 1):
            if l[j][0] < l[j + 1][0]: l[j + 1], l[j] = l[j], l[j + 1]

    print("Hottest 7 Day Intevals\nTemp\tYear\tMonth\tDay")
    for i in range(10):
        temp = rank_li[i][0]
        year = rank_li[i][1]
        month, day = julian_2_mn_day(rank_li[i][2])
        print('%0.2f\t%0.2f\t%0.2f\t%0.2f\t' % (temp, year, month, day))

def main():
    # task_02(): While using any function above, if the percentage of missing data is >= 3% , it returns -99
    # task_03()
    # task_04()
    # task_05()
    # task_06()
    #task_07() # working but slow
    task_08() # working but slow

main()

