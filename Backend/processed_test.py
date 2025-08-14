from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json


# Cleaning the scraped data ,flattening the json so it is easier to load using JSONloader
def flatten_json(input_file, output_file):
    flat_data = []
    with open(input_file, "r", encoding="utf-8") as f:
        dataa = json.load(f)
  
    for data in dataa[:]:
        title = data.get("title", "")
        full_text = data.get("full_text", "")
        url = data.get("url", "")
        page_content = []

        for section in data["sections"]:
            heading = section.get("heading", "")
            paragraphs = section.get("paragraphs", "")

            if paragraphs:
                combined = f"{heading}:{paragraphs}"
                page_content.append(combined)
            else:
                combined = f"{heading}"
                page_content.append(combined)

        p_cont = " ".join(page_content)

        flat_data.append(
            {
                "title": title,
                "page_content": f"{p_cont} {full_text}",
                "metadata": {"url": url},
            }
        )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(flat_data, f, indent=4, ensure_ascii=False)


# flatten_json('inventory_data.json', 'flattened_data_testing2.json')


# Keep the original URL from your metadata object creating a function as per langchain json loader documentation
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["url"] = record.get("metadata", {}).get("url", "")
    return metadata


loader = JSONLoader(
    file_path="flattened_data_testing2.json",
    jq_schema=".[]",
    content_key="page_content",  # This is where main content is stored
    metadata_func=metadata_func,
    text_content=False,
)

documents = loader.load()

# SPLITTING TEXT INTO CHUNKS
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, 
    chunk_overlap=80, 
    separators=["\n\n", "\n", ". ", " ", ""]
)
docs = splitter.split_documents(documents)
