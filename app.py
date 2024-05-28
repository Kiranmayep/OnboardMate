import streamlit as st
import os
import shutil
from chatbot import handle_user_query, create_database, save_file_to_db

# Define the database path
DB_PATH = os.path.join("database", "chatbot.db")


def main():
    create_database()
    st.title("Project Chatbot")

    # Add option to upload individual files
    uploaded_files = st.file_uploader("Upload Project Files", type=["txt", "py", "md", "jpg", "png", "zip"],
                                      accept_multiple_files=True)

    if st.button("Upload Files"):
        if uploaded_files:
            with st.spinner("Processing files..."):
                for uploaded_file in uploaded_files:
                    if uploaded_file.type == "application/zip":
                        process_zip_folder(uploaded_file)
                    else:
                        save_file_to_db(uploaded_file)
            st.success("Files uploaded and processed successfully")
        else:
            st.error("Please upload at least one file.")

    st.header("Chatbot Interface")
    query = st.text_input("Ask your question about the project files:")
    if st.button("Ask"):
        if query:
            answer = handle_user_query(query)
            st.write("Answer:", answer)
        else:
            st.error("Please enter a question.")


def process_zip_folder(uploaded_folder):
    folder_path = "uploaded_folder.zip"
    with open(folder_path, "wb") as f:
        f.write(uploaded_folder.getbuffer())

    shutil.unpack_archive(folder_path, "temp_folder")

    for root, dirs, files in os.walk("temp_folder"):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                file_content = f.read()
                file_name = os.path.basename(file_path)
                file_type = 'text/plain' if file_name.endswith('.txt') else 'text/x-python' if file_name.endswith(
                    '.py') else 'image/jpeg' if file_name.endswith('.jpg') else 'image/png' if file_name.endswith(
                    '.png') else 'application/octet-stream'
                save_file_to_db(file_content, file_name, file_type)

    shutil.rmtree("temp_folder")
    os.remove(folder_path)


if __name__ == "__main__":
    main()
