from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_content",
    description="Reads the content of a document and return in string.", 
)
def read_document(
    doc_id: str = Field(description="The id of the document to read.")
):
    if doc_id not in docs:
        return f"Document with id '{doc_id}' not found."
    return docs[doc_id]

@mcp.tool(
    name="edit_doc_content",
    description="Edits the content of a document and return the new string.", 
)
def edit_document(
    doc_id: str = Field(description="The id of the document to edit."),
    old_content: str = Field(description="The old content to be replaced."),
    new_content: str = Field(description="The new content to replace the old content.")
):
    if doc_id not in docs:
        return f"Document with id '{doc_id}' not found."
    docs[doc_id] = new_content
    return f"Document with id '{doc_id}' has been updated."

@mcp.resource(
        "docs://dcouments",
        mime_type="application/json",
)
def list_documents() -> list[str]:
    return list(docs.keys())    

@mcp.resource(
        "docs://documents{doc_id}",
        mime_type="text/plain",
)
def get_document_content(doc_id: str) -> str:
    if doc_id not in docs:
        return f"Document with id '{doc_id}' not found."
    return docs[doc_id]

    # TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
