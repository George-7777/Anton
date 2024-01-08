import g4f

g4f.debug.logging = True
g4f.check_version = False
print(g4f.version)
print(g4f.Provider.Ails.params)
history = ""
def responce(text):
    print(text)
    if history:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            #provider=g4f.Provider.ChatgptAi
        )
    else:
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            #provider=g4f.Provider.ChatgptAi
        )

    return response