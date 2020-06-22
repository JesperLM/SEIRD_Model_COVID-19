import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.integrate import solve_ivp

def movingAverage(series, window_size, exclude = 1):
    """
    This function averages the data series over a set of 
    datapoints (window_size). It can also exlude a set amount 
    of datapoints (exlude) at the end of the data serie.
    """
    i = 0
    moving_averages = [0] * int(window_size/2)

    index_array = series.index.array

    while i < len(series) - window_size + 1 - exclude: # The last '-exclude' is to exclude the data from the lastest days.
        this_window = series[i : i + window_size]

        window_average = sum(this_window) / window_size
        moving_averages.append(window_average)
        i += 1
    moving_averages[int(window_size/2)] = series[0]
    df = pd.DataFrame(data=moving_averages, index=index_array[0:len(series) - (window_size-int(window_size/2)) + 1 - exclude], columns=['Average'])
    return df

def social_distancing(t):
    """ Defines curves for effects of social distancing. """
    time_array =       np.array([0, 32,   35,   45,   54,   59,   60,   62,   70,  130,  200,  270,  300,  400, 1000])
    distancing_array = np.array([1,  1, 0.99, 0.95, 0.80,  0.5, 0.20, 0.19, 0.15, 0.14, 0.25, 0.25, 0.25, 0.25, 0.25])
    return np.interp(t, time_array, distancing_array)

def calculate_Re(t, beta, gamma, alpha, mu):
    """ Calculates the Reproduction number. """
    R_num = social_distancing(t) * alpha/(alpha+mu) * beta/(mu+gamma)
    return R_num

