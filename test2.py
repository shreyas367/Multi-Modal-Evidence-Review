import pandas as pd

# import ollama

# response = ollama.chat(
#     model="qwen2.5vl:3b",
#     messages=[
#         {
#             "role":"user",
#             "content":"What is 2+2?"
#         }
#     ]
# )

# print(response["message"]["content"])

# print(pd.read_csv("dataset/claims.csv").head(3))
# print(pd.read_csv("dataset/sample_claims.csv").head(3))
# print(pd.read_csv("dataset/user_history.csv").head(3))
# print(pd.read_csv("dataset/output.csv").head(3))

import pandas as pd

claims = pd.read_csv("dataset/claims.csv")
output = pd.read_csv("output.csv")

print("Claims:", len(claims))
print("Output:", len(output))


import pandas as pd

df = pd.read_csv("output.csv")

print(df.columns.tolist())


import pandas as pd

df = pd.read_csv("output.csv")

print(df["claim_status"].unique())
print(df["claim_status"].value_counts())
print(df["severity"].unique())
print(df["issue_type"].unique())


import pandas as pd

df = pd.read_csv("output.csv")

print(df["evidence_standard_met"].value_counts())
print(df["valid_image"].value_counts())
print(df["risk_flags"].value_counts().head(10))