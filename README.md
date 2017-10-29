# C3FOCSite
This is the repository for the C3FOC web site. Follow @c3foc on twitter for upcoming news.
The website is written for and using python3. Using python2.x may work but is untested and unintended.

## required python packages

 * django
 * markdown
 * MarkdownSuperscript
 * MarkdownSubscript
 * pyembed-markdown
 * django_extensions

## Structure

 * The entire content of the website is located inside the
   frontpage app.
 * While django provides a way to access the database directly (the
   admin interface) the C3FOC site features an self implemented admin
   panel. This is not me being super stupid but thinking that editing
   the database content from hand (including compiling posts from hand)
   is stupid.
 * Djangos internal admin system is also implemented inside the website
   but only accessible to the root users and meant to be used if
   something horrible happens
 * Djangos internal rendering engine (templates and forms) isn't used in
   here since it can be very slow and is very complex. After all we deploy
   this website to thousands of hackers and don't want the website to be
   DDOSed by accident or having to notice some SQL injections :-)

## Under the hood

The user writes the text of posts and article descriptions as markdown.
The website will then save the markdown source and parse it. The generated
html will be stored inside the database as well (under the 'cachedText'
attributes) and a query will only display the cached text rather than
recompiling the markdown every time the website gets accessed. Since the
markdown package is used the behaviour is altered a bit. The following
extensions are loaded when compiling markdown sources:

* markdown.extensions.extra
* markdown.extensions.admonition
* markdown.extensions.toc
* markdown.extensions.wikilinks
* superscript
* subscript
* pyembed

I'm not convinced by the usage of the django-markdown package since it
requires the usage of the sometimes buggy django-forms but doesn't give
enough extra functionality in order to take on the hassle of maintaining
it properly. A simple 'show preview' button should do the trick as well.

#### User rights

The following rights show what logged in users are allowed to do. This
corresponds to the <code>c3shop.frontpage.models.Profile.rights</code>
value. A user who has a higher rights value is allowed to do all the
stuff that requires a lower rights value. The reason this isn't bound to
django's right management is due to me not wanting to allow other apps
to mess with these permissions. The ones from django keep in existence
and apply to other apps and django's native admin panel.

* 0 -> No special permits
* 1 -> Use the 'N units sold button' on articles
* 2 -> Edit other properties of articles and add new ones
* 3 -> Write and edit posts
* 4 -> Add users and change settings

## Deployment

Have a look at PushToProduction file for detailed information on how to
deploy this website.

## Settings
#### Store Open
The <code>frontpage.store.open</code> setting manages the store icon
on the index page. When it contains a <code>true</code> it will render
the store as open, or otherwise (<code>false</code>) as closed.
#### Nav Bar and Footer
The settings for the navigation bar located in the header contains the
following setting keys:
* <code>frontpage.ui.navbar.content</code>
    - The content of this variable is used to determine which items the
      nav bar should contain.
    - The setting contains multiple items notated in JSON format.
    - Each item must contain a <code>type</code> object
    - Only the <code>link</code> type is supported yet but others may
      come
    - A valid example may look like the following:
        <code>
        [{
            "type":"link",
            "href":"example.com","text":"Visit example.com"
        },{"type":"link","text":"Visit the top level website",
        "href":".."}]
        </code>
    - The example above would display two links displaying "Visit
    example.com" and "Visit the top level website" and would redirect to
    example.com and ..
* <code>frontpage.ui.footer.content</code>
    - This setting entry is basically the same as the one above but
      handles the footer of the content parts.
    - It uses the same JSON syntax

## Setup
First install all dependencies using pip3. Then run the following commands:
<code>
python3 manage.py migrate
python3 manage.py collectstatics
PYCAM="from test.init_database import *\ninit_db()"
python3 manage.py shell_plus < echo $PYCAM
</code>
At last configure your web server to serve the static files.

## Password rules
 * At least 6 characters long
 * must contain upper and lower case letters