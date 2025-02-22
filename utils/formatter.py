import re
from collections import defaultdict

def extract_and_format_references(text):
    # Regex to find references, including multiple file-page pairs in one mention
    ref_pattern = re.compile(r'\("file"\s*:\s*"(.*?)"(?:,\s*"page"\s*:\s*(\d+(?:-\d+)?))?\)')
    
    ref_dict = {}
    ref_count = 1
    formatted_text = text
    
    # Dictionary to track references
    references_map = defaultdict(set)
    
    # Find all matches and process them
    for match in ref_pattern.finditer(text):
        file_name, page_number = match.groups()
        ref_key = (file_name, page_number if page_number else "N/A")
        
        if ref_key not in ref_dict:
            ref_dict[ref_key] = ref_count
            ref_count += 1
        
        citation_number = ref_dict[ref_key]
        references_map[match.group(0)].add(citation_number)
    
    # Replace references with multiple citations if needed
    for ref, numbers in references_map.items():
        citation_str = "".join(f'[{num}]' for num in sorted(numbers))
        formatted_text = formatted_text.replace(ref, f' {citation_str}', 1)

        
    ref_pattern = re.compile(r'\(page_label.*?\)')
    formatted_text = re.sub(ref_pattern, '', formatted_text)

    # Formatting the references section
    references = "\n### References\n" + "\n".join(
        f'- **[{num}]** Filename: {key[0]}, Page: {key[1]}' 
        for key, num in sorted(ref_dict.items(), key=lambda x: x[1])
    )
    
    return formatted_text.strip() + "\n\n" + references

def remove_page_references(text):
    # Regex to remove occurrences of (page_label.......... until the closing parenthesis)
    ref_pattern = re.compile(r'\(page_label.*?\)')
    return re.sub(ref_pattern, '', text)

def format_as_markdown(text):
    """
    Convert formatted reference text into a well-structured Markdown format.
    """
    lines = text.strip().split("\n")
    formatted_lines = []
    references = []
    in_references = False
    
    for line in lines:
        if re.match(r'^- \*\*\[\d+\]\*\*', line):
            in_references = True
        
        if in_references:
            references.append(line)
        else:
            formatted_lines.append(line)
    
    markdown_output = "\n".join(formatted_lines) + "\n\n" + "\n".join(references)
    
    return markdown_output

# Example passage
test_passage = '''Based on the information from these sources, Elara is described as a young and curious scholar in ("file" : "story.pdf", "page" : 1) and ("file" : "story_new.pdf", "page" : 1) who is fascinated by the legends of the Lost City of Arandor. She is determined to uncover the truth and embarks on a quest to find the city, facing various challenges and obstacles along the way ("file" : "story.pdf", "page" : 2). In a different context, Elara is portrayed as a detective in ("file" : "story_new.pdf", "page" : 1) who is skilled in code and cryptography, and is tasked with solving a high-profile cyber crime case involving a notorious hacker collective called "Arandor". She uses her skills to infiltrate the collective's system and bring their reign to an end ("file" : "story_new.pdf", "page" : 2). Overall, Elara is depicted as a determined, curious, and skilled individual who is driven to uncover the truth and solve complex problems, whether in the context of ancient legends or modern-day cyber crimes.'''

# formatted_output = extract_and_format_references(test_passage)
# print(format_as_markdown(formatted_output))

# cleaned_text = remove_page_references(test_passage)
# print(cleaned_text)