def outbreak():
    """Test case using a SEIR model."""
    def SEIRD_ODE(t, u):
        S, E, I, R, D = u
        return [-beta*social_distancing(t)*S*I/(N-D), beta*social_distancing(t)*S*I/(N-D) - alpha*E, alpha*E - gamma*I - mu*I, gamma*I, mu*I]
    

    N = 10000000       # Size of population
    E0 = 50   # Amount of initally exposed
    I0 = 100   # Amount of initally infected
    R0 = 0   # Amount of initally recovered
    D0 = 0   # Amount of initally dead
    S0 = N - E0 - I0 - R0 - D0
    incubation_time = 5     # Time before an individual is infected
    time_sick = 15          # Time an individual is sick
    death_rate = 0.01       # death rate of disease

    beta  = 0.32      # Contact rate
    alpha = 1 / incubation_time   # inverse of average incubation period
    gamma = 1 / time_sick  # mean recovery rate
    mu = death_rate*gamma
    
    print('R: ' + str(alpha/(alpha+mu)*beta/(mu+gamma)))

    dt = 0.1                # 2.4 h
    Days = 365                # Simulate for 30 days
    N_t = int(Days/dt)        # Corresponding no of time steps
    t_ivp = np.linspace(0, Days, N_t+1)

    SEIRD_0 = [S0, E0, I0 ,R0, D0]    

    solution_ivp = solve_ivp(SEIRD_ODE, [0,Days], SEIRD_0, t_eval=t_ivp)

    S = solution_ivp.y[0]
    E = solution_ivp.y[1]
    I = solution_ivp.y[2]
    R = solution_ivp.y[3]
    D = solution_ivp.y[4]

    print('Death toll after a year: ' + str(D[-1]))
    print('Suseptible after a year: ' + str(S[-1]/N))

    # Change per day
    rate_D = np.diff(D)/dt

    # Read Infected and Dead data from FHM
    df_infected_per_day = pd.read_excel (r'FHM_data\Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal per dag region', index_col=0)
    df_dead_per_day = pd.read_excel (r'FHM_data\Folkhalsomyndigheten_Covid19.xlsx', sheet_name='Antal avlidna per dag', index_col=0)


    # Infected / Day
    df_infected = pd.concat( [df_infected_per_day['Totalt_antal_fall'],
                              movingAverage(df_infected_per_day['Totalt_antal_fall'],7)], axis=1)

    # Dead / Day
    df_dead = pd.concat( [df_dead_per_day['Antal_avlidna'],
                          movingAverage(df_dead_per_day['Antal_avlidna'],21)], axis=1)

    time_infected = np.linspace(0, len(df_infected['Totalt_antal_fall']), len(df_infected['Totalt_antal_fall']))+32-36
    time_dead = np.linspace(0, len(df_dead['Antal_avlidna']), len(df_dead['Antal_avlidna']))+32

    print('Death toll after 120 model: ' + str(D[1200]))
    print('Death toll after 120 true: ' + str(df_dead['Average'].sum()))

    # Calculate Re
    Re = calculate_Re(t_ivp, beta, gamma, alpha, mu)

    # Plot the Re, Death evolution and the pandemic outbreak for the model
    fig = plt.figure(constrained_layout=True)
    fig.set_size_inches(10, 5)
    
    gs = fig.add_gridspec(2, 2)

    ax1 = fig.add_subplot(gs[0,1])
    ax1.plot(t_ivp, Re, label='Estimated R', zorder=10)    

    ax1.set_xlabel('Days')
    ax1.set_ylabel('Estimated R')
    ax1.set_xlim(0,Days)

    ax1.xaxis.set_major_locator(plt.MultipleLocator(60))

    ax1.legend()

    # Subplot for the Death rate
    ax2 = fig.add_subplot(gs[1, :])

    ax2.plot(t_ivp[:-1], rate_D, label='Predicted Death Rate', color='tab:blue', zorder=10)
    ax2.bar(time_dead, df_dead['Antal_avlidna'], label='Daily Death', color='tab:orange', width=1)
    ax2.plot(time_dead, df_dead['Average'], label='7 Day Moving Average', color='tab:green')

    ax2.annotate('Middle of April', xy=(72, 90), xytext=(122, 100),
            arrowprops=dict(arrowstyle="->"))  
    ax2.annotate('Midsummer', xy=(137, 25), xytext=(190, 70),
            arrowprops=dict(arrowstyle="->"))

    ax2.set_xlabel('Days')
    ax2.set_ylabel('New Deaths per Day')
    ax2.set_xlim(0,Days)
    ax2.set_ylim(0,120)#N)
    ax2.xaxis.set_major_locator(plt.MultipleLocator(60))

    ax2.legend()

    # Subplot for the pandemic outbreak
    ax3 = fig.add_subplot(gs[0, 0])

    ax3.plot(t_ivp, S, label='Susceptibles')
    ax3.plot(t_ivp, E, label='Exposed')
    ax3.plot(t_ivp, I, label='Infected')
    ax3.plot(t_ivp, R, label='Recovered')
    ax3.plot(t_ivp, D, label='Dead')

    ax3.set_ylabel('Number of People')
    ax3.set_xlabel('Days')
    ax3.set_ylim(0,N)
    ax3.set_xlim(0,Days)
    ax3.xaxis.set_major_locator(plt.MultipleLocator(30))
    ax3.text(80,7500000, r'Assumed 1% death rate')

    ax3.legend()

    fig.suptitle('Modeling COVID-19 outbreak in Sweden')
    
    plt.savefig(r'.\Figure\outbreak_overview.png')

    # Plot the Re for the model
    fig = plt.figure(constrained_layout=True)
   
    gs = fig.add_gridspec(1, 1)

    ax1 = fig.add_subplot(gs[0,0])
    ax1.plot(t_ivp, Re, label='Estimated R', zorder=10)    

    ax1.set_xlabel('Days')
    ax1.set_ylabel('Estimated R')
    ax1.set_xlim(0,Days)

    ax1.xaxis.set_major_locator(plt.MultipleLocator(60))

    ax1.legend()

    fig.suptitle('Estimated repoduction number for Sweden')

    plt.savefig(r'.\Figure\reproduction.png')

    # Plot the Death evolution for the model
    fig = plt.figure(constrained_layout=True)
   
    gs = fig.add_gridspec(1, 1)

    ax2 = fig.add_subplot(gs[0, 0])

    ax2.plot(t_ivp[:-1], rate_D, label='Predicted Death Rate', color='tab:blue', zorder=10)
    ax2.bar(time_dead, df_dead['Antal_avlidna'], label='Daily Death', color='tab:orange', width=1)
    ax2.plot(time_dead, df_dead['Average'], label='7 Day Moving Average', color='tab:green')

    ax2.annotate('Middle of April', xy=(72, 90), xytext=(122, 100),
            arrowprops=dict(arrowstyle="->"))  
    ax2.annotate('Midsummer', xy=(137, 25), xytext=(190, 70),
            arrowprops=dict(arrowstyle="->"))

    ax2.set_xlabel('Days')
    ax2.set_ylabel('New Deaths per Day')
    ax2.set_xlim(0,Days)
    ax2.set_ylim(0,120)#N)
    ax2.xaxis.set_major_locator(plt.MultipleLocator(60))

    ax2.legend()

    fig.suptitle('Estimated COVID-19 deaths in Sweden')

    plt.savefig(r'.\Figure\death.png')



    # Plot for the pandemic outbreak 
    fig = plt.figure(constrained_layout=True)
   
    gs = fig.add_gridspec(1, 1)
    ax3 = fig.add_subplot(gs[0, 0])

    ax3.plot(t_ivp, S, label='Susceptibles')
    ax3.plot(t_ivp, E, label='Exposed')
    ax3.plot(t_ivp, I, label='Infected')
    ax3.plot(t_ivp, R, label='Recovered')
    ax3.plot(t_ivp, D, label='Dead')

    ax3.set_ylabel('Number of People')
    ax3.set_xlabel('Days')
    ax3.set_ylim(0,N)
    ax3.set_xlim(0,Days)
    ax3.xaxis.set_major_locator(plt.MultipleLocator(30))
    ax3.text(130,7500000, r'Assumed 1% death rate')

    ax3.legend()

    fig.suptitle('COVID-19 outbreak in Sweden')
    
    plt.savefig(r'.\Figure\outbreak.png')


    plt.show()
    

if __name__ == '__main__':
    outbreak()