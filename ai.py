import g4f

g4f.debug.logging = True
g4f.check_version = False
print(g4f.version)
print(g4f.Provider.Ails.params)

def responce(text):
    print(text)
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Общайся со мной как с другом. (не говори привет. Это нужно) " + text}],
        provider=g4f.Provider.ChatgptAi
    )

    return response