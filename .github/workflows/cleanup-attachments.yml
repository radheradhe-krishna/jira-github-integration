#!/usr/bin/env python3
"""
Cleanup script to delete GitHub Releases containing Jira attachments
after PR is merged.
"""

import os
import sys
import json
import urllib.request
import urllib.error


def delete_releases_for_bug(bug_key):
    """Delete all releases associated with a Jira bug key"""
    
    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    
    if not token or not repo:
        print("❌ Missing GITHUB_TOKEN or GITHUB_REPOSITORY")
        return 1
    
    print("=" * 70)
    print("🧹 Cleaning up attachments for merged PR")
    print("=" * 70)
    print(f"Bug Key: {bug_key}")
    print()
    
    # List all releases
    owner, repo_name = repo.split('/')
    releases_url = f"https://api.github.com/repos/{owner}/{repo_name}/releases"
    
    request = urllib.request.Request(releases_url)
    request.add_header('Authorization', f"Bearer {token}")
    request.add_header('Accept', 'application/vnd.github+json')
    request.add_header('X-GitHub-Api-Version', '2022-11-28')
    
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            releases = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to list releases: {e.code} - {e.reason}")
        return 1
    
    # Find releases matching the bug key pattern
    bug_key_lower = bug_key.lower()
    matching_releases = [
        r for r in releases 
        if r['tag_name'].startswith(f"jira-{bug_key_lower}-")
    ]
    
    if not matching_releases:
        print(f"ℹ️  No releases found for {bug_key}")
        print("   This is normal if no attachments were uploaded.")
        return 0
    
    print(f"📦 Found {len(matching_releases)} release(s) to delete:")
    for release in matching_releases:
        print(f"   - {release['tag_name']} ({len(release.get('assets', []))} assets)")
    print()
    
    # Delete each release
    deleted_count = 0
    for release in matching_releases:
        release_id = release['id']
        tag_name = release['tag_name']
        
        delete_url = f"https://api.github.com/repos/{owner}/{repo_name}/releases/{release_id}"
        
        request = urllib.request.Request(delete_url, method='DELETE')
        request.add_header('Authorization', f"Bearer {token}")
        request.add_header('Accept', 'application/vnd.github+json')
        request.add_header('X-GitHub-Api-Version', '2022-11-28')
        
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                print(f"✅ Deleted release: {tag_name}")
                deleted_count += 1
        except urllib.error.HTTPError as e:
            print(f"⚠️  Failed to delete {tag_name}: {e.code} - {e.reason}")
    
    print()
    print("=" * 70)
    print(f"✅ Cleanup Complete! Deleted {deleted_count} release(s)")
    print("=" * 70)
    
    return 0


def main():
    if len(sys.argv) < 2:
        print("Usage: cleanup_attachments.py <BUG-KEY>")
        return 1
    
    bug_key = sys.argv[1]
    return delete_releases_for_bug(bug_key)


if __name__ == '__main__':
    sys.exit(main())
