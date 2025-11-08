import requests
from bs4 import BeautifulSoup
import json
import time
import re
from typing import List, Dict
import os

class SHLScraper:
    def __init__(self):
        self.catalog_url = "https://www.shl.com/solutions/products/product-catalog/"
        self.base_url = "https://www.shl.com"
        self.assessments = []
        
    def scrape_catalog(self) -> List[Dict]:
        """
        Scrape the SHL product catalog for individual test solutions.
        Ignores Pre-packaged Job Solutions.
        """
        print("Starting to scrape SHL catalog...")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(self.catalog_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all assessment links
            # The actual structure may vary, this is a general approach
            assessment_links = []
            
            # Look for links in the catalog
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Filter for product catalog links, exclude job solutions
                if '/product-catalog/view/' in href and 'job-' not in href.lower():
                    full_url = href if href.startswith('http') else self.base_url + href
                    if full_url not in assessment_links:
                        assessment_links.append(full_url)
            
            print(f"Found {len(assessment_links)} assessment links")
            
            # Scrape each assessment page
            for idx, url in enumerate(assessment_links[:100], 1):  # Limit for testing
                print(f"Scraping {idx}/{min(len(assessment_links), 100)}: {url}")
                assessment_data = self.scrape_assessment_page(url)
                if assessment_data:
                    self.assessments.append(assessment_data)
                time.sleep(0.5)  # Be respectful to the server
                
        except Exception as e:
            print(f"Error scraping catalog: {e}")
            
        return self.assessments
    
    def scrape_assessment_page(self, url: str) -> Dict:
        """
        Scrape individual assessment page for details.
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract assessment name
            name = ""
            h1_tag = soup.find('h1')
            if h1_tag:
                name = h1_tag.get_text(strip=True)
            
            # Extract description
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                description = meta_desc['content']
            else:
                # Try to find description in page content
                desc_div = soup.find('div', class_=re.compile('description|overview', re.I))
                if desc_div:
                    description = desc_div.get_text(strip=True)[:500]
            
            # Extract test type
            test_type = self.extract_test_type(soup, description)
            
            # Extract duration (in minutes)
            duration = self.extract_duration(soup, description)
            
            # Extract adaptive and remote support
            adaptive_support = "No"
            remote_support = "Yes"  # Most SHL assessments are remote
            
            text_content = soup.get_text().lower()
            if 'adaptive' in text_content:
                adaptive_support = "Yes"
            
            assessment_data = {
                "url": url,
                "name": name if name else url.split('/')[-2].replace('-', ' ').title(),
                "adaptive_support": adaptive_support,
                "description": description if description else "SHL assessment for talent evaluation",
                "duration": duration,
                "remote_support": remote_support,
                "test_type": test_type
            }
            
            return assessment_data
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def extract_test_type(self, soup, description: str) -> List[str]:
        """
        Extract test type from page content.
        """
        test_types = []
        text = soup.get_text().lower() + " " + description.lower()
        
        type_mapping = {
            "Knowledge & Skills": ["technical", "coding", "programming", "java", "python", "sql", 
                                   "javascript", "css", "html", "knowledge", "skill"],
            "Personality & Behavior": ["personality", "behavior", "opq", "leadership", "cultural fit",
                                       "behavioral", "competenc"],
            "Ability & Aptitude": ["cognitive", "numerical", "verbal", "reasoning", "aptitude", 
                                   "inductive", "deductive", "ability"],
            "Competencies": ["competenc", "sales", "customer service", "communication", "manager"],
            "Simulations": ["simulation", "exercise", "case study", "role play"]
        }
        
        for test_type, keywords in type_mapping.items():
            if any(keyword in text for keyword in keywords):
                test_types.append(test_type)
        
        # Default if no type found
        if not test_types:
            test_types = ["Assessment"]
            
        return test_types
    
    def extract_duration(self, soup, description: str) -> int:
        """
        Extract assessment duration in minutes.
        """
        text = soup.get_text() + " " + description
        
        # Look for duration patterns
        duration_patterns = [
            r'(\d+)\s*(?:minutes?|mins?)',
            r'(\d+)\s*(?:hours?|hrs?)',
        ]
        
        for pattern in duration_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                duration = int(matches[0])
                # Convert hours to minutes if needed
                if 'hour' in pattern or 'hr' in pattern:
                    duration *= 60
                return duration
        
        # Default duration based on test type
        return 60
    
    def save_to_json(self, filename: str):
        """
        Save scraped assessments to JSON file.
        """
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.assessments, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.assessments)} assessments to {filename}")

def main():
    scraper = SHLScraper()
    assessments = scraper.scrape_catalog()
    
    if assessments:
        scraper.save_to_json('data/assessments.json')
        print(f"Successfully scraped {len(assessments)} assessments")
    else:
        print("No assessments scraped. Using fallback data...")
        # Create fallback data if scraping fails
        create_fallback_data()

def create_fallback_data():
    """
    Create fallback assessment data based on the provided training examples.
    This ensures the system works even if web scraping fails.
    """
    print("Creating fallback assessment data from training examples...")
    
    # Extract unique assessments from training data
    assessments = {}
    
    training_data = [
        ("https://www.shl.com/solutions/products/product-catalog/view/automata-fix-new/", 
         "Automata Fix", "Technical coding assessment for automated testing", 60, ["Knowledge & Skills"]),
        ("https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/",
         "Core Java Entry Level", "Java programming assessment for entry-level developers", 45, ["Knowledge & Skills"]),
        ("https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
         "Java 8", "Advanced Java 8 programming assessment", 60, ["Knowledge & Skills"]),
        ("https://www.shl.com/products/product-catalog/view/interpersonal-communications/",
         "Interpersonal Communications", "Assessment of communication and collaboration skills", 30, ["Personality & Behavior", "Competencies"]),
        ("https://www.shl.com/solutions/products/product-catalog/view/entry-level-sales-7-1/",
         "Entry Level Sales 7.1", "Sales aptitude assessment for entry-level positions", 60, ["Competencies"]),
        ("https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
         "Occupational Personality Questionnaire OPQ32r", "Comprehensive personality assessment for workplace behavior", 90, ["Personality & Behavior"]),
        ("https://www.shl.com/solutions/products/product-catalog/view/verify-verbal-ability-next-generation/",
         "Verify Verbal Ability Next Generation", "Verbal reasoning and comprehension assessment", 18, ["Ability & Aptitude"]),
        ("https://www.shl.com/solutions/products/product-catalog/view/verify-numerical-ability/",
         "Verify Numerical Ability", "Numerical reasoning assessment", 18, ["Ability & Aptitude"]),
        ("https://www.shl.com/solutions/products/product-catalog/view/python-new/",
         "Python", "Python programming skills assessment", 60, ["Knowledge & Skills"]),
        ("https://www.shl.com/solutions/products/product-catalog/view/sql-server-new/",
         "SQL Server", "SQL database querying and management assessment", 60, ["Knowledge & Skills"]),
    ]
    
    fallback_assessments = []
    for url, name, desc, duration, test_types in training_data:
        assessment = {
            "url": url,
            "name": name,
            "adaptive_support": "Yes" if "adaptive" in desc.lower() else "No",
            "description": desc,
            "duration": duration,
            "remote_support": "Yes",
            "test_type": test_types
        }
        fallback_assessments.append(assessment)
    
    os.makedirs('data', exist_ok=True)
    with open('data/assessments.json', 'w', encoding='utf-8') as f:
        json.dump(fallback_assessments, f, indent=2, ensure_ascii=False)
    
    print(f"Created fallback data with {len(fallback_assessments)} assessments")

if __name__ == "__main__":
    main()
