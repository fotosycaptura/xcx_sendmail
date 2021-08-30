import pandas as pd

class datos_csv():
    def get_rectores():
        rectores = pd.read_csv('./datos/datos.csv', header = 0,delimiter =';', encoding='utf-8-sig', index_col=0)
        return rectores 