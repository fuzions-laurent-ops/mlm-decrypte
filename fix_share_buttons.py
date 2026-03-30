#!/usr/bin/env python3
"""
Fix share button scripts across all article files.
Replaces the old share button script with the corrected version.
"""

import os
import glob
import re

articles_dir = "/sessions/loving-wonderful-volta/mnt/MLM/articles"

# Old script to find - using literal string matching instead of regex
old_script_pattern = """(function(){
  var u=encodeURIComponent(window.location.href);
  var t=encodeURIComponent(document.title);
  var wa=document.getElementById('sh-wa');
  var fb=document.getElementById('sh-fb');
  var li=document.getElementById('sh-li');
  var x=document.getElementById('sh-x');
  if(wa)wa.href='https://wa.me/?text='+t+'%20'+u;
  if(fb)fb.href='https://www.facebook.com/sharer/sharer.php?u='+u;
  if(li)li.href='https://www.linkedin.com/shareArticle?mini=true&url='+u+'&title='+t;
  if(x)x.href='https://twitter.com/intent/tweet?url='+u+'&text='+t;
})();"""

# New script to replace with
new_script = """(function(){
  var canonical=document.querySelector('link[rel="canonical"]');
  var pageUrl=canonical?canonical.href:window.location.href;
  var u=encodeURIComponent(pageUrl);
  var t=encodeURIComponent(document.title.split(' — ')[0]);
  var wa=document.getElementById('sh-wa');
  var fb=document.getElementById('sh-fb');
  var li=document.getElementById('sh-li');
  var x=document.getElementById('sh-x');
  if(wa){wa.href='https://wa.me/?text='+t+'%20'+u;wa.onclick=function(e){e.preventDefault();window.open(this.href,'wa','width=600,height=500');}}
  if(fb){fb.href='https://www.facebook.com/sharer/sharer.php?u='+u;fb.onclick=function(e){e.preventDefault();window.open(this.href,'fb','width=600,height=400');}}
  if(li){li.href='https://www.linkedin.com/sharing/share-offsite/?url='+u;li.onclick=function(e){e.preventDefault();window.open(this.href,'li','width=600,height=400');}}
  if(x){x.href='https://twitter.com/intent/tweet?url='+u+'&text='+t;x.onclick=function(e){e.preventDefault();window.open(this.href,'tw','width=600,height=400');}}
})();"""

# Find all HTML files
html_files = sorted(glob.glob(os.path.join(articles_dir, "*.html")))

updated_count = 0
skip_count = 0
not_found_count = 0

for filepath in html_files:
    filename = os.path.basename(filepath)

    # Skip the file that's already done
    if filename == "pourquoi-blog-mlm-decrypte.html":
        skip_count += 1
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try flexible pattern matching with variable whitespace
    # Match the exact script but allow flexible whitespace
    flexible_pattern = r"\(function\(\)\{\s*var u=encodeURIComponent\(window\.location\.href\);\s*var t=encodeURIComponent\(document\.title\);\s*var wa=document\.getElementById\('sh-wa'\);\s*var fb=document\.getElementById\('sh-fb'\);\s*var li=document\.getElementById\('sh-li'\);\s*var x=document\.getElementById\('sh-x'\);\s*if\(wa\)wa\.href='https://wa\.me/\?text='\+t\+'\%20'\+u;\s*if\(fb\)fb\.href='https://www\.facebook\.com/sharer/sharer\.php\?u='\+u;\s*if\(li\)li\.href='https://www\.linkedin\.com/shareArticle\?mini=true&url='\+u\+'\&title='\+t;\s*if\(x\)x\.href='https://twitter\.com/intent/tweet\?url='\+u\+'\&text='\+t;\s*\}\)\(\);"

    new_content = re.sub(flexible_pattern, new_script, content, flags=re.MULTILINE | re.DOTALL)

    if new_content != content:
        # Replacement was successful
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Updated: {filename}")
        updated_count += 1
    else:
        print(f"✗ Pattern not found: {filename}")
        not_found_count += 1

print(f"\n=== Summary ===")
print(f"Updated: {updated_count}")
print(f"Skipped: {skip_count} (pourquoi-blog-mlm-decrypte.html)")
print(f"Not found: {not_found_count}")
print(f"Total files: {len(html_files)}")
