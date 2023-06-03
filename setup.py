from setuptools import setup, find_packages
 
setup(name = "packages", packages = find_packages())


"""
ImportError: intento de importación relativa sin paquete principal conocido
https://www.pythonpool.com/importerror-attempted-relative-import-with-no-known-parent-package/#:~:text=This%20article%20will%20discuss%20the,python%20files%20results%20in%20ImportError.



en consola 

en un entorno VENV (ir al direceterio a nivel Lib con cd carpeta y ejecutar el comando)
python /c/CURSOS/Repositorios/Web_Scraping_pr/setup.py install

python setup.py install
"""