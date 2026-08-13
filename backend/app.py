"""
EvalvoCloud Backend API - Version 1 (Static)
Flask application serving API endpoints for the EvalvoCloud frontend.
This version works without a database.
"""

import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# CORS configuration - allow frontend to connect
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
CORS(app, origins=allowed_origins)

# App configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# ========================================
# API Routes
# ========================================

@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API information."""
    return jsonify({
        'app': 'EvalvoCloud Backend API',
        'version': '1.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'info': '/api/info',
            'contact': '/api/contact (POST)',
            'labs': '/api/labs',
            'stats': '/api/stats'
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'EvalvoCloud-backend',
        'database': 'not configured (Version 1)'
    })


@app.route('/api/info', methods=['GET'])
def app_info():
    """Application information endpoint."""
    return jsonify({
        'app_name': 'EvalvoCloud',
        'description': 'Experiential Learning Platform',
        'version': '1.0',
        'environment': os.getenv('FLASK_ENV', 'production'),
        'features': [
            'Hands-on Cloud Labs',
            'Linux Platform',
            'Windows Platform',
            'Custom Labs',
            'Self-Service Portal'
        ],
        'contact': {
            'email': 'query@evalvocloud.com',
            'phone': '75748 77958',
            'location': 'Vadodara, Gujarat, India'
        }
    })


@app.route('/api/labs', methods=['GET'])
def get_labs():
    """Get list of available labs (static data for Version 1)."""
    labs = [
        {
            'id': 1,
            'title': 'EC2 Instance Management',
            'category': 'aws',
            'duration': '45 mins',
            'level': 'Beginner',
            'description': 'Launch, configure and manage EC2 instances in AWS cloud.'
        },
        {
            'id': 2,
            'title': 'S3 Static Website Hosting',
            'category': 'aws',
            'duration': '30 mins',
            'level': 'Beginner',
            'description': 'Host a static website using Amazon S3 and CloudFront.'
        },
        {
            'id': 3,
            'title': 'Linux Administration',
            'category': 'linux',
            'duration': '60 mins',
            'level': 'Intermediate',
            'description': 'Learn essential Linux system administration commands and tools.'
        },
        {
            'id': 4,
            'title': 'Container Orchestration',
            'category': 'docker',
            'duration': '90 mins',
            'level': 'Advanced',
            'description': 'Build, run and manage Docker containers and compose applications.'
        },
        {
            'id': 5,
            'title': 'VPC Networking',
            'category': 'aws',
            'duration': '75 mins',
            'level': 'Intermediate',
            'description': 'Design and configure Virtual Private Cloud networking in AWS.'
        },
        {
            'id': 6,
            'title': 'Kubernetes Basics',
            'category': 'docker',
            'duration': '120 mins',
            'level': 'Advanced',
            'description': 'Deploy and manage containerized applications with Kubernetes.'
        }
    ]

    # Optional filtering by category
    category = request.args.get('category')
    if category and category != 'all':
        labs = [lab for lab in labs if lab['category'] == category]

    return jsonify({
        'labs': labs,
        'total': len(labs)
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get platform statistics (static for Version 1)."""
    return jsonify({
        'students_enrolled': 1098,
        'labs_available': 50,
        'platforms': 4,
        'uptime_percentage': 99.9,
        'last_updated': datetime.utcnow().isoformat()
    })


@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submissions (logs only in Version 1)."""
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if not data or not data.get(field):
            return jsonify({'error': f'Field "{field}" is required'}), 400

    # Validate email format (basic)
    email = data.get('email', '')
    if '@' not in email or '.' not in email:
        return jsonify({'error': 'Invalid email address'}), 400

    # In Version 1, just log and acknowledge
    # In Version 2, this will be stored in the database
    print(f"[CONTACT] From: {data['name']} ({data['email']}) - Subject: {data['subject']}")

    return jsonify({
        'message': 'Thank you for contacting EvalvoCloud! We will get back to you soon.',
        'status': 'received',
        'note': 'Version 1: Message logged (not stored in database)'
    }), 201


# ========================================
# Error Handlers
# ========================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405


# ========================================
# Main Entry Point
# ========================================

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'

    print(f"""
    ╔══════════════════════════════════════╗
    ║   EvalvoCloud Backend API v1.0        ║
    ║   Running on http://{host}:{port}     ║
    ║   Database: Not configured (v1)     ║
    ╚══════════════════════════════════════╝
    """)

    app.run(host=host, port=port, debug=debug)
