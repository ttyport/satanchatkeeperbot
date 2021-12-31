from json import dumps


def create_config():
    print("Welcome in satanchatkeeperbot setup configurator\nLet's start!")
    token = input("Enter your bot's token:\n\t")

    valid = False
    while not valid:
        try:
            timeout = int(input("Enter your bot's ban timeout (seconds):\n\t"))
            valid = True
        except ValueError:
            print("You entered incorrect amount of seconds, try one more time.")

    phrases = ["Если я нашу кандибобер на голове, то это не значит, что я женщина или балерина.",
               "Я прошла афганскую войну, и желаю всем мужчинам пройти ее.",
               "Ибрагим вам о чем нибудь говорит? Прекрасное имя, Аллах Акбар.",
               "Мужчина определяется делом, а не словом."]

    config = {"token": token, "timeout": timeout, "phrases": phrases}
    json = dumps(config, indent=2)

    with open("../data/config.json", "w", encoding="utf-8") as config_file:  # Проблема с кодировкой никак не влияет на работоспособность бота
        config_file.write(json)

    config_file.close()

    print("Congrats! Bot was configured successfully.")


if __name__ == '__main__':
    create_config()