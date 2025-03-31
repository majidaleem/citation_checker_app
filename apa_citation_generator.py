def generate_apa_from_ris(entries):
    apa_entries = []
    for entry in entries:
        authors = entry.get('authors', [])
        year = entry.get('year', 'n.d.')
        title = entry.get('title', '[No title]')
        journal = entry.get('journal_name') or entry.get('secondary_title', '')
        volume = entry.get('volume', '')
        issue = entry.get('issue', '')
        pages = f"{entry.get('start_page', '')}-{entry.get('end_page', '')}".strip('-')
        doi = entry.get('doi', '')

        author_str = ', '.join(authors) if authors else 'Unknown'
        apa_entry = f"{author_str} ({year}). {title}. *{journal}*, {volume}({issue}), {pages}. {doi}".strip()
        apa_entries.append(apa_entry)
    return apa_entries
