

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'PNG', 'JPG', 'JPEG'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
