import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from src.api import app
    port = int(os.environ.get('PORT', 8011))
    app.run(debug=True, host='0.0.0.0', port=port)
