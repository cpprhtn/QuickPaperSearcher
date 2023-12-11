import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_arxiv_pdf(arxiv_id, download_dir='pdf_downloads'):
    # Ensure the download directory exists
    os.makedirs(download_dir, exist_ok=True)

    # Construct the arXiv URL
    arxiv_url = f'https://arxiv.org/abs/{arxiv_id}'

    # Send an HTTP request to get the HTML content of the arXiv page
    response = requests.get(arxiv_url)
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the link to the PDF file on the arXiv page
        pdf_link = soup.find('meta', {'name': 'citation_pdf_url'})
        if pdf_link and pdf_link.get('content'):
            # Construct the absolute URL of the PDF file
            pdf_url = pdf_link.get('content')

            # Send an HTTP request to download the PDF file
            pdf_response = requests.get(pdf_url)
            if pdf_response.status_code == 200:
                # Save the PDF file to the download directory
                pdf_filename = f'{arxiv_id}.pdf'
                pdf_filepath = os.path.join(download_dir, pdf_filename)
                with open(pdf_filepath, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                
                print(f'Downloaded PDF: {pdf_filepath}')
            else:
                print(f'Failed to download PDF. Status code: {pdf_response.status_code}')
        else:
            print('PDF link not found in the meta tags on the arXiv page.')
    else:
        print(f'Failed to fetch arXiv page. Status code: {response.status_code}')

# Example usage: Download the PDF for the arXiv ID '2101.00123'
download_arxiv_pdf('2101.00123')
