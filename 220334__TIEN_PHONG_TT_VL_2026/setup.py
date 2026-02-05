from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="image_processing_demo",
    version="2.0.0",
    author="Your Name",
    description="Advanced image processing and banner creation with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/220334_TIEN_PHONG_TT_VL_2026",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        line.strip() 
        for line in open("requirements.txt").readlines() 
        if line.strip() and not line.startswith("#")
    ],
)
