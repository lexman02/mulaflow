# MulaFlow
CSCI 3030 Project

## Useful Links
### Git/GitHub
- [Getting Started With Git](https://www.w3schools.com/git/git_getstarted.asp?remote=github)
- [How To Download The Project From GitHub](https://www.w3schools.com/git/git_clone.asp?remote=github)
- [Using Git in VS Code](https://code.visualstudio.com/docs/sourcecontrol/intro-to-git)
- [Using Git in PyCharm](https://www.jetbrains.com/help/pycharm/set-up-a-git-repository.html)

### Frontend
- [Heroicons (Icons used in Figma)](https://heroicons.com/)
- [Tailwind CSS (Colors and misc. styling)](https://tailwindcss.com/docs/utility-first)
- [Django Templating Documentation](https://docs.djangoproject.com/en/4.2/topics/templates/)
  - [List of all built-in template tags and filters](https://docs.djangoproject.com/en/4.2/ref/templates/builtins/)

### Backend
- [Django](https://docs.djangoproject.com/en/4.2/)

### Misc.
- [Sample Project](https://github.com/Renato79/delitaly/tree/master)
- [MDN Django App Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django)
- [Using Python Virtual Environments](https://geekflare.com/virtual-environments-python/#geekflare-toc-how-to-create-a-python-virtual-environment-in-ubuntu)
  - [Using Python Virtual Environments (Windows Instructions)](https://geekflare.com/virtual-environments-python/#geekflare-toc-how-to-create-a-python-virtual-environment-in-windows)

## Development Instructions
> [!NOTE]
> Both the frontend and backend server automatically refresh on save so you don't have to re-run these commands on changes.
1. Install the dependencies in your virtual environment `pip install -r requirements.txt`
2. Install the frontend packages
  - npm `npm install`
  - yarn `yarn install`
  - pnpm `pnpm install`
1. Run the development servers
   1. Frontend: Bundles and compiles the CSS (Tailwind)
       - npm `npm run dev`
       - yarn `yarn dev`
   2. Backend: Serves the frontend assets and web app
       - Mac/Linux `python3 manage.py runserver`
       - Windows `py -3 manage.py runserver`
