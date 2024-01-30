from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Frequenza delle keywords
keyword_frequencies = {    
    "Obesity": 462,
    "Children": 435,
    "HIV": 424,
    "Epidemiology": 417,
    "Breast cancer": 386,
    "Quality of life": 375,
    "Malaria": 374,
    "Physical activity": 370,
    "Prognosis": 358,
    "Mortality": 352,
    "Prevalence": 338,
    "prognosis": 329,
    "Risk factors": 317,
    "Depression": 297,
    "Ethiopia": 261,}

# Creare il word cloud direttamente dalla frequenza delle parole
wordcloud = WordCloud(width=1600, height=800, background_color="white").generate_from_frequencies(keyword_frequencies)

# Visualizzare il word cloud utilizzando matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
