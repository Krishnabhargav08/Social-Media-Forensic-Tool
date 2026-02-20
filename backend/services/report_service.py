"""
Report Generation Service
Creates encrypted PDF forensic reports
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
import hashlib
import os
from flask import current_app

class ReportService:
    """Service for generating forensic PDF reports"""
    
    def __init__(self):
        self.report_folder = None
    
    def generate_pdf_report(self, case_data, encryption_password):
        """Generate an encrypted PDF forensic report"""
        
        # Set report folder from config
        if not self.report_folder:
            self.report_folder = current_app.config.get('REPORT_FOLDER', 'reports')
        
        os.makedirs(self.report_folder, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"forensic_report_{case_data['_id']}_{timestamp}.pdf"
        temp_filepath = os.path.join(self.report_folder, f"temp_{filename}")
        final_filepath = os.path.join(self.report_folder, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(temp_filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#00d4ff'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#00ff88'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("FORENSIC INVESTIGATION REPORT", title_style))
        story.append(Paragraph("CONFIDENTIAL - OFFICIAL USE ONLY", styles['Normal']))
        story.append(Spacer(1, 0.5*inch))
        
        # Case Information
        story.append(Paragraph("CASE INFORMATION", heading_style))
        case_info = [
            ['Case ID:', case_data['_id']],
            ['Target Username:', case_data['target_username']],
            ['Platform:', case_data['platform']],
            ['Status:', case_data['status'].upper()],
            ['Created Date:', case_data['created_at']],
            ['Report Generated:', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')]
        ]
        case_table = Table(case_info, colWidths=[2*inch, 4*inch])
        case_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1a1a1a')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#00d4ff'))
        ]))
        story.append(case_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Risk Assessment
        analysis = case_data.get('analysis_results', {})
        story.append(Paragraph("RISK ASSESSMENT", heading_style))
        risk_info = [
            ['Risk Level:', case_data.get('risk_level', 'UNKNOWN').upper()],
            ['Risk Score:', f"{case_data.get('risk_score', 0)}/100"]
        ]
        risk_table = Table(risk_info, colWidths=[2*inch, 4*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1a1a1a')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.red if case_data.get('risk_score', 0) > 50 else colors.green)
        ]))
        story.append(risk_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Sentiment Analysis
        if analysis.get('sentiment'):
            story.append(Paragraph("SENTIMENT ANALYSIS", heading_style))
            sentiment = analysis['sentiment']
            sentiment_text = f"""
            Overall Sentiment: {sentiment.get('overall', 'N/A').upper()}<br/>
            Positive: {sentiment.get('positive_percentage', 0)}%<br/>
            Negative: {sentiment.get('negative_percentage', 0)}%<br/>
            Neutral: {sentiment.get('neutral_percentage', 0)}%
            """
            story.append(Paragraph(sentiment_text, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Cyberbullying Detection
        if analysis.get('cyberbullying'):
            story.append(Paragraph("CYBERBULLYING DETECTION", heading_style))
            cyberbullying = analysis['cyberbullying']
            cb_text = f"""
            Detected: {'YES' if cyberbullying.get('detected') else 'NO'}<br/>
            Confidence: {cyberbullying.get('confidence', 0)}%<br/>
            Incidents: {cyberbullying.get('incidents_count', 0)}<br/>
            Total Flags: {cyberbullying.get('total_flags', 0)}
            """
            story.append(Paragraph(cb_text, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Fraud Detection
        if analysis.get('fraud_detection'):
            story.append(Paragraph("FRAUD/SCAM DETECTION", heading_style))
            fraud = analysis['fraud_detection']
            fraud_text = f"""
            Detected: {'YES' if fraud.get('detected') else 'NO'}<br/>
            Confidence: {fraud.get('confidence', 0)}%<br/>
            Suspicious Posts: {fraud.get('suspicious_count', 0)}<br/>
            Total Flags: {fraud.get('total_flags', 0)}
            """
            story.append(Paragraph(fraud_text, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Fake Profile Analysis
        if analysis.get('fake_profile'):
            story.append(Paragraph("FAKE PROFILE ANALYSIS", heading_style))
            fake = analysis['fake_profile']
            fake_text = f"""
            Potentially Fake: {'YES' if fake.get('is_potentially_fake') else 'NO'}<br/>
            Fake Score: {fake.get('fake_score', 0)}/100<br/>
            Account Age: {fake.get('account_age_days', 0)} days<br/>
            Risk Factors: {len(fake.get('risk_factors', []))}
            """
            story.append(Paragraph(fake_text, styles['Normal']))
            
            if fake.get('risk_factors'):
                story.append(Paragraph("<br/>Identified Risk Factors:", styles['Normal']))
                for factor in fake['risk_factors']:
                    story.append(Paragraph(f"• {factor}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Evidence Integrity
        story.append(Paragraph("EVIDENCE INTEGRITY", heading_style))
        evidence_hash = case_data.get('evidence_hash', 'NOT_AVAILABLE')
        story.append(Paragraph(f"SHA-256 Hash:", styles['Normal']))
        story.append(Paragraph(f"<font name='Courier' size='8'>{evidence_hash}</font>", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Footer
        story.append(PageBreak())
        story.append(Paragraph("LEGAL NOTICE", heading_style))
        legal_text = """
        This report contains confidential information collected as part of an official forensic investigation.
        Unauthorized access, distribution, or use of this document is strictly prohibited and may result in legal action.
        All data was collected in compliance with applicable laws and regulations.
        Evidence integrity is verified using SHA-256 cryptographic hash.
        """
        story.append(Paragraph(legal_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        # Encrypt PDF
        self._encrypt_pdf(temp_filepath, final_filepath, encryption_password)
        
        # Remove temporary file
        os.remove(temp_filepath)
        
        # Generate file hash
        file_hash = self._generate_file_hash(final_filepath)
        
        # Generate encryption password hash (for verification)
        encryption_hash = hashlib.sha256(encryption_password.encode()).hexdigest()
        
        return {
            'file_path': final_filepath,
            'file_hash': file_hash,
            'encryption_hash': encryption_hash
        }
    
    def _encrypt_pdf(self, input_path, output_path, password):
        """Encrypt PDF with password"""
        try:
            pdf_reader = PdfReader(input_path)
            pdf_writer = PdfWriter()
            
            # Copy all pages
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
            
            # Encrypt with password
            pdf_writer.encrypt(user_password=password, owner_password=password, algorithm="AES-256")
            
            # Write encrypted PDF
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
                
        except Exception as e:
            raise Exception(f"PDF encryption failed: {str(e)}")
    
    def _generate_file_hash(self, filepath):
        """Generate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        
        with open(filepath, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
