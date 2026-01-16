"""
Zero-Cost Jira Bug Processor
Runs entirely on GitHub Actions - No external servers needed!
"""

import os
import sys
import json
import base64
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
import time

# Configuration from GitHub Secrets
CONFIG = {
    'JIRA_EMAIL': os.environ.get('JIRA_EMAIL'),
    'JIRA_API_TOKEN': os.environ.get('JIRA_API_TOKEN'),
    'JIRA_BASE_URL': os.environ.get('JIRA_BASE_URL'),
    'GITHUB_TOKEN': os.environ.get('GITHUB_TOKEN'),
    'GITHUB_REPOSITORY': os.environ.get('GITHUB_REPOSITORY')
}


class JiraGitHubProcessor:
    """Main processor class"""
    
    def __init__(self, bug_key):
        self.bug_key = bug_key
        self.bug_data = None
        self.attachments = []
        self.github_issue_number = None
        self.github_issue_url = None
        
    def run(self):
        """Main execution flow"""
        print("=" * 70)
        print("🐍 Python Zero-Cost Jira Bug Processor")
        print("=" * 70)
        print(f"Processing bug: {self.bug_key}")
        print()
        
        try:
            # Step 1: Fetch bug details from Jira
            self.fetch_bug_from_jira()
            
            # Step 2: Download and store attachments
            self.process_attachments()
            
            # Step 3: Upload attachments to GitHub Release
            if self.attachments:
                self.upload_to_github_release()
            
            # Step 4: Create GitHub issue
            self.create_github_issue()
            
            # Step 5: Update Jira with GitHub link
            self.update_jira()
            
            print()
            print("=" * 70)
            print("✅ Processing Complete!")
            print("=" * 70)
            print(f"Jira Bug:      {self.bug_key}")
            print(f"GitHub Issue:  #{self.github_issue_number}")
            print(f"Attachments:   {len(self.attachments)}")
            print()
            
            return 0
            
        except Exception as e:
            print(f"❌ Error: {str(e)}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1
    
    def fetch_bug_from_jira(self):
        """Fetch complete bug details from Jira"""
        print("📥 Fetching bug details from Jira...")
        
        url = f"{CONFIG['JIRA_BASE_URL']}/rest/api/3/issue/{self.bug_key}"
        
        # Create Basic Auth header
        auth_string = f"{CONFIG['JIRA_EMAIL']}:{CONFIG['JIRA_API_TOKEN']}"
        auth_bytes = base64.b64encode(auth_string.encode('utf-8'))
        auth_header = f"Basic {auth_bytes.decode('utf-8')}"
        
        request = urllib.request.Request(url)
        request.add_header('Authorization', auth_header)
        request.add_header('Accept', 'application/json')
        
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                self.bug_data = json.loads(response.read().decode('utf-8'))
                print(f"✅ Fetched bug: {self.bug_data['key']}")
                print(f"   Summary: {self.bug_data['fields']['summary']}")
                
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP Error: {e.code} - {e.reason}")
            error_body = e.read().decode('utf-8')
            print(f"   Response: {error_body}")
            raise
    
    def process_attachments(self):
        """Download attachments and store locally"""
        attachments_data = self.bug_data['fields'].get('attachment', [])
        
        if not attachments_data:
            print("📎 No attachments found")
            return
        
        print(f"📎 Processing {len(attachments_data)} attachment(s)...")
        
        # Create directory for attachments
        attachments_dir = Path('attachments')
        attachments_dir.mkdir(exist_ok=True)
        
        for attachment in attachments_data:
            try:
                filename = attachment['filename']
                file_url = attachment['content']
                file_size = attachment['size']
                
                print(f"   Downloading: {filename} ({self._format_size(file_size)})")
                
                # Download file
                file_data = self._download_from_jira(file_url)
                
                # Save to disk
                file_path = attachments_dir / filename
                with open(file_path, 'wb') as f:
                    f.write(file_data)
                
                self.attachments.append({
                    'filename': filename,
                    'path': str(file_path),
                    'size': file_size,
                    'mime_type': attachment.get('mimeType', 'application/octet-stream'),
                    'github_url': None  # Will be set after upload
                })
                
                print(f"   ✅ Downloaded: {filename}")
                
            except Exception as e:
                print(f"   ⚠️  Failed to download {filename}: {str(e)}")
                continue
        
        print(f"✅ Downloaded {len(self.attachments)} attachment(s)")
    
    def _download_from_jira(self, url):
        """Download file from Jira"""
        auth_string = f"{CONFIG['JIRA_EMAIL']}:{CONFIG['JIRA_API_TOKEN']}"
        auth_bytes = base64.b64encode(auth_string.encode('utf-8'))
        auth_header = f"Basic {auth_bytes.decode('utf-8')}"
        
        request = urllib.request.Request(url)
        request.add_header('Authorization', auth_header)
        
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()
    
    def upload_to_github_release(self):
        """Upload attachments to GitHub Release"""
        print(f"📦 Creating GitHub Release for attachments...")
        
        owner, repo = CONFIG['GITHUB_REPOSITORY'].split('/')
        
        # Create release
        release_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
        release_tag = f"jira-{self.bug_key.lower()}-{int(time.time())}"
        
        release_data = {
            'tag_name': release_tag,
            'name': f"Attachments: {self.bug_key}",
            'body': f"Attachments for Jira bug [{self.bug_key}]({CONFIG['JIRA_BASE_URL']}/browse/{self.bug_key})",
            'draft': False,
            'prerelease': True
        }
        
        request = urllib.request.Request(
            release_url,
            data=json.dumps(release_data).encode('utf-8'),
            method='POST'
        )
        request.add_header('Authorization', f"Bearer {CONFIG['GITHUB_TOKEN']}")
        request.add_header('Accept', 'application/vnd.github+json')
        request.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                release = json.loads(response.read().decode('utf-8'))
                upload_url = release['upload_url'].replace('{?name,label}', '')
                
                print(f"✅ Release created: {release_tag}")
                
                # Upload each attachment
                for attachment in self.attachments:
                    self._upload_asset(upload_url, attachment)
                    
        except urllib.error.HTTPError as e:
            print(f"⚠️  Failed to create release: {e.code} - {e.reason}")
            print(f"   Attachments will be listed in issue without download links")
    
    def _upload_asset(self, upload_url, attachment):
        """Upload single file as release asset"""
        print(f"   Uploading: {attachment['filename']}")
        
        with open(attachment['path'], 'rb') as f:
            file_data = f.read()
        
        asset_url = f"{upload_url}?name={attachment['filename']}"
        
        request = urllib.request.Request(asset_url, data=file_data, method='POST')
        request.add_header('Authorization', f"Bearer {CONFIG['GITHUB_TOKEN']}")
        request.add_header('Content-Type', attachment['mime_type'])
        
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                asset = json.loads(response.read().decode('utf-8'))
                attachment['github_url'] = asset['browser_download_url']
                print(f"   ✅ Uploaded: {attachment['filename']}")
                print(f"      URL: {attachment['github_url']}")
        except urllib.error.HTTPError as e:
            print(f"   ⚠️  Failed to upload {attachment['filename']}: {e.code}")
    
    def create_github_issue(self):
        """Create GitHub issue with bug details and attachment links"""
        print("🔨 Creating GitHub issue...")
        
        fields = self.bug_data['fields']
        
        # Build attachment section
        attachment_section = ""
        if self.attachments:
            attachment_section = "\n## 📎 Attachments\n\n"
            for att in self.attachments:
                size_kb = att['size'] / 1024
                if att['github_url']:
                    attachment_section += f"- [{att['filename']}]({att['github_url']}) ({size_kb:.2f} KB)\n"
                else:
                    attachment_section += f"- {att['filename']} ({size_kb:.2f} KB) - *Download failed*\n"
        
        # Build labels
        labels = fields.get('labels', [])
        label_section = ""
        if labels:
            label_section = f"\n## 🏷️ Labels\n{', '.join(labels)}\n"
        
        # Build components
        components = [c['name'] for c in fields.get('components', [])]
        component_section = ""
        if components:
            component_section = f"\n## 📦 Components\n{', '.join(components)}\n"
        
        # Get description safely
        description = fields.get('description', '')
        if isinstance(description, dict):
            # If it's Atlassian Document Format, extract text
            description = self._extract_text_from_adf(description)
        elif description is None:
            description = 'No description provided'
        
        issue_body = f"""## 🐛 Bug Report from Jira

**Jira Key:** [{self.bug_key}]({CONFIG['JIRA_BASE_URL']}/browse/{self.bug_key})  
**Priority:** {fields.get('priority', {}).get('name', 'Medium')}  
**Status:** {fields.get('status', {}).get('name', 'Unknown')}  
**Reporter:** {fields.get('reporter', {}).get('displayName', 'Unknown')}  

## 📝 Description
{description}

## 🌍 Environment
{fields.get('environment', 'Not specified')}

{label_section}

{component_section}

{attachment_section}

---
*Automatically created on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*  
*💰 Zero-Cost Python Integration* 🐍
"""
        
        # Prepare API request
        owner, repo = CONFIG['GITHUB_REPOSITORY'].split('/')
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        
        priority = fields.get('priority', {}).get('name', 'Medium').lower()
        issue_data = {
            'title': f"[{self.bug_key}] {fields['summary']}",
            'body': issue_body,
            'labels': ['jira-bug', 'automated', priority] + labels
        }
        
        request = urllib.request.Request(
            url,
            data=json.dumps(issue_data).encode('utf-8'),
            method='POST'
        )
        request.add_header('Authorization', f"Bearer {CONFIG['GITHUB_TOKEN']}")
        request.add_header('Accept', 'application/vnd.github+json')
        request.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                self.github_issue_number = result['number']
                self.github_issue_url = result['html_url']
                print(f"✅ Created GitHub issue #{self.github_issue_number}")
                print(f"   URL: {self.github_issue_url}")
                
        except urllib.error.HTTPError as e:
            print(f"❌ Failed to create GitHub issue: {e.code} - {e.reason}")
            print(f"   Response: {e.read().decode('utf-8')}")
            raise
    
    def _extract_text_from_adf(self, adf_doc):
        """Extract plain text from Atlassian Document Format"""
        if not isinstance(adf_doc, dict):
            return str(adf_doc)
        
        text_parts = []
        
        def extract_content(node):
            if isinstance(node, dict):
                if node.get('type') == 'text':
                    text_parts.append(node.get('text', ''))
                if 'content' in node:
                    for child in node['content']:
                        extract_content(child)
            elif isinstance(node, list):
                for item in node:
                    extract_content(item)
        
        extract_content(adf_doc)
        return '\n'.join(text_parts) if text_parts else 'No description provided'
    
    def update_jira(self):
        """Add comment to Jira with GitHub issue link"""
        print("🔗 Updating Jira with GitHub link...")
        
        url = f"{CONFIG['JIRA_BASE_URL']}/rest/api/3/issue/{self.bug_key}/comment"
        
        comment_data = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "🔗 GitHub Issue created: "
                            },
                            {
                                "type": "text",
                                "text": f"#{self.github_issue_number}",
                                "marks": [
                                    {
                                        "type": "link",
                                        "attrs": {
                                            "href": self.github_issue_url
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        
        auth_string = f"{CONFIG['JIRA_EMAIL']}:{CONFIG['JIRA_API_TOKEN']}"
        auth_bytes = base64.b64encode(auth_string.encode('utf-8'))
        auth_header = f"Basic {auth_bytes.decode('utf-8')}"
        
        request = urllib.request.Request(
            url,
            data=json.dumps(comment_data).encode('utf-8'),
            method='POST'
        )
        request.add_header('Authorization', auth_header)
        request.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                print(f"✅ Updated Jira with GitHub link")
                
        except urllib.error.HTTPError as e:
            print(f"⚠️  Failed to update Jira: {e.code} - {e.reason}")
    
    @staticmethod
    def _format_size(size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        bug_key = sys.argv[1]
    else:
        bug_key = os.environ.get('JIRA_BUG_KEY')
    
    if not bug_key:
        print("❌ Error: Bug key not provided", file=sys.stderr)
        return 1
    
    missing = [k for k, v in CONFIG.items() if not v]
    if missing:
        print(f"❌ Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        return 1
    
    processor = JiraGitHubProcessor(bug_key)
    return processor.run()


if __name__ == '__main__':

    sys.exit(main())

