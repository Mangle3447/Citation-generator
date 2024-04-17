import logging
import os
from flask import Flask, request
from flask_restx import Api, Resource, fields
from datetime import datetime

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    
    # Setup logging to log unique citations to a file
    log_directory = os.path.join(app.instance_path, 'logs')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    logging.basicConfig(filename=os.path.join) ("C:\Users\matth\Downloads\VERTEXDOCS\Citation generator\Log_Directory\citations.log"), level=logging.INFO, format='%(asctime)s:%(message)s')
    
    log_file_path = os.path.join("C:\Users\matth\Downloads\VERTEXDOCS\Citation generator\Log_Directory\application.log")

    # Initialize Flask-RESTx
    api = Api(app, title='Citation Generator API', version='1.0', description='API for generating citations in various formats')
    
    # Namespace for Citations
    ns = api.namespace('citations', description='Citation operations')

    # Citation model
    citation_model = api.model('Citation', {
        'type': fields.String(required=True, description='Type of document'),
        'author': fields.String(required=True, description="Author's full name"),
        'year': fields.String(required=True, description='Year of publication'),
        'title': fields.String(required=True, description='Title of the document'),
        'container': fields.String(description='Container of work, e.g., journal name'),
        'location': fields.String(description='Location of publication'),
        'publisher': fields.String(description='Publisher'),
        'page_range': fields.String(description='Page range'),
        'url': fields.String(description='URL if available'),
        'accessed_date': fields.String(description='Date when the document was accessed')
    })

    @ns.route('/')
    class Citation(Resource):
        @api.expect(citation_model)
        def post(self):
            data = request.json
            if not data:
                api.abort(400, "No data provided")
            in_text_citation = f"({data.get('author', '').split(',')[0]}, {data.get('year', '')})"
            full_citation = generate_full_citation(data)
            log_citation(data['author'], full_citation)  # Log the unique full citation under the author
            return {'in_text_citation': in_text_citation, 'harvard_citation': full_citation}, 200

    def generate_full_citation(data):
        # Select citation type handler based on the 'type' field
        citation_handlers = {
            'book': generate_book_citation,
            'online_journal': generate_journal_citation,
            'print_journal': generate_journal_citation,
            'online_web_page': generate_webpage_citation,
            'online_blog': generate_blog_citation,
            'online_social_media_post': generate_social_media_citation
        }
        return citation_handlers.get(data['type'], lambda _: "Citation format not implemented.")(data)

    def log_citation(author, citation):
        """Logs a citation to a structured bibliography file grouped by author."""
        file_path = os.path.join("C:\Users\matth\Downloads\VERTEXDOCS\Citation generator\Log_Directory\Bibliography.txt")
        try:
            if not os.path.exists(file_path):
                with open(file_path, 'w'): pass  # Create the file if it does not exist
            with open(file_path, 'r+') as file:
                content = file.read()
                author_section = f"\n{author}\n"
                if author_section not in content:
                    file.write(author_section)
                if citation not in content:
                    file.write(f"({citation})\n")
                    logging.info("Logged a new citation for author: " + author)
        except Exception as e:
            logging.error("Failed to log citation: " + str(e))

    # Define citation generation for different types
    # Each function uses .get() method with default values to handle missing data gracefully
    def generate_book_citation(data):
        return (f"{data.get('author', 'NOT FOUND')} ({data.get('year', 'NOT FOUND')}) "
                f"‘{data.get('title', 'NOT FOUND')}’, in {data.get('container', 'NOT FOUND')} "
                f"(ed.) {data.get('publisher', 'NOT FOUND')}. {data.get('location', 'NOT FOUND')}: "
                f"{data.get('page_range', 'NOT FOUND')}.")

    def generate_journal_citation(data):
        return (f"{data.get('author', 'NOT FOUND')} ({data.get('year', 'NOT_FOUND')}) "
                f"‘{data.get('title', 'NOT FOUND')}’, {data.get('container', 'NOT FOUND')}, "
                f"{data.get('volume', 'NOT FOUND')}({data.get('issue', 'NOT FOUND')}), "
                f"pp. {data.get('page_range', 'NOT FOUND')}. DOI: {data.get('url', 'NOT FOUND')}.")

    def generate_webpage_citation(data):
        accessed_date = datetime.now().strftime("%d %B %Y")
        return (f"{data.get('author', 'NOT FOUND')} ({data.get('year', 'NOT FOUND')}) "
                f"{data.get('title', 'NOT FOUND')}. Available at: {data.get('url', 'NOT FOUND')} "
                f"(Accessed: {accessed_date}).")

    def generate_blog_citation(data):
        return (f"{data.get('author', 'NOT FOUND')} ({data.get('year', 'NOT FOUND')}) "
                f"‘{data.get('title', 'NOT FOUND')}’, {data.get('container', 'NOT FOUND')}, "
                f"{data.get('accessed_date', 'NOT FOUND')}. Available at: {data.get('url', 'NOT FOUND')}.")

    def generate_social_media_citation(data):
        return (f"{data.get('author', 'NOT FOUND')} [{data.get('publisher', 'NOT FOUND')}] "
                f"({data.get('year', 'NOT FOUND')}) {data.get('title', 'NOT FOUND')} "
                f"[{data.get('container', 'NOT FOUND')}] {data.get('accessed_date', 'NOT FOUND')}. "
                f"Available at: {data.get('url', 'NOT FOUND')}.")

    if test_config is not None:
        # Load the test config if passed in
        app.config.update(test_config)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)
