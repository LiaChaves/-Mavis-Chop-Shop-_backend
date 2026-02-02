from setuptools import setup

setup(
    name="mavis-backend",
    version="1.0.0",
    install_requires=[
        "Flask==2.3.3",
        "flask-cors==4.0.0",
        "rembg==2.0.69",
        "Pillow==9.5.0",
        "gunicorn==20.1.0",
    ],
)
