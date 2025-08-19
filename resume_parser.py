import PyPDF2
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts raw text from a PDF file.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"  # Add text from each page
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return None
    return text

def parse_resume(text):
    """
    Analyzes the extracted text to find key information using regex patterns.
    Returns a dictionary of the parsed details.
    """
    details = {
        'email': None,
        'phone': None,
        'name': None,  # This is tricky and often requires more advanced NLP
        'skills': [],
        'education': [] # We'll look for common education keywords
    }

    # 1. Extract Email (a very common pattern)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        details['email'] = email_match.group()

    # 2. Extract Phone Number (catches various common formats)
    phone_pattern = r'(\+\d{1,3}[-\.\s]?)?(\(?\d{1,4}\)?[-\.\s]?)?\d{1,4}[-\.\s]?\d{1,4}[-\.\s]?\d{1,9}'
    phone_match = re.search(phone_pattern, text)
    if phone_match:
        details['phone'] = phone_match.group().strip()

    # 3. Extract Skills (Look for a common skills section)
    # Common tech skills keywords
    skill_keywords = ['python', 'java', 'c++', 'javascript', 'linux', 'kali', 'networking', 'bash', 'git', 'cybersecurity', 'encryption', 'penetration testing', 'mysql', 'flask', 'django', 'automation', 'scripting']
    found_skills = []
    for skill in skill_keywords:
        # Search for the skill word, case-insensitive
        if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE):
            found_skills.append(skill)
    details['skills'] = found_skills

    # 4. Extract Education (Look for common university names or degree types)
    education_keywords = ['bachelor', 'b\.tech', 'bsc', 'master', 'm\.tech', 'msc', 'phd', 'diploma', 'university', 'college', 'institute of technology', 'high school']
    found_education = []
    for edu in education_keywords:
        if re.search(rf'\b{re.escape(edu)}\b', text, re.IGNORECASE):
            found_education.append(edu)
    details['education'] = found_education

    # 5. (Advanced & Optional) Extract Name - This is a simple heuristic.
    # Often the first line or a line in large font is the name.
    # This is not reliable but can be a starting point.
    lines = text.split('\n')
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and len(stripped_line) < 50: # Not a long paragraph
            # Check if it looks like a name (has letters and possibly a space)
            if re.match(r'^[A-Za-z\.\s]+$', stripped_line):
                details['name'] = stripped_line
                break # Assume the first likely candidate is the name

    return details

def main():
    """
    Main function to run the resume parser.
    """
    import sys
    import json # For pretty printing the output

    if len(sys.argv) != 2:
        print("Usage: python3 resume_parser.py <path_to_resume.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    print(f"[+] Attempting to parse: {pdf_path}")

    # Step 1: Get the text
    raw_text = extract_text_from_pdf(pdf_path)
    if raw_text is None:
        sys.exit(1) # Exit if PDF reading failed

    # Optional: Print raw text for debugging
    # print("--- RAW TEXT ---")
    # print(raw_text[:500]) # Print first 500 characters
    # print("---------------")

    # Step 2: Parse the text
    print("[+] Analyzing text...")
    resume_data = parse_resume(raw_text)

    # Step 3: Print the results nicely
    print("\n" + "="*50)
    print("RESUME ANALYSIS RESULTS")
    print("="*50)
    print(f"Name: {resume_data.get('name', 'Not Found')}")
    print(f"Email: {resume_data.get('email', 'Not Found')}")
    print(f"Phone: {resume_data.get('phone', 'Not Found')}")

    print("\nSkills Found:")
    if resume_data['skills']:
        for skill in resume_data['skills']:
            print(f"  - {skill.title()}")
    else:
        print("  - None detected")

    print("\nEducation Keywords Found:")
    if resume_data['education']:
        for edu in resume_data['education']:
            print(f"  - {edu.title()}")
    else:
        print("  - None detected")
    print("="*50)

    # Uncomment the line below to see the raw dictionary output
    # print(json.dumps(resume_data, indent=2))

if __name__ == "__main__":
    main()
