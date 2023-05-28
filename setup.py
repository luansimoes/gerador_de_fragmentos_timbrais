setup(
    name="parsimonious_system",
    version="0.1.0",
    description="Compositional System that generates musical fragments with aid of Parsimonious Graphs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/luansimoes/parsimonious_system",
    author="Luan Simões",
    author_email="luansimoes@cos.ufrj.br",
    license="",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["app"],
    include_package_data=True,
    install_requires=[
        "edopi", "scamp", "pysimplegui"
    ],
    entry_points={"console_scripts": ["parsimonious_system=app.main:main"]},
)