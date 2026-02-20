"""
Hash Utilities
Provides hashing functions for evidence integrity and password verification
"""

import hashlib
import json

def generate_evidence_hash(data):
    """
    Generate SHA-256 hash for evidence integrity
    Takes data object and creates a deterministic hash
    """
    # Convert data to JSON string (sorted for consistency)
    json_string = json.dumps(data, sort_keys=True)
    
    # Generate SHA-256 hash
    sha256_hash = hashlib.sha256(json_string.encode('utf-8')).hexdigest()
    
    return sha256_hash

def verify_evidence_hash(data, stored_hash):
    """Verify evidence integrity by comparing hashes"""
    current_hash = generate_evidence_hash(data)
    return current_hash == stored_hash

def hash_password(password):
    """Generate SHA-256 hash of password (for report encryption verification)"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password_hash(password, stored_hash):
    """Verify password against stored hash"""
    current_hash = hash_password(password)
    return current_hash == stored_hash

def generate_file_hash(file_path):
    """Generate SHA-256 hash of a file"""
    sha256_hash = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None
