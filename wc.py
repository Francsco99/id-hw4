from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Frequenza delle keywords
keyword_frequencies = {"Children": 110, "Malaria": 109, "Epidemiology": 103,
                       "Quality of life": 98, "Obesity": 95, "HIV": 91,
                       "Breast cancer": 90, "Physical activity": 85,
                       "Prognosis": 84, "Mortality": 79}

# Creare il word cloud direttamente dalla frequenza delle parole
wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(keyword_frequencies)

# Visualizzare il word cloud utilizzando matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
