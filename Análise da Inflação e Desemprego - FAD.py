#!/usr/bin/env python
# coding: utf-8

# In[14]:


get_ipython().system('pip install sidrapy')
get_ipython().system('pip install pandas')
get_ipython().system('pip install numpy')
get_ipython().system('pip install seaborn')
get_ipython().system('pip install matplotlib')


# In[16]:


import sidrapy

import pandas as pd
import numpy as np

import seaborn as sns
from matplotlib import pyplot as plt


# In[17]:


ipca_raw = sidrapy.get_table(table_code = '1737', 
                             territorial_level = '1', 
                             ibge_territorial_code = 'all',
                             variable = '2265',
                             period = 'all',
                             header = 'n')


# In[18]:


ipca_raw


# In[19]:


ipca = (
        ipca_raw
        .loc[0:, ['V', 'D2C']]
        .rename(columns = {'V': 'ipca', 'D2C': 'date'})
        
)


# In[20]:


ipca = ipca.loc[ipca.date >= '2004-01-01']


# In[21]:


ipca['date'] = pd.to_datetime(ipca['date'],
                             format = '%Y%m')


# In[24]:


ipca['ipca'] = ipca['ipca'].astype(float)


# In[25]:


ipca.describe()


# In[26]:


sns.lineplot(x = 'date', y = 'ipca', data = ipca)


# In[27]:


sns.histplot(x = 'ipca', data = ipca)


# In[28]:


sns.boxplot(y = 'ipca', data = ipca)


# In[29]:


# Taxa de desocupação - % - PNADC-M/IBGE
desocupacao_raw = sidrapy.get_table(table_code= "6381",
                                    territorial_level = "1",
                                    ibge_territorial_code = "all",
                                    variable = "4099",
                                    period = "all",
                                    header ='n')
# Realiza a limpeza e manipulação da tabela
desocupacao =  (
     desocupacao_raw
    .loc[0:,['V', 'D2C']]
    .rename(columns = {'V': 'desocupacao',
                       'D2C': 'date',}
            )
      )
# Transforma a coluna date em tipo datetime
desocupacao['date'] = pd.to_datetime(desocupacao['date'],
                                format = "%Y%m")

# Filtra os dados
desocupacao = desocupacao.loc[desocupacao.date > '2004-01-01']

# Transforma a coluna ipca em tipo float
desocupacao['desocupacao'] = desocupacao['desocupacao'].astype(float)

# Junta os dados
df_dados = pd.merge(ipca, desocupacao, on = 'date')


# In[33]:


df_dados


# In[36]:


plt.plot('date',
        'ipca',
        data = df_dados,
        label = 'ipca')

plt.plot('date',
       'desocupacao',
       data = df_dados,
       label = 'desemprego')

plt.legend()

plt.show()


# In[37]:


get_ipython().system('pip install statsmodels')


# In[38]:


import statsmodels.formula.api as smf


# In[41]:


modelo = smf.ols('ipca ~ desocupacao', data = df_dados).fit()


# In[44]:


modelo.summary()


# In[45]:


sns.regplot(x = 'desocupacao', y = 'ipca', data = df_dados)


# In[ ]:




