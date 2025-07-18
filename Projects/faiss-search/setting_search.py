import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Step 1: Define the feature/settings list
settings = [
    {
        "id": "wifi_settings",
        "title": "Wi-Fi Settings",
        "description": "Manage network connections, toggle Wi-Fi, and set up hotspots."
    },
    {
        "id": "display_brightness",
        "title": "Display and Brightness",
        "description": "Adjust screen brightness, night mode, and display timeout."
    },
    {
        "id": "privacy_permissions",
        "title": "Privacy and Permissions",
        "description": "Control app permissions and privacy settings."
    },
    {
        "id": "sound_settings",
        "title": "Sound Settings",
        "description": "Manage volume, ringtones, and notification sounds."
    },
    {
        "id": "battery_optimization",
        "title": "Battery Optimization",
        "description": "Extend battery life and manage background activity."
    }
]

# Step 2: Embed titles + descriptions
texts = [s['title'] + " " + s['description'] for s in settings]
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts, convert_to_numpy=True).astype('float32')

# Step 3: Normalize for cosine similarity
faiss.normalize_L2(embeddings)

# Step 4: Create FAISS index and add embeddings
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # IP = inner product for cosine if normalized
index.add(embeddings)

# Step 5: Save the index (optional)
faiss.write_index(index, "settings_index.faiss")

# Step 6: Accept user query and embed
query = input("Type your setting-related search: ")
query_embedding = model.encode([query], convert_to_numpy=True).astype('float32')
faiss.normalize_L2(query_embedding)

# Step 7: Perform search
top_k = 3
scores, indices = index.search(query_embedding, top_k)

# Step 8: Display results
print("\nTop Matches:")
for i, idx in enumerate(indices[0]):
    print(f"\nMatch {i+1}")
    print(f"Title: {settings[idx]['title']}")
    print(f"Description: {settings[idx]['description']}")
    print(f"Similarity Score: {scores[0][i]:.3f}")