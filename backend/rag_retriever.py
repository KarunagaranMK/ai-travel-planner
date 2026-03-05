import os
import pandas as pd

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


def load_vector_store():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    csv_path = os.path.join(
        BASE_DIR,
        "AI_Travel_Planner_Dataset_500_Records.csv"
    )

    # Load dataset
    df = pd.read_csv(csv_path)

    documents = []

    for _, row in df.iterrows():
        # Derive a daily cost proxy
        daily_cost = int(row['Total_Cost']) // int(row['Days']) if int(row['Days']) > 0 else int(row['Total_Cost'])
        content = f"""
Destination: {row['Destination']}
Avg Daily Cost: {daily_cost}
Temperature: {row['Temperature_Range']}
"""

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "destination": row["Destination"],
                    "daily_cost": daily_cost,
                    "avg_temp": row["Temperature_Range"]
                }
            )
        )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(documents, embeddings)

    return vectorstore