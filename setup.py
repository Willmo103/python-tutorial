from setuptools import setup, find_packages

setup(
    name="slides-parser",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
    ],
    entry_points="""
        [console_scripts]
        next=cli:next_slide
        reset=cli:reset
    """,
)
