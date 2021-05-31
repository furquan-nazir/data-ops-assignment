# Data Ops Assignment

This assignment will simulate a scenario where we have data from different departments stored in multiple formats and storage methods.
We include a mock.py file that you can use to mock an AWS account with this assignment's data.

## Data

**Defects:**
Excel file sent to you by customer service with the list of products that customers reported defects.
**Plant:**
CSV files stored on S3 with data collected when producing the products.
**Users:**
Customer information stored in DynamoDB.

Based on the provided data, we want to get more insights regarding product defects.
Please complete the following tasks:

1. Read the multiple data sources and displays the defects, plant, and user data in a single view.
2. Calculate basic statistics of the data (count, mean, std, etc.) and examine data and state your observations.
3. Select columns that will probably be important to predict the cause of defects.
4. If you removed columns, explain why you removed those.
5. Identify what is causing the defects.

**Bonus challenge:**

1. Build a machine learning model to predict products with defects.
2. Describe hyper-parameters in your model and how you would change them to improve the performance of the model.
3. What is regularization? What is the regularization parameter in your model?

Our marketing team would like to get more insights regarding the data we have to do targeting advertisement.
They raised the following questions:

1. Is there a relation between the color of the part and the car color or model?
2. In the user database, we have the part color name. In the plant, we have the part color Hex. Create a view that relates which parts a customer might have bought based on the relation between the color Hex and the color name.
