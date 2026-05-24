#!/usr/bin/env python3
"""
Weekly batch article generation and posting.

Workflow:
1. Fetch 3 unprocessed ideas from Notion
2. Generate article for each idea using Claude API
3. Create draft in WordPress
4. Update Notion status to processed
"""

import sys
import json
from datetime import datetime
from notion_fetcher import fetch_unprocessed_ideas, update_status_to_processed
from article_generator import generate_article
from wordpress_poster import create_draft_post
from image_generator import generate_featured_image

def run_batch(num_articles=3, dry_run=False):
    """
    Run the weekly batch article generation.

    Args:
        num_articles: Number of articles to generate (default 3)
        dry_run: If True, don't update WordPress or Notion (for testing)
    """
    print(f'[{datetime.now().isoformat()}] Starting batch article generation...')
    print(f'Mode: {"DRY RUN" if dry_run else "LIVE"}')
    print()

    # Step 1: Fetch ideas from Notion
    print('Step 1: Fetching unprocessed ideas from Notion...')
    try:
        ideas = fetch_unprocessed_ideas(limit=num_articles)
        print(f'✓ Fetched {len(ideas)} ideas')
        for idea in ideas:
            print(f"  - {idea['title']} ({idea['category']})")
    except Exception as e:
        print(f'✗ Error fetching ideas: {e}')
        return False
    print()

    # Step 2-4: Generate articles, create drafts, update Notion
    results = []
    for idx, idea in enumerate(ideas, 1):
        print(f'Processing idea {idx}/{len(ideas)}: {idea["title"]}')

        try:
            # Generate article
            print('  Generating article with Claude API...')
            article_content = generate_article(
                title=idea['title'],
                category=idea['category'],
                memo=idea['memo']
            )
            print(f'  ✓ Generated {len(article_content)} characters')

            # Generate featured image metadata
            print('  Preparing featured image...')
            image_result = generate_featured_image(idea['title'], idea['category'])
            print(f'  ✓ Image metadata: {image_result.get("status")}')

            # Create WordPress draft
            if not dry_run:
                print('  Creating WordPress draft...')
                post_result = create_draft_post(
                    title=idea['title'],
                    content=article_content,
                    category=idea['category'],
                    featured_image_url=image_result.get('design_url') or image_result.get('color')
                )

                if post_result.get('status') == 'success':
                    print(f'  ✓ Draft created: {post_result["edit_url"]}')

                    # Update Notion status
                    print('  Updating Notion status...')
                    update_status_to_processed(idea['id'])
                    print('  ✓ Notion status updated')

                    results.append({
                        'idea': idea['title'],
                        'post_id': post_result.get('post_id'),
                        'edit_url': post_result.get('edit_url'),
                        'status': 'success'
                    })
                else:
                    print(f'  ✗ WordPress error: {post_result.get("error")}')
                    results.append({
                        'idea': idea['title'],
                        'status': 'failed',
                        'error': post_result.get('error')
                    })
            else:
                print('  [DRY RUN] WordPress draft not created')
                results.append({
                    'idea': idea['title'],
                    'status': 'dry_run'
                })

        except Exception as e:
            print(f'  ✗ Error processing idea: {e}')
            results.append({
                'idea': idea['title'],
                'status': 'error',
                'error': str(e)
            })

        print()

    # Summary
    print('=' * 60)
    print('Batch Summary')
    print('=' * 60)
    successful = sum(1 for r in results if r['status'] == 'success')
    failed = sum(1 for r in results if r['status'] == 'failed')
    print(f'Successful: {successful}/{len(ideas)}')
    print(f'Failed: {failed}/{len(ideas)}')
    print()

    for result in results:
        if result['status'] == 'success':
            print(f"✓ {result['idea']}")
            print(f"  URL: {result['edit_url']}")
        elif result['status'] == 'failed':
            print(f"✗ {result['idea']}")
            print(f"  Error: {result['error']}")
        else:
            print(f"~ {result['idea']} ({result['status']})")

    print()
    print(f'[{datetime.now().isoformat()}] Batch complete')

    return successful == len(ideas) or len(ideas) == 0

if __name__ == '__main__':
    # Run with 3 articles by default, or 1 for testing
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    num_articles = 3
    if '--num' in sys.argv:
        idx = sys.argv.index('--num')
        num_articles = int(sys.argv[idx + 1])

    success = run_batch(num_articles=num_articles, dry_run=dry_run)
    sys.exit(0 if success else 1)
