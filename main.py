# Eduardo Herreros Fraile - GBSFLP 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider



#PARAMETERS
alpha_h = 0.1
beta_h = 0.1

wint_season = 2
wint_alpha = 0.2
wint_beta = 0.2
wint_zeta = 0.2

#  -----------------------------------------------
# |           DEFINE YOUR FUNCTION HERE!         |      
#  -----------------------------------------------

number_points = 100
np.random.seed(6)
y = np.random.rand(number_points)
x = range(0,number_points)
y = np.linspace(1,3,100)+y*1.5


# x = np.arange(0,4*np.pi,0.1)   # start,stop,step
# y = np.sin(x)+2



def MovingAverage(og_fun, Window):

    if Window == 0:
        pass
        # mov_avg = np.zeros_like(og_fun)
    else:
        mov_avg = np.zeros_like(og_fun)
        for i in range(len(og_fun) - Window):
            mov_avg[i+Window] = og_fun[i:i+Window].sum()/Window
 
        return mov_avg

def Centr_mov_avg(og_fun, Window):

    if Window == 1:
        pass
    else:
        HalfWindow = int((Window-1)/2)
        Smooth = np.zeros_like(og_fun)
        for i in range(HalfWindow, og_fun.shape[0]-HalfWindow):
            Smooth[i] = np.mean(og_fun[(i-HalfWindow):(i+HalfWindow)])

        return Smooth

def ExpSmo_func(og_fun,alpha):
    
    if alpha<0:
        pass
    else:
        Smooth = np.zeros_like(og_fun)
        Smooth[0] = og_fun[0]

        for i in range(1,len(og_fun)):
            Smooth[i] = alpha * og_fun[i] + (1-alpha) * Smooth[i-1]
    
        return Smooth



def Holt_exp_fun(og_fun,alpha,beta):

    if alpha<0 and beta<0:
        pass
    else:  
        #Initialization
        Smooth  = np.zeros_like(og_fun)
        Trend   = np.zeros_like(og_fun)
        Prediction = np.zeros_like(og_fun)

        Smooth[0] = og_fun[0]
        Smooth[1] = og_fun[1]
        Prediction[2] = Smooth[1] + (Smooth[1] - Smooth[0])

        for i in range(2,len(og_fun)-1):
            Smooth[i] = alpha*og_fun[i] + (1-alpha)*(Smooth[i-1]+Trend[i-1])
            Trend[i]  = beta*(Smooth[i]-Smooth[i-1]) + ((1-beta)*Trend[i-1])
            Prediction[i+1]  = Smooth[i]+Trend[i]


        return Prediction

def Wint_exp_fun(og_fun, alpha, beta, zeta, S_len):

    if S_len == 0:
        pass
    else:
    
        Smooth     = np.zeros_like(og_fun)
        Trend      = np.zeros_like(og_fun)
        Season     = np.zeros_like(og_fun)
        Prediction = np.zeros_like(og_fun)

        #Initial values
        Season[:S_len] = og_fun[:S_len] / og_fun[:S_len].mean()
        Smooth[S_len]  = og_fun[S_len] / Season[0]
        Trend[S_len]   = Smooth[S_len] - (og_fun[S_len-1]/Season[S_len-1])

        for i in range(S_len, len(og_fun)-1):
            Season[i] = zeta * (og_fun[i]/Smooth[i]) + (1-zeta) * Season[i-S_len]
            Prediction[i+1] = (Smooth[i] + Trend[i]) * Season[i-S_len]
            Smooth[i+1] = alpha * (og_fun[i+1] / Season[i+1-S_len]) + (1 - alpha) * (Smooth[i] + Trend[i])
            Trend[i+1] = beta * (Smooth[i+1] - Smooth[i]) + (1-beta) * Trend[i]
            
        return Prediction



def update_mov_avg(val):
    current_v = slider_mov_avg.val
    mov_avg = MovingAverage(y, Window=current_v)
    p1.set_ydata(mov_avg)
    fig.canvas.draw()

def update_centr_mov_avg(val):
    current_v = slider_centr_mov_avg.val
    centrl_mov_avg = Centr_mov_avg(y, Window=current_v)
    p2.set_ydata(centrl_mov_avg)
    fig.canvas.draw()
    
def update_exp_smoothing(val):
    current_v = slider_exp_smooth.val
    exp_smooth_value = ExpSmo_func(y, alpha=current_v)
    p3.set_ydata(exp_smooth_value)
    fig.canvas.draw()

def update_holt_alpha(val):
    global alpha_h
    current_v = slider_holt_alpha.val
    alpha_h=current_v
    holt_value = Holt_exp_fun(y, alpha=current_v, beta=beta_h)
    p4.set_ydata(holt_value)
    fig.canvas.draw()

def update_holt_beta(val):
    global beta_h
    current_v = slider_holt_beta.val
    beta_h = current_v
    holt_value = Holt_exp_fun(y, alpha=alpha_h, beta=current_v)
    p4.set_ydata(holt_value)
    fig.canvas.draw()

def update_wint_season(val):
    global wint_season
    current_v = slider_wint_season.val
    wint_season = current_v
    wint_value = Wint_exp_fun(y, alpha=wint_alpha, beta=wint_beta, zeta=wint_zeta, S_len=current_v)
    p5.set_ydata(wint_value)
    fig.canvas.draw()

