import streamlit as st
from src.rag import ask_question

st.set_page_config(
    page_title="TechNova HR Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Sidebar ----------------

st.sidebar.title("🤖 TechNova HR Assistant")

st.sidebar.success("AI Engineering RAG Project")

st.sidebar.markdown("""
### Technologies
- 🐍 Python
- 🔗 LangChain
- 🧠 ChromaDB
- 🤗 Hugging Face Embeddings
- ⚡ Groq Llama 3
- 🎨 Streamlit

---

### Example Questions

- How many vacation days do employees receive?
- Can I reuse my password?
- Do I need to use a VPN?
- What holidays are paid?
- How do I submit expenses?
""")
st.sidebar.markdown("---")

st.sidebar.metric("Documents", "10")
st.sidebar.metric("Vector Database", "ChromaDB")
st.sidebar.metric("LLM", "Llama 3 70B")
st.sidebar.metric("Embedding Model", "MiniLM-L6-v2")

# ---------------- Main Page ----------------

st.title("🤖 TechNova HR Policy Assistant")

st.markdown("""
Welcome to the **TechNova HR Policy Assistant**.

This AI assistant uses **Retrieval-Augmented Generation (RAG)** to answer employee questions based on company policy documents.

Ask a question below to get started.
""")

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask a question about company policies...")

if question:

    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Searching company policies..."):
            answer, sources = ask_question(question)

        st.markdown(answer)

        with st.expander("📄 Sources Used"):
            for source in sources:
                filename = source.split("\\")[-1].split("/")[-1]
                st.write(f"📄 {filename}")

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )