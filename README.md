# B5W3: End-to-End Insurance Risk Analytics & Predictive Modeling
## Business Objective
- AlphaCare Insurance Solutions (ACIS) is committed to developing cutting-edge risk and predictive analytics in the area of **car insurance** planning and marketing in South Africa.
- I recently joined the data analytics team as marketing analytics engineer, and my first project is to analyse historical insurance claim data.
- The objective of this analyses is to help optimise the marketing strategy as well as discover “low-risk” targets for which the premium could be reduced, hence an opportunity to attract new clients
## Here is how I do this task as *Data Analyst*
- Envirnment setup
    - Python
    - Git and Github
    - Virtual envirnment
    - Python package instalition
        - `pip install pandas`
        - `pip install matplotlib`
        - `pip install seaborn`
        - `pip install scikit-learn`
        - `pip install xgboost`
    - Folder structure
        - data
        - notbooks
        - scripts
- The first task is **EDA** as usual task
    - Convert .txt to .csv
        `converter = DataConverter(input_file_path, output_file_path)`
    - The given data is in txt format so, better to convert into csv to suit for pandas manipulation
    - Then read as pandas and explor the data
        - `df  = pd.read_csv('../data/MachineLearningRating_v3.csv', low_memory=False )`
        - `df.head()`
        - `df.columns.tolist()`
        - `df.dtypes`
        - `df.shape`
        - `df.info()`
        - `df.isnull().sum()`
        - `df.duplicated().sum()`
        - `df.describe()`
        - `loss_ratio_by_gender = df.groupby('Gender')[['TotalClaims', 'TotalPremium']].sum()`

- Hypothesis testing is the second task
- Model training and comparison is the last task
