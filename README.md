# Modeling of COVID-19 outbreak in Sweden
The aim of this project was to learn modeling of a pandemic outbreak as well as to understand the ongoing outbreak with a focus on Sweden.

To do this a ODE model is used and compared to the data available from Folkhälsomydigheten (swedish CDC).

## Model
The model used in the code is a compartmentalized model based on a SIR approch. The change with respect to a SIR model is that this model also will include the incubation period and the deceased. A visulazation of the model is shown below.

![Model Visulization](https://raw.githubusercontent.com/JesperLM/SEIRD_Model_COVID-19/master/Figure/SEIRD-model.PNG)

This model uses the following ordinary differatial equations:

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dS}{dt}=-\frac{\beta IS}{N-D}"/>,

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dE}{dt}=\frac{\beta IS}{N-D}-\alpha E" />,

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dI}{dt}=\alpha E - \gamma I - \mu I" />,

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dR}{dt}=\gamma I"/>,

<img src="https://render.githubusercontent.com/render/math?math=\LARGE  \frac{dD}{dt}=\mu I"/>,

where S is the number of suseptible individuals, E is the number of individuals exposed to the disease, I is the numbner of infected individuals, R is the amount of recoverd individuals (imune) and D is the number of individuals who have died from the disease.

β is the contact rate of the disease, α is the average incubation rate, γ is the recovery rate and μ is the mortality rate of the disease.

## Assumtions
As mentined earlier the model aims to predict the spread of the disease in Sweden and hence the model is input is aligned with the conditions in Sweden.

| What | Value      | Comment    |
| :--: | :--------- | ---------: |
|  β   | 0.32       | Tuned for model    |
|  α   | 1/5        | The average incubation time has been reported to be 5  days      |
|  γ   | 1/15       | The average time beeing sick has been reported to be 15 days    |
|  μ   | 0.5% * γ   | The assumed fatality rate  |
|  N   | 10 000 000 | Population of Sweden  \| |

An initial condition is needed to start calcualting the spread of the model. The one used in this model is that there is are 25 intially exposed to the disease and 50 individuals who are sick.

From the values in the table above the reproduction number would be ~4.74. However the reproduction number has been reduce with the social distancing that has been used.

![Reproduction number](https://raw.githubusercontent.com/JesperLM/SEIRD_Model_COVID-19/master/Figure/reproduction.png)

## Output
Using the model preseted above the both the model and the reported numbers predict ~5 000 deaths up to the swedish midsummer. A visulization of the prediction can be seen below.

![Number of Death per day](https://raw.githubusercontent.com/JesperLM/SEIRD_Model_COVID-19/master/Figure/death.png)

It can be seen that even with a slight reducttion in the social distancing the virus will increase it speading during the fall. With this model the number of dead in Sweden after a year is predicted to be ~11 000 people. 

Even dough it some tiomes feels like the pandemic is about to end the outbreak is far from over if we relax the social distancing. This model predicts that after 1 year 88% of the swedish population will not have been infected. If a lower death rate would have been assumed this number will be lower, but since the estimated fatality rate is in the range 0.5-1% no more than 24% (linear scaling) would have been invfected if a fatality rate of 0.5 had been used.

![Overview of Outbreak](https://raw.githubusercontent.com/JesperLM/SEIRD_Model_COVID-19/master/Figure/outbreak.png)

Remeber to keep up the social distansing and wash your hands!

## Licence
MIT
