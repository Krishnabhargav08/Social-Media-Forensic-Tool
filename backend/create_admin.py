"""
Admin User Setup Script
Run this to create the first admin account
"""

from pymongo import MongoClient
import bcrypt
from datetime import datetime
import sys

def create_admin():
    """Create admin user in MongoDB"""
    
    print("\n" + "="*60)
    print("  SOCIAL MEDIA FORENSIC TOOL - Admin Setup")
    print("="*60 + "\n")
    
    # Get admin details
    print("Enter admin account details:\n")
    
    email = input("Email [admin@forensictool.com]: ").strip() or "admin@forensictool.com"
    password = input("Password [Admin@123]: ").strip() or "Admin@123"
    full_name = input("Full Name [System Administrator]: ").strip() or "System Administrator"
    badge_number = input("Badge Number [ADMIN-001]: ").strip() or "ADMIN-001"
    department = input("Department [System Administration]: ").strip() or "System Administration"
    
    print("\n" + "-"*60)
    print("Creating admin account...")
    print("-"*60 + "\n")
    
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['forensic_tool']
        
        # Check if admin already exists
        existing = db.users.find_one({'email': email})
        if existing:
            print(f"⚠️  User with email {email} already exists!")
            overwrite = input("Do you want to delete and recreate? (yes/no): ").lower()
            if overwrite == 'yes':
                db.users.delete_one({'email': email})
                print("✓ Existing user deleted")
            else:
                print("Cancelled. Exiting...")
                return
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        
        # Create admin document
        admin_data = {
            'email': email.lower(),
            'password': hashed_password,
            'full_name': full_name,
            'badge_number': badge_number,
            'department': department,
            'role': 'admin',
            'status': 'approved',
            'login_attempts': 0,
            'account_locked': False,
            'locked_until': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'last_login': None
        }
        
        # Insert into database
        result = db.users.insert_one(admin_data)
        
        print("\n" + "="*60)
        print("  ✅ ADMIN ACCOUNT CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"\n  Email:    {email}")
        print(f"  Password: {password}")
        print(f"  Role:     ADMIN")
        print(f"  Status:   APPROVED")
        print("\n" + "="*60)
        print("\n⚠️  IMPORTANT: Save these credentials securely!")
        print("⚠️  Change the password after first login!\n")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure:")
        print("1. MongoDB is running on localhost:27017")
        print("2. You have installed required packages: pip install pymongo bcrypt")
        sys.exit(1)

if __name__ == "__main__":
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
