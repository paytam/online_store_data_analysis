from utilities.pandas_helper import  PandasHelper

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    p:PandasHelper=PandasHelper(file_path="../dataset/dataset.xlsx")
    print(p.columns)

