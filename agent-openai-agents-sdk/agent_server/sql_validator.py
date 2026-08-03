import re

ALLOWED_TABLES = {
    "rag_demo.rag.drug_events",
    "rag_demo.rag.drug_event_drugs",
    "rag_demo.rag.drug_event_reactions",
}

FORBIDDEN = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "MERGE",
    "GRANT",
    "REVOKE",
}


def validate(sql: str) -> str:

    sql = sql.strip()

    upper = sql.upper()

    if not upper.startswith("SELECT"):
        raise ValueError("Only SELECT statements are allowed.")

    for keyword in FORBIDDEN:
        if re.search(rf"\b{keyword}\b", upper):
            raise ValueError(f"{keyword} statements are not allowed.")

    lower = sql.lower()

    table_pattern = r"rag_demo\.rag\.[a-zA-Z0-9_]+"

    referenced_tables = set(re.findall(table_pattern, lower))

    if not referenced_tables:
        raise ValueError(
            "No approved Unity Catalog tables were referenced."
        )

    invalid_tables = referenced_tables - ALLOWED_TABLES

    if invalid_tables:
        raise ValueError(
            f"Queries against {invalid_tables} are not permitted."
        )

    return sql