# clustering_analysis.py

# Import the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


from data.data_preprocessing_package import (normalise_data)


# function to perfomr PCA on the dataframe
def perform_pca(dataframe, n_components):
    pca = PCA(n_components=n_components)
    pca.fit(dataframe)
    pca_data = pca.transform(dataframe)
    return pca_data

# function to plot the explained variance to determine the optimal number of principal components
def plot_explained_variance(dataframe):
    pca = PCA()
    pca.fit(dataframe)
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.title('Explained Variance by Number of Components')
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance')
    plt.show()

# kmeans clustering function
def kmeans_clustering(dataframe, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(dataframe)
    return kmeans.labels_

# function to Plot customer clusters in a 2D space using Matplotlib
def plot_clusters(dataframe, labels):
    pca_data = perform_pca(dataframe, 2)
    plt.scatter(pca_data[:, 0], pca_data[:, 1], c=labels, cmap='viridis')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('Clusters')
    plt.show()  


# main function with exception handling
def main():
    try:
        data_frames_path = "C:\\Users\\david\\BathUni\\MA50290_24\\practice_for_exam\\data\\data_frames"
        # load the customers and transactions dataframes from the data_frames_path
        customers_df = pd.read_csv(f"{data_frames_path}/customers.csv")
        transactions_df = pd.read_csv(f"{data_frames_path}/transactions.csv")
     
        # Merge the two dataframes on the customer_id column
        merged_df = pd.merge(customers_df, transactions_df, on="customer_id")

        # normalise the data using the normalise_data function
        normalised_df = normalise_data(merged_df, 'total_amount')

        # print the columns of the normalised dataframe
        print(normalised_df.columns)



        # one hot encode non numerical columns
        normalised_df = pd.get_dummies(normalised_df, columns=['name', 'email', 'signup_date', 'transaction_date'])

        # Plot the explained variance to determine the optimal number of principal components.
        plot_explained_variance(normalised_df)

        # perform PCA on the normalised data with the optimal number of components
        pca_data = perform_pca(normalised_df, 10)

        # Perform kmeans clustering on the PCA data
        labels = kmeans_clustering(pca_data, 3)

        # Add the labels to the dataframe and save it to a csv file in the data_frames_path
        normalised_df['cluster'] = labels
        normalised_df.to_csv(f"{data_frames_path}/clustered_data.csv", index=False)


        # Plot the clusters
        plot_clusters(pca_data, labels)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except pd.errors.EmptyDataError as e:
        print(f"Empty data error: {e}")
    except KeyError as e:
        print(f"Key error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")





if __name__ == "__main__":
    main()

