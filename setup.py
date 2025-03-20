from setuptools import setup, find_packages

install_requires = [
    "praw>=7.7.1",
    "pandas>=2.1.4",
    "python-dotenv>=1.0.0",
    "ntscraper>=0.3.17",  # Updated to use the latest available version
]

setup(
    name="ai_agent_utilities",
    version="0.1",
    packages=find_packages(),
    install_requires=install_requires,
    description="Utilities for AI agents, including data scraping tools",
    author="Suman Urawat",
    python_requires=">=3.8",
)