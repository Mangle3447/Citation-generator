from flask_restx import Resource, Namespace, fields
from flask import request

api = Namespace('citations', description='Citation operations')

# Model for citation information
citation_model = api.model('CitationRequest', {
    'author': fields.String(required=True, description="Author's Last Name"),
    'year': fields.String(required=True, description="Year of Publication"),
    'title': fields.String(required=True, description="Title of Work"),
    'container': fields.String(description="Container of Work (e.g., journal name, book title)"),
    'location': fields.String(description="Location of Publication"),
    'publisher': fields.String(description="Publisher"),
    'page_range': fields.String(description="Page Range"),
    'url': fields.String(description="URL if available"),
    'accessed_date': fields.String(description="Date when the source was accessed")
})

@api.route('/generate-citation')
class Citation(Resource):
    @api.expect(citation_model, validate=True)
    def post(self):
        data = request.json
        try:
            in_text_citation = generate_in_text_citation(data)
            harvard_citation = generate_harvard_citation(data)
            return {
                "in_text_citation": in_text_citation,
                "harvard_citation": harvard_citation
            }, 200
        except Exception as e:
            api.abort(400, str(e))

def generate_in_text_citation(data):
    return f"({data['author'].split()[-1]}, {data['year']})"

def generate_harvard_citation(data):
    citation_format = "{author} ({year}) ‘{title}’, {container}, {location}: {publisher}, pp. {page_range}. Available at: {url} (Accessed: {accessed_date})."
    return citation_format.format(
        author=data.get('author', 'NOT FOUND'),
        year=data.get('year', 'NOT FOUND'),
        title=data.get('title', 'NOT FOUND'),
        container=data.get('container', 'NOT FOUND'),
        location=data.get('location', 'NOT FOUND'),
        publisher=data.get('publisher', 'NOT FOUND'),
        page_range=data.get('page_range', 'NOT FOUND'),
        url=data.get('url', 'NOT FOUND'),
        accessed_date=data.get('accessed_date', 'NOT FOUND')
    )

def configure_api(api):
    api.add_namespace(api)
