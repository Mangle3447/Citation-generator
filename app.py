from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/generate-citation', methods=['POST'])
def generate_citation():
    data = request.json
    citation_type = data['type']
    in_text_citation = generate_in_text_citation(data)
    full_citation = format_citation(citation_type, data)
    response = f"IN TEXT CITATION: {in_text_citation}\nHARVARD CITATION: {full_citation}"
    return response, 200, {'Content-Type': 'text/plain; charset=utf-8'}

def generate_in_text_citation(data):
    # Generate in-text citation format (Author's surname, Year)
    author_surname = data.get('author', 'NOT FOUND').split(',')  # Assumes format "Surname, Initial"
    year = data.get('year', 'NOT FOUND')
    return f"({author_surname[0] if len(author_surname) > 0 else 'NOT FOUND'}, {year})"

def format_citation(citation_type, data):
    # Format the full Harvard citation based on the type
    if citation_type == 'book':
        return f"{data.get('author', 'NOT FOUND')} ({data.get('year', 'NOT FOUND')}) ‘{data.get('chapter_title', 'NOT FOUND')}’, in {data.get('editor', 'NOT FOUND')} (ed(s).) {data.get('book_title', 'NOT_FOUND')}. {data.get('city', 'NOT FOUND')}: {data.get('publisher', 'NOT FOUND')}, {data.get('page_range', 'NOT FOUND')}."
    elif citation_type == 'online_journal':
        return f"{data.get('author', 'NOT FOUND')} ({data.get('year', 'NOT FOUND')}) ‘{data.get('article_title', 'NOT FOUND')}’, {data.get('journal_name', 'NOT FOUND')}, {data.get('volume', 'NOT FOUND')}({data.get('issue', 'NOT FOUND')}), {data.get('page_range', 'NOT FOUND')}. DOI: {data.get('doi', 'NOT FOUND')}."
    elif citation_type == 'print_journal':
        return f"{data.get('author', 'NOT FOUND')} ({data.get('year', 'NOT FOUND')}) ‘{data.get('article_title', 'NOT FOUND')}’, {data.get('journal_name', 'NOT FOUND')}, {data.get('volume', 'NOT FOUND')}({data.get('issue', 'NOT FOUND')}), pp. {data.get('page_range', 'NOT FOUND')}."
    elif citation_type == 'online_web_page':
        accessed_date = datetime.now().strftime("%d %B %Y")
        return f"{data.get('author', 'NOT FOUND')} ({data.get('year', 'NOT FOUND')}) {data.get('page_title', 'NOT FOUND')}. Available at: {data.get('url', 'NOT FOUND')} (Accessed: {accessed_date})."
    elif citation_type == 'online_blog':
        return f"{data.get('author', 'NOT FOUND')} ({data.get('year', 'NOT FOUND')}) ‘{data.get('article_title', 'NOT FOUND')}’, {data.get('blog_name', 'NOT FOUND')}, {data.get('date', 'NOT FOUND')}. Available at: {data.get('url', 'NOT FOUND')} (Accessed: {data.get('accessed_date', 'NOT FOUND')})."
    elif citation_type == 'online_social_media_post':
        return f"{data.get('author', 'NOT FOUND')} [{data.get('username', 'NOT FOUND')}] ({data.get('year', 'NOT_FOUND')}) {data.get('title', 'NOT FOUND')} [{data.get('website_name', 'NOT FOUND')}] {data.get('date', 'NOT FOUND')}. Available at: {data.get('url', 'NOT FOUND')} (Accessed: {data.get('accessed_date', 'NOT FOUND')})."
    else:
        return "Citation format not implemented."

if __name__ == '__main__':
    app.run(debug=True)
