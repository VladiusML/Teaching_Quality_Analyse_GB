def doPredicts(data, path, title=None):
    import matplotlib.pyplot as plt
    import mpld3
    import pandas as pd

    col_check = ["Вежливость","Технические проблемы","Оскорбления и конфликты","Реклама и спам","Плохое объяснение материала и сложность","Хорошее объяснение материала","Помощь и понимание","Опоздание"]
    groupefewfs = [ "Вежливость", "Технические проблемы", "Хорошее объяснение материала", "Плохое объяснение материала и сложность", "Помощь и понимание", "Реклама и спам", "Оскорбления и конфликты", "Опоздание", "Выполнение задания"]

    if not title:
        title = "Общая статистика"
    else:
        title = f"Статистика по вебинару {title}"

    data['count'] = data[col_check].sum(axis=1)
    
    categories = pd.DataFrame({'Category': data[col_check].apply(lambda row: row.idxmax(), axis=1)})
    data = pd.concat([data, categories], axis=1)
    row = data.sum().to_dict()
    predicts = []
    count = row["count"]
    if row["Опоздание"]/count > 0.2:
        predicts.append("Ученики опаздывают")
    if row["Реклама и спам"]/count > 0.15:
        predicts.append("Ученики общаются на отвлеченные темы, не заинтересованы")
    #if row["Выполнение задания"] > 1:
    #   predicts.append("Ученики выполняют небольшие задания преподавателя")
    if row["Вежливость"]/count > 0.2:
        predicts.append("Ученики вежливы друг с другом и преподавателем")
    if row["Технические проблемы"] > 1:
        predicts.append("Во время вебинара были техничесике неполадки")
    if row["Оскорбления и конфликты"] > 0:
        predicts.append("Есть токсичные ученики, нужно следить")
    if row["Помощь и понимание"]/count > 0.2:
        predicts.append("Сильная взаимопомощь в команде вебинара")
    if row["Хорошее объяснение материала"]/count > 0.3:
        predicts.append("Вебинар оставил хорошее впечатление")
    if row["Плохое объяснение материала и сложность"]/count > 0.2:
        predicts.append("Преподаватель плохо объясняет или тема сложная")
    if data['Время от начала урока'].max() < 10:
        predicts.append("Вебинар закончился слишком рано. Вероятно произошли технические неполадки, либо пришло слишком мало учеников")

    colors = ["blue", "red", "black", "pink","magenta", "green", "grey", "yellow", "brown"]
    names = ["Вежливость", "Технические проблемы", "Хорошее объяснение материала", "Плохое объяснение материала и сложность", "Помощь и понимание", "Реклама и спам", "Оскорбления и конфликты", "Опоздание", "Выполнение задания"]

    x = [list(data[data["Category"] == category]['Время от начала урока']) for category in groupefewfs]

    plt.switch_backend("agg")
    fig, ax = plt.subplots(figsize=(20,15))


    ax.hist(x, bins=20, color=colors, stacked=True, label=names)
    ax.set_position([0.1,0.1,0.65,0.8])
    plt.xlabel("Время с начала занятия")
    plt.title(title)
    plt.ylabel("Количество сообщений")
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.savefig(path, format="jpg", dpi=70)

    return ', '.join(predicts)