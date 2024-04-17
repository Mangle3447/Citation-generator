from flask import Flask, request
from flask_restx import Api, Resource, fields
from datetime import datetime

# Create a Flask application instance
app = Flask(__name__)
api = Api(app, version='1.0', title='Citation Tool API',
          description='A simple Citation Generator API')

# Create a namespace
ns = api.namespace('citations', description='Citation operations')

# Model for input data
citation_model = api.model('CitationRequest', {
    'type': fields.String(required=True, description='Type of citation', enum=['book', 'online_journal', 'print_journal', 'online_web_page', 'online_blog', 'online_social_media_post']),
    'author': fields.String(required=True, description='Author of the work'),
    'year': fields.String(required=True, description='Year of publication'),
    'chapter_title': fields.String(description='Title of the chapter', required=False),
    'editor': fields.String(description='Editor of the book', required=False),
    'book_title': fields.String(description='Title of the book', required=False),
    'city': fields.String(description='City of publication', required=False),
    'publisher': fields.String(description='Publisher of the work', required=False),
    'page_range': fields.String(description='Page range', required=False),
    'journal_name': fields.String(description='Name of the journal', required=False),
    'volume': fields.String(description='Volume of the journal', required=False),
    'issue': fields.String(description='Issue of the journal', required=False),
    'doi': fields.String(description='DOI of the journal article', required=False),
    'url': fields.String(description='URL of the online source', required=False),
    'date': fields.String(description='Date of the online source', required=False),
    'username': fields.String(description='Username for social media posts', required=False),
    'website_name': fields.String(description='Website name for social media posts', required=False),
    'title': fields.String(description='Title or text of the post', required=False),
    'accessed_date': fields.String(description='Date when the source was accessed', required=False)
})

# Define the POST endpoint
@ns.route('/')
class Citation(Resource):
    @ns.expect(citation_model, validate=True)
    def post(self):
        data = request.json
        citation_type = data['type']
        in_text_citation = generate_in_text_citation(data)
        full_citation = format_citation(citation_type, data)
        return {
            "IN TEXT CITATION": in_text_citation,
            "HARVARD CITATION": full_citation
        }

def generate_in_text_citation(data):
    author_surname = data.get('author', 'NOT FOUND').split(',')  
    year = data.get('year', 'NOT FOUND')
    return f"({author_surname[0] if len(author_surname) > 0 else 'NOT FOUND'}, {year})"

def format_citation(citation_type, data):
    # Your existing formatting logic here
    pass  # Implement as shown in your earlier code snippet

if __name__ == '__main__':
    app.run
