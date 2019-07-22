from Dictionary import Dictionary

capitals = Dictionary()

capitals["Pakistan"] = "Islamabad"
capitals["United Kingdoms"] = "London"
capitals["France"] = "Paris"
capitals["India"] = "New Delhi"
capitals["Afghanistan"] = "Kabul"
capitals["China"] = "Beijing"
capitals["Iran"] = "Tehran"
capitals["Russia"] = "Moscow"
capitals["Germany"] = "Berlin"

print("Captital of Pakistan is", capitals["Pakistan"], "\n")

for key in capitals:
    print(capitals[key])

del capitals["India"]
print("INTENTIONAL KEY ERROR")
print(capitals["India"])