def update_wint_alpha(val):
    global wint_alpha
    current_v = slider_wint_alpha.val
    wint_alpha = current_v
    wint_value = Wint_exp_fun(y, alpha=current_v, beta=wint_beta, zeta=wint_zeta, S_len=wint_season)
    p5.set_ydata(wint_value)
    fig.canvas.draw()

def update_wint_beta(val):
    global wint_beta
    current_v = slider_wint_beta.val
    wint_beta = current_v
    wint_value = Wint_exp_fun(y, alpha=wint_alpha, beta=current_v, zeta=wint_zeta, S_len=wint_season)
    p5.set_ydata(wint_value)
    fig.canvas.draw()

def update_wint_zeta(val):
    global wint_zeta
    current_v = slider_wint_zeta.val
    wint_zeta = current_v
    wint_value = Wint_exp_fun(y, alpha=wint_alpha, beta=wint_beta, zeta=current_v, S_len = wint_season)
    p5.set_ydata(wint_value)
    fig.canvas.draw()
    

if __name__ == '__main__':

 

    fig = plt.figure(figsize=[10,6])
    ax  = fig.subplots()
    plt.title('Smoothing methods')
        


    # x, y = random_function(100)
    mov_avg = MovingAverage(y, 3)
    centrl_mov_avg = Centr_mov_avg(y, 3)
    exp_smo = ExpSmo_func(y, 0.2)
    holt_exp = Holt_exp_fun(y,0.2,0.95)
    wint_exp = Wint_exp_fun(y, 0.2, 0.2, 0.2, 5)

    
    plt.subplots_adjust(bottom = 0.45)
    p     = ax.plot(x,y)
    p1,   = ax.plot(x,mov_avg,'r', label = 'Moving avg')
    p2,   = ax.plot(x,centrl_mov_avg,'g', label = 'Centralized moving avg')
    p3,   = ax.plot(x,exp_smo,'k', label = 'Exponential smoothing')
    p4,   = ax.plot(x,holt_exp,'y', label = "Holt's exponential smoothing")
    p5,   = ax.plot(x,wint_exp,'violet', label = "Winter's exponential smoothing")



    ax.legend()


    #Slider
    ax_slide  = plt.axes([0.2, 0.1, 0.65, 0.03])
    ax_slide2 = plt.axes([0.2, 0.14, 0.65, 0.03])
    ax_slide3 = plt.axes([0.2, 0.18, 0.65, 0.03])
    ax_slide4 = plt.axes([0.2, 0.22, 0.28, 0.03])
    ax_slide4_2 = plt.axes([0.57, 0.22, 0.28, 0.03])

    ax_slide5_1 = plt.axes([0.2, 0.26, 0.28, 0.03])
    ax_slide5_2 = plt.axes([0.57, 0.26, 0.28, 0.03])
    ax_slide5_3 = plt.axes([0.2, 0.30, 0.28, 0.03])
    ax_slide5_4 = plt.axes([0.57, 0.30, 0.28, 0.03])




    slider_mov_avg = Slider(ax_slide, 'Window_size (Mov.avg)', valmin = 0, valmax=20, valinit=3, valstep=1, color='red', initcolor='none')
    slider_centr_mov_avg = Slider(ax_slide2, 'Window size (C.Mov.avg)', valmin = 1, valmax=31, valinit=3, valstep=2, color='g',initcolor='none')
    slider_exp_smooth = Slider(ax_slide3, 'Exp_smoothing (α)', valmin = -0.03, valmax=1, valinit=0.2, valstep=0.03, color='k',initcolor='none')
    slider_holt_alpha = Slider(ax_slide4, "Holt's exp. α", valmin = -0.01, valmax=1, valinit=0.2, valstep=0.01, color='y',initcolor='none')
    slider_holt_beta = Slider(ax_slide4_2, label='β', valmin = -0.01, valmax=1, valinit=0.95, valstep=0.01, color='y',initcolor='none')

    slider_wint_season = Slider(ax_slide5_1, label="Winter's season_length", valmin = 0, valmax=10, valinit=5, valstep=1, color='violet',initcolor='none')
    slider_wint_alpha  = Slider(ax_slide5_2, label='α', valmin = 0, valmax=1, valinit=0.2, valstep=0.01, color='violet',initcolor='none')
    slider_wint_beta   = Slider(ax_slide5_3, label='β', valmin = 0, valmax=1, valinit=0.2, valstep=0.01, color='violet',initcolor='none')
    slider_wint_zeta   = Slider(ax_slide5_4, label='ζ', valmin = 0, valmax=1, valinit=0.2, valstep=0.01, color='violet',initcolor='none')


    


    

    slider_mov_avg.on_changed(update_mov_avg)
    slider_centr_mov_avg.on_changed(update_centr_mov_avg)
    slider_exp_smooth.on_changed(update_exp_smoothing)
    slider_holt_alpha.on_changed(update_holt_alpha)
    slider_holt_beta.on_changed(update_holt_beta)

    slider_wint_season.on_changed(update_wint_season)
    slider_wint_alpha.on_changed(update_wint_alpha)
    slider_wint_beta.on_changed(update_wint_beta)
    slider_wint_zeta.on_changed(update_wint_zeta)

    


    plt.show()


    

