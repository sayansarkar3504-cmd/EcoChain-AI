import re

def mask_sensitive_data(text: str) -> str:
    """
    Masks PII such as Bank Accounts, SSNs, and Emails from text.
    """
    # Mask Bank Accounts (Assuming 9-12 digits)
    bank_account_pattern = r'\b\d{5,8}(\d{4})\b'
    text = re.sub(bank_account_pattern, lambda m: 'X' * (len(m.group(0)) - 4) + m.group(1), text)
    
    # Mask Emails
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    text = re.sub(email_pattern, '[EMAIL MASKED]', text)
    
    # Mask SSN (XXX-XX-XXXX)
    ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
    text = re.sub(ssn_pattern, 'XXX-XX-XXXX', text)
    
    # Mask Credit Cards (16 digits)
    cc_pattern = r'\b(?:\d[ -]*?){13,16}\b'
    # Simple regex to replace 16 digit cards leaving last 4
    text = re.sub(r'\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?(\d{4})\b', r'XXXX-XXXX-XXXX-\1', text)
    
    return text

if __name__ == "__main__":
    # Test cases
    sample = "My bank account is 1234567890 and email is test@example.com."
    print("Original:", sample)
    print("Masked:", mask_sensitive_data(sample))
