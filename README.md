# What needs:

= Collection and preparation of data - collect historical data about customer purchases (products, hour, amount, frequency, sales channels) and prepare them before analysis. =
= Customer segmentation – classify customers based on behavioral and demographic characteristics to identify different groups of buyers. = 
= Development of forecasting models – create and test machine learning algorithms to predict demand and the likelihood of repeat purchases. =
= Analysis of influencing factors – to identify key factors that influence product choice and customer behavior. = 
= Visualization of results – develop dashboards or reports to visually present management forecasts and recommendations. =
= Integrate results into business processes – implement a forecasting system to optimize inventory, create personalized promotions, and increase customer loyalty. =

# Todo
1. Collect and familiarize yourself with the dataset: Download the MovieLens dataset (e.g., ml-latest-small), study its structure, column descriptions, and overall amount of information.
2. Preliminary analysis and data cleaning (EDA): Perform exploratory data analysis to identify anomalies, missing values, and gain an initial understanding of the distribution of ratings. Ensure data integrity.
3. Feature engineering: Process categorical features (e.g., genres, which are represented as a string with separators) and convert them into a format suitable for modeling (e.g., one-hot encoding for genres).
4. Build a user-item matrix: Create a sparse matrix where rows are users, columns are movies, and values are ratings. This is the basis for further calculations.
5. Implement a recommendation model based on content-based filtering: Develop an algorithm that recommends movies similar to those liked by the user based on their attributes (e.g., genres).
6. Implementation of a recommendation model based on collaborative filtering: Implement an algorithm that finds users with similar tastes (User-User) or movies that are often rated together (Item-Item) using similarity metrics (cosine similarity, Pearson correlation).
7. Evaluating model quality: Use recommendation system evaluation metrics such as Precision@k, Recall@k, and RMSE (Root Mean Square Error) to quantitatively compare the effectiveness of the constructed models.
8. Visualization of results: Create visual graphs (e.g., histograms of rating distributions, heatmaps for movie similarity) to better represent the results of the analysis and the performance of the models.
9. Develop a prototype interface (optional, but highly recommended): Create a simple console interface or web application using Streamlit that allows you to enter a user ID and get a list of recommended movies.
10. Analysis of problems and limitations: Discuss issues such as cold start for new users or movies, and the curse of data sparsity.
