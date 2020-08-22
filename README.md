# Modeling of COVID-19 outbreak in Sweden
The aim of this project was to learn modeling of a pandemic outbreak as well as to understand the ongoing outbreak with a focus on Sweden.

To do this a ODE model is used and compared to the data available from Folkhälsomyndigheten (swedish CDC).

## Model
The model used in the code is a compartmentalized model based on a SIR approach. The change with respect to a SIR model is that this model also will include the incubation period and the deceased. A visualization of the model is shown below.

![Model Visualization](https://raw.githubusercontent.com/JesperLM/SEIRD_Model_COVID-19/master/Figure/SEIRD-model.PNG)

This model uses the following ordinary differential equations:

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dS}{dt}=-\frac{\beta IS}{N-D}"/>,

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dE}{dt}=\frac{\beta IS}{N-D}-\alpha E" />,

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dI}{dt}=\alpha E - \gamma I - \mu I" />,

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dR}{dt}=\gamma I"/>,

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dD}{dt}=\mu I"/>,

where S is the number of susceptible individuals, E is the number of individuals exposed to the disease, I is the number of infected individuals, R is the amount of recovered individuals (immune) and D is the number of individuals who have died from the disease.

β is the contact rate of the disease, α is the average incubation rate, γ is the recovery rate and μ is the mortality rate of the disease.

## Assumptions
As mentioned earlier the model aims to predict the spread of the disease in Sweden and hence the model is input is aligned with the conditions in Sweden.

| What | Value      | Comment    |
| :--: | :--------- | ---------: |
|  β   | 0.32       | Tuned for model    |
|  α   | 1/5        | The average incubation time has been reported to be 5  days      |
|  γ   | 1/15       | The average time being sick has been reported to be 15 days    |
|  μ   | 0.5% * γ   | The assumed fatality rate  |
|  N   | 10 000 000 | Population of Sweden  \| |

An initial condition is needed to start calculating the spread of the model. The one used in this model is that there is are 25 initially exposed to the disease and 50 individuals who are sick.

From the values in the table above the reproduction number would be ~4.74. However the reproduction number has been reduce with the social distancing that has been used.

![Reproduction number](https://raw.githubusercontent.com/JesperLM/SEIRD_Model_COVID-19/master/Figure/reproduction.png)

## Output
Using the model presented above the both the model and the reported numbers predict ~5 000 deaths up to the swedish midsummer. A visualization of the prediction can be seen below.

![Number of Death per day](https://raw.githubusercontent.com/JesperLM/SEIRD_Model_COVID-19/master/Figure/death.png)

It can be seen that even with a slight reduction in the social distancing the virus will increase its spreading during the fall. With this model the number of dead in Sweden after a year is predicted to be ~11 000 people. 

Even dough it some times feels like the pandemic is about to end the outbreak is far from over if we relax the social distancing. This model predicts that after 1 year 86% of the swedish population will not have been infected. This is highly dependant on how the disease spreads during the fall.

![Overview of Outbreak](https://raw.githubusercontent.com/JesperLM/SEIRD_Model_COVID-19/master/Figure/outbreak.png)

Remember to keep up the social distancing and wash your hands!

## Licence
MIT
