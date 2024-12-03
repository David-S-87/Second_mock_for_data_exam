# recomendation_system.py

# Import the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from data.data_preprocessing_package import (create_connection)


'''
Load Clustered Data:

Retrieve customer cluster labels from the MySQL database or clustering results.
Customer Similarity Matching:

Create a function to find similar customers within the same cluster.
Match based on attributes like purchase history or product categories.
Recommendation Logic:

Recommend products that similar customers have purchased but the target customer hasn’t.
Implement a scoring system to rank recommendations.
Modular Functions:

Define recommend() and match_customers() functions with clear docstrings.
Ensure easy integration with other parts of the project.
Exception Handling:

Handle cases where customer data or recommendations are unavailable.
Provide fallback messages or default recommendations.
'''

# function to create a dataframe of products purchased by customers from the path specified
def create_products_df(path):
    # load the products data from the csv file at the specified path
    products_df = pd.read_csv(path)
    return products_df
    

# function to load clustered data
def load_clustered_data(path):
    # load the clustered data from the csv file at the specified path
    clustered_data = pd.read_csv(path)
    return clustered_data

# function to find similar customers within the same cluster
def match_customers(clustered_data, customer_id):
    # check if the customer_id exists in the clustered data
    if customer_id in clustered_data['customer_id'].values:
        # retrieve the cluster label of the target customer
        target_cluster = clustered_data[clustered_data['customer_id'] == customer_id]['cluster'].values[0]
        # filter customers in the same cluster as the target customer
        similar_customers = clustered_data[clustered_data['cluster'] == target_cluster]
        return similar_customers
    else:
        return None
    
# function to recommend products to the target customer based on similar customers' purchase history and the products they have bought
def recommend(clustered_data, similar_customers, target_customer_id, path):
    # check if there are similar customers in the same cluster
    if similar_customers is not None:
        # create a dataframe of products purchased by similar customers
        products_df = create_products_df(path)
        similar_customers_ids = similar_customers['customer_id'].values
        similar_products = products_df[products_df['customer_id'].isin(similar_customers_ids)]
        target_products = products_df[products_df['customer_id'] == target_customer_id]
        
        # find unique products purchased by similar customers but not by the target customer
        recommendations = similar_products[~similar_products['product_id'].isin(target_products['product_id'])]
        # calculate a score based on the frequency of purchase of each product
        recommendations = recommendations['product_id'].value_counts().reset_index()
        recommendations.columns = ['product_id', 'score']
        recommendations = recommendations.sort_values('score', ascending=False)
        return recommendations.values
    else:
        return None
    


    




    
# main function with exception handling
def main():
    try:
        path = r"C:\Users\david\BathUni\MA50290_24\practice_for_exam\data\data_frames\clustered_data.csv"
        clustered_data = load_clustered_data(path)

        # specify the target customer_id
        avaliable_customer_ids = clustered_data['customer_id'].values
        print(f"Available customer IDs: {avaliable_customer_ids}")
        target_customer_id = int(input("Enter the target customer ID: "))

        # find similar customers within the same cluster
        similar_customers = match_customers(clustered_data, target_customer_id)

        # recommend products to the target customer
        recommendations = recommend(clustered_data, similar_customers, target_customer_id, path)

        if recommendations is not None:
            print(f"Recommendations for Customer {target_customer_id}:")
            for product, score in recommendations:
                print(f"Product ID: {product}, Score: {score}")
        else:
            print("No recommendations available for the target customer.")
    except FileNotFoundError:
        print("Error: The specified file was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except KeyError as e:
        print(f"Error: Missing expected column in the data - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
