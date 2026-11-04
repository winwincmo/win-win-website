# Win-Win website + daily article publishing

This is a custom responsive website for Win-Win, with a home page, services, inquiry form, an article index, individual SEO-friendly article pages, sitemap and RSS feed.

## Open the site locally

Install Python 3.10+, then in this folder:

```bash
pip install -r requirements.txt
python build.py
cd dist
python -m http.server 8000
```

Open http://localhost:8000 in your browser. Avoid opening HTML files directly from the filesystem: the links expect a web server.

## Set it up so you can publish articles daily through your browser

The recommended setup uses **GitHub Pages** for hosting and **Pages CMS** for editing. It doesn't require a paid blog platform.

1. Create a GitHub account if needed. Create a new repository, for example `win-win-website`.
2. Upload **the contents** of this folder to the repository's `main` branch, including hidden files `.pages.yml` and `.github/workflows/deploy.yml`. Don't upload the generated `dist` folder.
3. In GitHub repository **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source. The included workflow will build and publish the site after each change.
4. Go to **https://pagescms.org**, sign in with GitHub, and grant access to this repository. Choose **Blog articles** and write a new post using the rich-text editor. Turn on **Publish this article**, then save. Pages CMS commits the article to GitHub and triggers automatic website redeployment.
5. Before publishing publicly, edit `site.json`: set `site_url` to the final website URL (including https). For GitHub Pages without a custom domain, use `https://YOURUSERNAME.github.io/YOUR-REPOSITORY` (the generator will add the repository path to internal links), and set `contact_email` to the real inbox you want inquiries sent to. This also updates the sitemap and RSS links. Keep `contact_email` blank until you're ready; the form then lets visitors copy a prepared message, rather than pretending to submit to a server.

**Important:** this package isn't already hosted or connected to your GitHub account. You must complete the account setup and deployment steps. Publishing may take a moment after each article save.

## Edit or add posts manually

Each `.md` file under `posts/` represents an article with a title, date, excerpt, category, and `published` flag in YAML at the top. The text below the frontmatter is Markdown. Create one file per article with a simple lowercase-hyphenated filename (its URL slug). Run `python build.py` to update the site. Set `published: false` to keep a draft off the public website.

The included two articles are **starter editorial drafts** to review and customize before going live; no testimonials or invented business results are used.

## Customize

- `site.json`: business details and contact email.
- `templates/`: homepage, blog and article layouts.
- `assets/styles.css`: colors, type and layout.
- `assets/styles.css`: website palette and geometric homepage illustration.
- `.pages.yml`: browser editor setup.

The contact form currently creates an email draft via `mailto:` once an address is configured. It does not collect or store website visitors' data on a backend, and it does not send messages without the visitor using their email application. For more reliable contact submissions, connect a service like Formspree or your preferred CRM form later.

## Domain

You can connect a purchased domain through GitHub Pages settings. Add the domain to `site.json` too. Check domain and trademark availability before branding the public launch.
