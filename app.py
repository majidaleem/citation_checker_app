import streamlit as st
import re
import fitz  # PyMuPDF
from docx import Document
from rispy import load as load_ris
from apa_citation_generator import generate_apa_from_ris

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(uploaded_file):
    document = Document(uploaded_file)
    return " ".join(para.text for para in document.paragraphs)

def extract_citations(text):
    matches = re.findall(r'\(([^)]+?,\s*\d{4})\)', text)
    return set(re.sub(r'et al\.?', '', m).strip() for m in matches)

def main():
    st.title("📚 Citation Checker: Match Your Citations to RIS")

    st.markdown("Upload a `.docx` or `.pdf` file and a `.ris` file.")

    doc_file = st.file_uploader("Upload Document (.docx or .pdf)", type=["docx", "pdf"])
    ris_file = st.file_uploader("Upload RIS File (.ris)", type=["ris"])

    if doc_file and ris_file:
        if doc_file.name.endswith(".docx"):
            text = extract_text_from_docx(doc_file)
        elif doc_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(doc_file)
        else:
            st.error("Unsupported file type.")
            return

        citations_in_text = extract_citations(text)

        ris_data = load_ris(ris_file)

        ris_map = {}
        for entry in ris_data:
            authors = entry.get('authors', ['Unknown'])
            year = entry.get('year', 'n.d.')
            author = authors[0].split(',')[0] if authors else 'Unknown'
            key = f"{author} {year}"
            ris_map[key] = entry

        matched = {k: ris_map[k] for k in citations_in_text if k in ris_map}
        unmatched = [k for k in citations_in_text if k not in ris_map]

        st.subheader("✅ APA-formatted Bibliography")
        apa_bib = generate_apa_from_ris(matched.values())
        for ref in apa_bib:
            st.markdown(f"- {ref}")

        st.download_button("📥 Download APA Bibliography", "\n".join(apa_bib), file_name="apa_references.txt")

        st.subheader("⚠️ Unmatched In-text Citations")
        if unmatched:
            for item in unmatched:
                st.write(f"- {item}")
            st.download_button("📥 Download Unmatched Citations", "\n".join(unmatched), file_name="unmatched_citations.txt")
        else:
            st.success("All citations matched!")

if __name__ == '__main__':
    main()
