from flask import jsonify, send_file, current_app as app
from bson import ObjectId
import os


# handler for avatar streaming
def stream_avatar(id, collection):
    try:
        # Check if the patient exists
        item = app.db[collection].find_one({"_id": ObjectId(id)})
        if not item:
            return jsonify({"error": "Item not found"}), 404
        
        # Get the avatar file path
        avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], item["avatar"])

        # Get file extension from avatar filename
        extension = item["avatar"].split('.')[-1].lower()
        
        # Map common image extensions to MIME types
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg', 
            'png': 'image/png',
            'gif': 'image/gif',
        }
        
        # Get correct MIME type or default to jpeg
        mime_type = mime_types.get(extension, 'image/jpeg')

        # Stream the avatar file with correct MIME type
        return send_file(avatar_path, mimetype=mime_type)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500