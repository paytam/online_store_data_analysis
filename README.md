# DATA ANALYSIS PROJECT
In this project I try to read the dataset from [kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset).


## About Dataset

### Abstract: 
A real online retail transaction data set of two years.

### Data Set Information:
This Online Retail II data set contains all the transactions occurring for a UK-based and registered, non-store online retail between 01/12/2009 and 09/12/2011.The company mainly sells unique all-occasion gift-ware. Many customers of the company are wholesalers.

### Attribute Information:
- **InvoiceNo**: Invoice number. Nominal. A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'c', it indicates a cancellation.
- **StockCode:** Product (item) code. Nominal. A 5-digit integral number uniquely assigned to each distinct product.
- **Description:** Product (item) name. Nominal.
- **Quantity:** The quantities of each product (item) per transaction. Numeric.
- **InvoiceDate:** Invice date and time. Numeric. The day and time when a transaction was generated.
- **UnitPrice:** Unit price. Numeric. Product price per unit in sterling (Â£).
- **CustomerID:** Customer number. Nominal. A 5-digit integral number uniquely assigned to each customer.
- **Country:** Country name. Nominal. The name of the country where a customer resides.

## HOW TO CREATE ENVIRONMENT
In order to run the application, you can use virtual environment

```python
python -m venv venv
```
then activate the environment.
in windows:

```cmd
.\venv\Scripts\activate.bat
```
in linux
```bash
source ./venv/bin/activate
```
then install the required packages

```cmd
pip install -r requirements.txt -U
```

then simply run src/main.py
```cmd
python main.py
```