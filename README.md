# PubHub

🍄 PubHub is a simple ActivityPub server. It is meant to be used as a starting
point for other projects or a complete backend for your decentralised
application. 🌸

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