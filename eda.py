import pandas as pd

# Load dataset
df = pd.read_csv("dataset/processed/defect_dataset.csv")

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== SHAPE =====")
print(df.shape)

print("\n===== COLUMNS =====")
print(df.columns)

print("\n===== INFO =====")
df.info()

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== LABEL DISTRIBUTION =====")
print(df["label"].value_counts())

print("\n===== UNIQUE LABELS =====")
print(df["label"].nunique())
print(df["label"].unique())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATES =====")
print("Duplicate rows:", df.duplicated().sum())

print("\n===== CODE LENGTH =====")
df["code_length"] = df["code"].str.len()

print(df["code_length"].describe())

print("\n===== AVERAGE CODE LENGTH BY LABEL =====")
print(df.groupby("label")["code_length"].mean())

print("\n===== SAMPLE CODE =====")
print(df.iloc[0]["code"])

print("\n===== LABEL DISTRIBUTION =====")
print(df["label"].value_counts())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

print("\n===== CODE LENGTH BY LABEL =====")
print(
    df.groupby("label")["code_length"]
    .agg(["count", "mean", "min", "max"])
)

print("\n===== SHORTEST CODE =====")
print(df.loc[df["code_length"].idxmin(), "code"])

print("\n===== LONGEST CODE =====")
print(df.loc[df["code_length"].idxmax(), "code"])