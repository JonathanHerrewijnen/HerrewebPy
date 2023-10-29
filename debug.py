from herrewebpy.mlops import anomaly_scoring
import seaborn as sns

df = sns.load_dataset('iris')
anomaly_scoring.train_model(df)