🎓 Educational Learning Path Generator using RAG

This project is a **Retrieval-Augmented Generation (RAG)** based personalized learning path generator. It helps users get relevant Python educational content based on their query and experience level using **Streamlit**, **ChromaDB**, and **SentenceTransformers**.

🚀 Deployment Link

🔗 [Live App on Streamlit](https://akshaya-mandepudi-educational-learning-path-rag.streamlit.app/)

> ⚠️ *Note: The app may show a black screen temporarily on Streamlit Cloud due to limitations in loading the `chromadb` module online. However, the code runs successfully in the local environment.*

 📂 Project Structure
learning-path-project-main/
│
├── app.py                  # Streamlit app
├── requirements.txt        # List of dependencies
├── README.md               # Project description and setup guide
├── .gitignore              # Git ignored files
```

💡 Summary of My Approach

This project uses a **Retrieval-Augmented Generation system** to deliver personalized learning resources. The user selects their Python proficiency level and enters a query, and the app responds with a structured learning path by matching vector embeddings.

🔍 Features:

* Stores educational content using ChromaDB
* Converts user input into vector using `sentence-transformers`
* Filters results based on user skill level
* Shows results in an interactive and readable way using Streamlit

⚙️ Technologies Used:

* Python
* Streamlit
* ChromaDB
* SentenceTransformers
* Pandas
* UUID

🧠 Assumptions:

* Only Python content is used
* Educational content is small and preloaded in the app
* Users are expected to enter topic-related queries

🚧 Known Issues:

* Streamlit Cloud has limitations with `chromadb`, leading to a temporary black screen.
* Works perfectly on local environments using the below instructions.

🛠️ Setup / Run Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/Akshaya-Mandepudi/Educational-Learning-Path-RAG.git
   cd Educational-Learning-Path-RAG
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```
   
📁 Deliverables for Assignment

* ✅ GitHub Repository (public): [Akshaya-Mandepudi/Educational-Learning-Path-RAG](https://github.com/Akshaya-Mandepudi/Educational-Learning-Path-RAG)
* ✅ Deployment Link: [Live on Streamlit](https://akshaya-mandepudi-educational-learning-path-rag.streamlit.app/)
* ✅ Source Code ZIP file (attached in email submission)
* ✅ README with deployment link, setup steps, summary, and assumptions
