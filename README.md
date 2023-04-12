# PubHub

PubHub is a an ActivityPub server implementation in python using the **Django**
framework. PubHub is meant to be used as a template for an existing project or
a backend for your own ActivityPub server. This is still in development and
should not be used in production.

![](https://img.shields.io/github/issues/walizw/PubHub)
![](https://img.shields.io/github/repo-size/walizw/PubHub)
![](https://img.shields.io/github/issues-closed/walizw/PubHub)
![](https://img.shields.io/github/license/walizw/PubHub)
![](https://img.shields.io/github/stars/walizw/PubHub)
![](https://img.shields.io/github/commit-activity/m/walizw/PubHub)

## Quickstart

To get started clone the PubHub repository:

```bash
git clone https://github.com/walizw/PubHub.git
```

Create a virtual environment and activate it:

```bash
cd PubHub
python -m venv venv
. venv/bin/activate
```

Finally, install the dependencies:

```bash
pip install -r requirements.txt
```

I recommend you reading the [docs](docs/) for more information on setting
PubHub up.

### Running tests

If you want to run the tests (to ensure everything is working correctly),
you can execute `pytest` on the folder `tests`. Note that you have to be inside
the virtual environment that has pytest installed:

```bash
pytest tests
```