import streamlit as st
# ChromaDB is our vector database
import chromadb
# SentenceTransformer is for turning text into numerical vectors (embeddings)
from sentence_transformers import SentenceTransformer
# Pandas is for handling data in a structured way (like a spreadsheet)
import pandas as pd
# UUID is to create unique IDs for our database entries
import uuid

# --- 1. Educational Content ---
# In a real application, this would come from a larger database or multiple files.
# For this example, we define it directly in the code.
# --- 1. Educational Content (EXPANDED AND IMPROVED) ---
educational_content = [
    {
        "id": "py001",
        "topic": "Python Basics",
        "level": "Beginner",
        "content": "Python is an interpreted, high-level and general-purpose programming language. Its design philosophy emphasizes code readability with its notable use of significant whitespace."
    },
    {
        "id": "py002",
        "topic": "Python Variables",
        "level": "Beginner",
        "content": "A variable in Python is a symbolic name that is a reference or pointer to an object. Once an object is assigned to a variable, you can refer to the object by that name. Variables do not need to be declared with any particular type."
    },
    {
        "id": "py003",
        "topic": "Python Data Types",
        "level": "Beginner",
        "content": "Variables can store data of different types. Common data types in Python include Integers (int), Floating-Point Numbers (float), Strings (str), and Booleans (bool). The type of a variable is determined at runtime."
    },
    {
        "id": "py004",
        "topic": "Using Variables in Operations",
        "level": "Beginner",
        "content": "You can perform mathematical operations with variables that store numbers, like addition and subtraction. You can also concatenate strings using the plus operator. For example: x = 10, y = 20, z = x + y."
    },
    {
        "id": "py005",
        "topic": "Python Lists",
        "level": "Intermediate",
        "content": "A list is a data structure in Python that is a mutable, or changeable, ordered sequence of elements. Each element or value that is inside of a list is called an item. Lists are defined with square brackets []."
    },
    {
        "id": "py006",
        "topic": "Python Functions",
        "level": "Intermediate",
        "content": "A function is a reusable block of code which only runs when it is called. You can pass data, known as parameters or arguments, into a function. A function can return data as a result using the 'return' keyword."
    },
    {
        "id": "py007",
        "topic": "Function Parameters",
        "level": "Intermediate",
        "content": "Parameters are variables listed inside the parentheses in the function definition. Arguments are the values that are sent to the function when it is called. These values are assigned to the parameter variables."
    },
    {
        "id": "py008",
        "topic": "Python Classes",
        "level": "Advanced",
        "content": "Python is an object-oriented programming language. Almost everything in Python is an object, with its properties and methods. A Class is like an object constructor, or a 'blueprint' for creating objects."
    }
]

# Convert our list of content into a pandas DataFrame for easier handling
df = pd.DataFrame(educational_content)


# --- 2. Initialize RAG Components (Model and Vector DB) ---
# Use Streamlit's cache to avoid reloading the model every time the app reruns
@st.cache_resource
def get_embedding_model():
    print("Loading embedding model...")
    # This model is small and fast, great for demos.
    return SentenceTransformer('all-MiniLM-L6-v2')

model = get_embedding_model()

# Use Streamlit's cache to avoid re-initializing the database on every interaction
@st.cache_resource
def get_chroma_client():
    print("Initializing ChromaDB client...")
    # This creates a temporary, in-memory database.
    return chromadb.Client()

client = get_chroma_client()

# Create a "collection" which is like a table in a traditional database.
collection_name = "educational_content_collection"
# If the collection already exists from a previous run, delete it to start fresh.
if collection_name in [c.name for c in client.list_collections()]:
    client.delete_collection(name=collection_name)

# Create the collection.
collection = client.create_collection(name=collection_name)


# --- 3. Process and Store Content in the Vector Database ---
# This part runs only once to populate the database with our content.
# Get the text content for embedding
documents = df['content'].tolist()
# Get the other data (topic, level) as metadata
metadatas = df.drop(columns=['content']).to_dict('records')
# Create unique IDs for each entry, which ChromaDB requires.
ids = [str(uuid.uuid4()) for _ in range(len(documents))]

# Add the content, metadata, and IDs to the collection.
# The model automatically converts the 'documents' into vector embeddings here.
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)


# --- 4. Streamlit User Interface ---
st.title("🎓 Personalized Learning Path Generator")

st.write("""
This demo uses a Retrieval-Augmented Generation (RAG) system to suggest a personalized learning path.
Select your experience level and ask a question about a topic you want to learn.
""")

# --- Create input widgets for the user ---
st.subheader("Step 1: Tell us about yourself")

# Dropdown menu for the user to select their level
student_level = st.selectbox(
    "Select your experience level:",
    ("Beginner", "Intermediate", "Advanced")
)

# Text box for the user to enter their question
query = st.text_input(
    "What topic do you want to learn about?",
    "How do I create a function in Python?"
)

st.subheader("Step 2: Generate your path")

# --- 5. Generate Learning Path on Button Click ---
if st.button("🚀 Generate My Learning Path"):
    # Use the collection to find the most relevant documents based on the user's query
    results = collection.query(
        query_texts=[query],
        n_results=5  # Ask for the top 5 most similar documents
    )

    st.subheader("📚 Your Recommended Learning Path:")

    if not results['documents'][0]:
        st.warning("No relevant content found for your query. Try rephrasing it.")
    else:
        # This is the personalization part! We filter the retrieved results.
        learning_path = []
        retrieved_metadatas = results['metadatas'][0]
        retrieved_documents = results['documents'][0]

        for i in range(len(retrieved_metadatas)):
            meta = retrieved_metadatas[i]
            doc = retrieved_documents[i]
            
            # Simple filtering logic based on user's selected level
            if student_level == "Beginner" and meta['level'] == "Beginner":
                learning_path.append((meta, doc))
            elif student_level == "Intermediate" and meta['level'] in ["Beginner", "Intermediate"]:
                learning_path.append((meta, doc))
            elif student_level == "Advanced": # Advanced users get all relevant results
                 learning_path.append((meta, doc))

        if not learning_path:
            st.warning("Found relevant topics, but they don't match your selected skill level. Try selecting a different level or broadening your question.")
        else:
            # Display the filtered and ordered learning path
            for i, (meta, doc) in enumerate(learning_path):
                with st.expander(f"**Step {i+1}: {meta['topic']}** (Level: {meta['level']})"):
                    st.write(doc)
            st.success("End of your personalized learning path!")