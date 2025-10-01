#!/usr/bin/env python3
"""
Generate self-signed SSL certificates for Django development server
"""

import os
import subprocess
import sys
from pathlib import Path

def generate_ssl_certificates():
    """Generate self-signed SSL certificates for development use"""
    
    cert_file = "cert.pem"
    key_file = "key.pem"
    
    # Check if certificates already exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print(f"SSL certificates already exist: {cert_file}, {key_file}")
        return True
    
    # Try to use openssl command
    try:
        cmd = [
            "openssl", "req", "-new", "-x509", 
            "-keyout", key_file, 
            "-out", cert_file, 
            "-days", "365", 
            "-nodes", 
            "-subj", "/C=US/ST=Development/L=Development/O=Development/CN=localhost"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully generated SSL certificates: {cert_file}, {key_file}")
            return True
        else:
            print(f"OpenSSL command failed: {result.stderr}")
            
    except FileNotFoundError:
        print("OpenSSL not found in PATH. Trying alternative method...")
    
    # Alternative: Use Python cryptography library
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Generate certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Development"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Development"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Development"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write private key
        with open(key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Write certificate
        with open(cert_file, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        print(f"Successfully generated SSL certificates using Python: {cert_file}, {key_file}")
        return True
        
    except ImportError:
        print("cryptography library not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
            print("cryptography installed. Please run this script again.")
            return False
        except subprocess.CalledProcessError:
            print("Failed to install cryptography library")
            return False
    
    except Exception as e:
        print(f"Failed to generate certificates with Python: {e}")
        return False

if __name__ == "__main__":
    if generate_ssl_certificates():
        print("\n✅ SSL certificates generated successfully!")
        print("You can now run the HTTPS development server with:")
        print("python manage.py runserver_plus --cert-file cert.pem --key-file key.pem 127.0.0.1:8000")
    else:
        print("\n❌ Failed to generate SSL certificates")
        sys.exit(1)