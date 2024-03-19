# Import the app object from the source module
from source import app

# Check if this script is the main entry point of the program
if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)