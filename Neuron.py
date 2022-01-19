import numpy as np
from sklearn.linear_model import LogisticRegression


# требует качественного обучения
def processing(new, x, y):
    model = LogisticRegression(solver='lbfgs', random_state=0).fit(x, y)
    new_x = new[3:]
    x.append(new_x)
    y.append(1)
    x = np.array(x)
    y = np.array(y)
    model.fit(x, y)
    mark = model.predict_proba(x)[-1][1]
    new.append(int(mark + (0.6 if mark > 0 else -0.6)))
    # threading.Thread(target=yandex, args=(new,)).start()
    return int(mark * 100)

# def yandex(new):
#    Y = yadisk.YaDisk(token="AQAAAAA7SpTSAAd8zbO0v4G6B0dHklAfN0lo13g")
#    with open("base.csv", mode="a", encoding='utf-8') as w_file:
#        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
#        file_writer.writerow(new)
#    Y.remove("base.csv", permanently=True)
#    Y.upload("base.csv", "base.csv")
