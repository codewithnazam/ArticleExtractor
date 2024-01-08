import streamlit as st
import re
import requests
import json
from bs4 import BeautifulSoup, Comment
from datetime import datetime

# Existing functions from your script
def sanitize_filename(url):
     # Split the URL at '.com'
    parts = url.split('.com', 1)
    if len(parts) == 2:
        base, rest = parts
        # Only sanitize the part after '.com'
        sanitized_rest = re.sub(r'[<>:"/\\|?*]', '_', rest)
        # Recombine the parts
        sanitized_url = base + '.com' + sanitized_rest
    else:
        # If '.com' is not in the URL, sanitize the entire URL
        sanitized_url = re.sub(r'[<>:"/\\|?*]', '_', url)
  
    return sanitized_url


def clear_attributes(tag):
    try:
        if hasattr(tag, 'attrs'):
            tag.attrs = {}
        for child in tag:
            if hasattr(child, 'children'):
                clear_attributes(child)
    except Exception as e:
        print(f"Error in clear_attributes: {e}")

def parse_exclusion_list(exclusion_list_str):
    exclusion_list = []
    if exclusion_list_str:
        items = exclusion_list_str.split(';')
        for item in items:
            parts = item.split('=')
            if len(parts) == 2:
                tag, value = parts[0].strip(), parts[1].strip()
                if tag and value:
                    if value.startswith('class:'):
                        exclusion_list.append((tag, {'class': value.replace('class:', '').strip()}))
                    elif value.startswith('id:'):
                        exclusion_list.append((tag, {'id': value.replace('id:', '').strip()}))
    return exclusion_list

def extract_article_content(url, start_tag, exclude_tags, include_comments, output_format, remove_attributes):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        
            # Use entire page if start tag not provided
            if start_tag:
                start_point = soup.find(*start_tag)
                if not start_point:
                    return "Starting point of the article not found."
                article = start_point
            else:
                article = soup

            if not include_comments:
                for element in article.find_all(text=lambda text: isinstance(text, Comment)):
                    element.extract()

            for tag, attributes in exclude_tags:
                for section in article.find_all(tag, attributes):
                    section.decompose()

            if remove_attributes:
                clear_attributes(article)

            if output_format == 'json':
                return json.dumps(article.text)
            else:  # default to 'html'
                return article.prettify()
        except Exception as e:
            return f"Error in extract_article_content: {e}"

# Streamlit UI function
def streamlit_ui():
    st.title("Article Content Extractor")

    # Input fields
    article_url = st.text_input("Enter the article URL: ", placeholder="e.g., https://example.com/article-name")

    start_tag_input = st.text_input("Enter the tag and class/id to start extraction (e.g., `div,class=article`): ", placeholder="e.g., div,class=article")
    start_tag = None
    if start_tag_input:
        start_tag_parts = start_tag_input.split(',')
        if len(start_tag_parts) == 2:
            start_tag = (start_tag_parts[0].strip(), {start_tag_parts[1].split('=')[0].strip(): start_tag_parts[1].split('=')[1].strip()})
        else:
            start_tag = (start_tag_parts[0].strip(), {})

    exclude_tags_input = st.text_area("Enter tags to exclude (use format: `tag=class:class_name` or `tag=id:id_name`; separate multiple tags with semicolons)", 
                                  placeholder="e.g., div=class:footer; div=id:comments")
    exclude_tags = parse_exclusion_list(exclude_tags_input)

    include_comments = st.checkbox("Include comments?", False)
    output_format = st.radio("Output format", ['html', 'json'])
    remove_attributes = st.checkbox("Remove HTML attributes?", False)

    # Button to trigger processing
    if st.button("Extract Content"):
        try:
            article_content = extract_article_content(article_url, start_tag, exclude_tags, include_comments, output_format, remove_attributes)
            
            if article_content.startswith("Error"):
                st.error(article_content)
            else:
                st.text_area("Extracted Content:", article_content, height=300)
                # Download button for the content
                file_extension = "json" if output_format == 'json' else "html"
                
            # Use sanitize_filename function here
            sanitized_url = sanitize_filename(article_url)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_extension = "json" if output_format == 'json' else "html"
            file_name = f"{sanitized_url}_{timestamp}.{file_extension}"

            st.download_button(label="Download Content",
                               data=article_content,
                               file_name=file_name,
                               mime=f"text/{file_extension}")
        except Exception as e:
            st.error(f"Error: {e}")

# Run the Streamlit UI
if __name__ == "__main__":
    streamlit_ui()
