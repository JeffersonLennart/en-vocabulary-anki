import en_vocabulary_anki as eva

# text = "water"
# tts = gTTS(text=text, lang='en')
# tts.save("schedule.mp3")
#print(eva.get_word_ipa("camion",True))

# file_name = eva.create_word_pronunciation('zero')

# eva.add_note(deckName = "Udemy", modelName = "Basic", fields = {
#                     "Front": f"front content [sound:{file_name}]",
#                     "Back": "back content"
#                 }, options = {
#                     "allowDuplicate": False
#                 })

#print(eva.get_model_names())
# pais_info = pycountry.countries.search_fuzzy("Eswatini")
# print(pais_info)

# from countryinfo import CountryInfo


# country = CountryInfo('Cape Verde')
# print(country.info()["ISO"])

# test = ['Andorra', 'Bahamas', 'Myanmar', 'Congo', 'Eswatini', 'Gambia', 'Micronesia', 'Montenegro', 'Vatican City', 'Cape Verde']
# for i in test:
#     pais_info = pycountry.countries.search_fuzzy(i)
#     print(pais_info.alpha_2)

print(eva.get_deck_names())