from setuptools import setup, find_packages

setup(
    name="mavis-chop-shop",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==3.0.2",
        "flask-cors==4.0.0", 
        "rembg==2.0.69",
        "Pillow==10.3.0",
        "gunicorn==21.2.0",
    ],
)
