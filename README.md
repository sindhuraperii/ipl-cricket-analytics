IPL CRICKET ANALYSIS _ A DATA SCIENCE PROJECT

A comprehensive data science project that analyzes Indian Premier League cricket matches and predicts match winners using machine learning.

Project Overview

This project analyzes over 283,000 cricket records from 19 years of IPL data to understand what factors lead to match victories. The analysis includes creating a SQL database, engineering 32 advanced features, training three different machine learning models, and generating professional visualizations and reports.

Key Features

The project includes a complete SQL database with 2,380 matches and 283,042 deliveries. It creates 32 engineered features from the raw data to help machine learning models make better predictions. Three different ML models are trained: Logistic Regression, Random Forest, and Gradient Boosting. The project generates 11 professional visualizations showing player awards, venue statistics, cities distribution, and model performance. Finally, a comprehensive Excel report with 10 sheets is created containing all analysis results and insights.

Results

The Random Forest model achieved the best accuracy of 48.95% with a precision of 0.4895 and recall of 0.4874. The Logistic Regression model achieved 48.53% accuracy, while the Gradient Boosting model achieved 46.85% accuracy.

Key Insights

AB de Villiers is the top player with 50 Player of Match awards. Mumbai Indians is the most active team with 282 matches. Eden Gardens is the most frequently used venue with 154 matches. Mumbai is the city with the most matches played. Teams choose to field 65.9% of the time after winning the toss. The most important features for predicting winners are wickets (29%), runs (21%), and cumulative team matches (20%).

Project Structure

The data folder contains raw datasets and processed, cleaned data. The src folder contains Python scripts for data preparation, loading data to SQL, exploratory analysis, feature engineering, ML model training, and Excel report generation. The models folder stores all trained machine learning models. The visualizations folder contains 11 charts and graphs. The reports folder contains the Excel analytics report. The sql folder contains SQL queries for data analysis. The notebooks folder contains analysis notebooks.

Quick Start

You need Python 3.8 or newer and pip installed on your computer.

To get started, clone the repository and navigate to the project directory. Then install all required packages using pip install. After installation, run the pipeline scripts in order: first prepare the data, then load it to the SQL database, run exploratory analysis, create engineered features, train the ML models, and finally generate the Excel report.

Visualizations Generated

The project creates 11 visualizations including a chart showing top players by Player of Match awards, toss decision distribution, most frequently used venues, matches by city, teams by batting appearances, teams by bowling appearances, matches over time, ML model performance comparison, confusion matrix for model predictions, ROC curves for model evaluation, and feature importance ranking.

Database Contents

The Matches table contains match information including match ID, date, batting team, bowling team, player of the match, toss winner, toss decision, venue, city, and season. The Deliveries table contains ball-by-ball information including match ID, innings number, over number, ball number, batter name, bowler name, runs scored, extras, and wicket information.

SQL Analysis

The project includes SQL queries to analyze the data. You can find queries to identify top teams by number of matches, top venues by frequency, player awards ranking, and other statistical analyses in the sql folder.

Engineered Features

The project creates 32 new features from the raw data. Date-based features include year, month, day of week, and quarter. Toss-based features include whether the team won the toss, whether they chose to bat, and the toss decision encoded as a number. Team statistics features track matches played and player of match awards. Deliveries aggregation features include maximum overs, total runs, total extras, and total wickets. Additional features track unique batters and bowlers, venue statistics, season information, and historical cumulative matches for both teams.

Reports

The Excel report contains 10 sheets. The Executive Summary sheet provides an overview and key metrics. The EDA Summary sheet contains dataset statistics. The Key Insights sheet summarizes main findings. Additional sheets show top players, top venues, top cities, model results, sample engineered features, data dictionary, and methodology explanation.

Machine Learning Pipeline

The project follows a standard ML pipeline. First, data is loaded and cleaned. Then 32 advanced features are engineered from the raw data. The data is split into 80 percent training and 20 percent testing sets. Features are scaled using StandardScaler normalization. Three different models are trained: Logistic Regression, Random Forest, and Gradient Boosting. Model performance is evaluated using accuracy, precision, recall, F1-score, and AUC metrics. Finally, performance charts are generated for visualization.

Technologies Used

The project uses Python 3.13 as the programming language. Pandas is used for data manipulation and analysis. NumPy is used for numerical computing. Scikit-learn provides the machine learning models. Matplotlib and Seaborn are used for data visualization. SQLite stores the database. Openpyxl generates the Excel reports.

Dataset Information

The data comes from the Kaggle IPL Dataset covering 2008-2025. It contains 283,678 total records across 2,380 matches. The data spans from 2008 to 2026 with 283,042 deliveries. There are 19 unique teams, 59 unique venues, 719 unique batters, and 564 unique bowlers.

Model Performance

The best model is Random Forest with 48.95% accuracy, 0.4895 precision, 0.4874 recall, 0.4884 F1-score, and 0.4850 AUC. The top 5 most important features are batting team cumulative matches at 10.13%, bowling team cumulative matches at 10.13%, total runs at 9.09%, total extras at 7.55%, and batting matches played at 6.91%.

Future Improvements

The project can be enhanced with real-time match predictions, detailed player performance analytics, team strategy analysis, venue-specific prediction models, a web dashboard using Flask or Streamlit, deep learning models using LSTM or CNN, an API for making predictions, and mobile app integration.

Author

This project was created by Gayathri Sindhura Peri as a data science portfolio project.
