# Web Article Extractor

## Overview

The Web Article Extractor is an easy-to-use web application designed to extract content from web articles. It allows users to specify URLs, define extraction parameters, and choose output formats for efficient content extraction.

## Live Application

Access the live application here: [Web Article Extractor](https://webarticleextractor.streamlit.app/)

## Features

- **URL Input**: Extract content from any accessible web article.
- **Custom Extraction Settings**: Define start points, exclude specific tags, and more.
- **Output Formatting**: Choose between HTML and JSON output formats.
- **Attribute Removal**: Option to strip HTML attributes for cleaner content.

## How to Use the Application

### Step 1: Enter Article URL

- Input the full URL of the article you want to extract content from.
- Example: `https://example.com/article`

### Step 2: Configure Extraction Settings

#### Start Tag

- Optionally specify the HTML tag where extraction should start.
- Format: `tag,class=class_name` or `tag,id=id_name`
- Example: `div,class=article-content`

#### Exclude Tags

- Define tags to be excluded from the extraction.
- Format: `tag=class:class_name` or `tag=id:id_name`; separate multiple tags with semicolons.
- Example: `div=class:footer; div=id:comments`

#### Include Comments

- Choose whether to include HTML comments in the output.

### Step 3: Select Output Format

- Choose `HTML` for a web page format or `JSON` for a JSON-encoded text.

### Step 4: Remove HTML Attributes (Optional)

- Select this option if you want to remove all HTML attributes from the extracted content.

### Step 5: Extract Content

- Click the "Extract Content" button to process the input URL with the specified settings.

### Step 6: View and Download Extracted Content

- The extracted content will be displayed on the screen.
- Use the "Download Content" button to save the extracted content to your device.

## Troubleshooting and Support

If you encounter issues or have questions, please refer to the following:

- **Check URL Format**: Ensure the URL is correct and the webpage is accessible.
- **Review Tag Formatting**: Incorrect tag formats might lead to unexpected results.
- **Output Clarifications**: If the output is not as expected, adjust your extraction settings.

For further assistance, contact support at [codewithnazam@gmail.com].
